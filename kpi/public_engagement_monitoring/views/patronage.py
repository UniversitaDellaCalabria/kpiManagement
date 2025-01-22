from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from organizational_area.models import *

from template.utils import *

from .. decorators.generic import *
from .. decorators.patronage import *
from .. forms import *
from .. models import *
from .. settings import *
from .. utils import *
from .. views import management


@login_required
@patronage_operator_structures
def dashboard(request, structures=None):
    template = 'pem/patronage/dashboard.html'

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   '#': _('Patronage operator')}

    active_years = PublicEngagementAnnualMonitoring.objects\
                                                   .filter(is_active=True)\
                                                   .values_list('year', flat=True)
    events_per_structure = {}
    for structure in structures:
        to_evaluate = PublicEngagementEventData.objects.filter(event__structure=structure.office.organizational_structure,
                                                               event__start__year__in=active_years,
                                                               patronage_requested=True,
                                                               event__operator_evaluation_date__isnull=False,
                                                               event__operator_evaluation_success=True,
                                                               event__manager_taken_date__isnull=True).count()
        events_per_structure[structure.office.organizational_structure] = to_evaluate
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'events_per_structure': events_per_structure})


@login_required
@is_structure_patronage_operator
def events(request, structure_slug):
    template = 'pem/patronage/events.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:patronage_operator_dashboard'): _('Patronage operator'),
                   '#': structure_slug}
    api_url = reverse('public_engagement_monitoring:api_patronage_operator_events', kwargs={'structure_slug': structure_slug})
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'api_url': api_url,
                                      'structure_slug': structure_slug})


@login_required
@is_structure_patronage_operator
def event(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.prefetch_related('data')\
                                         .filter(pk=event_id,
                                                 structure__slug=structure_slug,
                                                 data__patronage_requested=True).first()
    if not event:
        messages.add_message(request, messages.ERROR,
                             "<b>{}</b>: {}".format(_('Alert'), _('URL access is not allowed')))
        return redirect('public_engagement_monitoring:patronage_operator_events', structure_slug=structure_slug)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:patronage_operator_dashboard'): _('Patronage operator'),
                   reverse('public_engagement_monitoring:patronage_operator_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                   '#': event.title}
    template = 'pem/patronage/event.html'

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(event).pk,
                                   object_id=event.pk)

    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event': event,
                                      'logs': logs,
                                      'structure_slug': structure_slug})


@login_required
@is_structure_patronage_operator
def take_event(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.prefetch_related('data')\
                                         .filter(pk=event_id,
                                                 structure__slug=structure_slug,
                                                 data__patronage_requested=True).first()

    if not event:
        return custom_message(request, _("Access denied"), 403)
    if not event.can_be_taken_by_patronage_operator():
        return custom_message(request, _("Access denied"), 403)

    event.patronage_operator_taken_by = request.user
    event.patronage_operator_taken_date = timezone.now()
    event.modified_by = request.user
    event.save()

    log_action(user=request.user,
               obj=event,
               flag=CHANGE,
               msg='{}: {}'.format(structure_slug, _('taken')))

    messages.add_message(request, messages.SUCCESS,
                         _("Event taken successfully"))

    # invia email al referente/compilatore
    subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('taken'))
    body = "{} {} {}".format(request.user, _('is evaluating the event'), '.')
    send_email_to_event_referents(event, subject, body)

    return redirect('public_engagement_monitoring:patronage_operator_event',
                    structure_slug=structure_slug,
                    event_id=event_id)


@login_required
@is_structure_patronage_operator
def event_evaluation(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.prefetch_related('data')\
                                         .filter(pk=event_id,
                                                 structure__slug=structure_slug,
                                                 data__patronage_requested=True).first()

    if not event:
        return custom_message(request, _("Access denied"), 403)

    if not event.is_ready_for_patronage_operator_evaluation():
        return custom_message(request, _("Access denied"), 403)

    form = PublicEngagementEventEvaluationForm()
    template = 'pem/event_evaluation.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:patronage_operator_dashboard'): _('Patronage operator'),
                   reverse('public_engagement_monitoring:patronage_operator_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                   reverse('public_engagement_monitoring:patronage_operator_event', kwargs={'structure_slug': structure_slug, 'event_id': event_id}): '{}'.format(event.title),
                   '#': _('Evaluation')}

    if request.method == 'POST':
        form = PublicEngagementEventEvaluationForm(data=request.POST)
        if form.is_valid():
            event.patronage_granted_date = timezone.now()
            event.patronage_granted = form.cleaned_data['success']
            event.patronage_granted_by = request.user
            event.patronage_granted_notes = form.cleaned_data['notes']
            event.modified_by = request.user
            event.save()

            messages.add_message(request, messages.SUCCESS, _("Patronage evaluation completed"))

            result = _('approved') if form.cleaned_data['success'] else _('not approved')
            msg = '{} - {}: {}'.format(structure_slug, _('patronage evaluation completed'), result)
            if not form.cleaned_data['success']:
                msg += ' {}'.format(operator_notes)

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg=msg)

            # invia email al referente/compilatore
            subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('Patronage evaluation completed'))
            body = "{} {} {}".format(request.user, _('has evaluated the event with the result'), result)
            send_email_to_event_referents(event, subject, body)

            # invia email ai manager
            send_email_to_managers(subject, body)

            return redirect("public_engagement_monitoring:patronage_operator_event",
                            structure_slug=structure_slug,
                            event_id=event_id)
        else:
            messages.add_message(request, messages.ERROR,
                                 "<b>{}</b>: {}".format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'event': event, 'form': form, 'structure_slug': structure_slug})


@login_required
@is_structure_patronage_operator
def event_reopen_evaluation(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.prefetch_related('data')\
                                         .filter(pk=event_id,
                                                 structure__slug=structure_slug,
                                                 data__patronage_requested=True).first()
    if not event:
        return custom_message(request, _("Access denied"), 403)

    if not event.can_patronage_operator_cancel_evaluation():
        return custom_message(request, _("Access denied"), 403)

    event.patronage_granted_date = None
    event.modified_by = request.user
    event.save()

    log_action(user=request.user,
               obj=event,
               flag=CHANGE,
               msg='{}:  {}'.format(structure_slug, _('patronage evaluation reopened')))

    messages.add_message(request, messages.SUCCESS, _("Evaluation reopened"))

    # email
    subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('patronage evaluation reopened'))
    body = "{} {} {}".format(request.user, _('has reopened patronage evaluation of the event'), '.')
    send_email_to_event_referents(event, subject, body)

    # invia email ai manager
    if event.patronage_granted:
        send_email_to_managers(subject, body)

    return redirect("public_engagement_monitoring:patronage_operator_event",
                    structure_slug=structure_slug,
                    event_id=event_id)
