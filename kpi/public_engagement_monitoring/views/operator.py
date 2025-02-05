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
from .. decorators.operator import *
from .. forms import *
from .. models import *
from .. settings import *
from .. utils import *
from .. views import management


@login_required
@evaluation_operator_structures
def dashboard(request, structures=None):
    template = 'pem/operator/dashboard.html'

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   '#': _('Structure operator')}

    active_years = PublicEngagementAnnualMonitoring.objects\
                                                   .filter(is_active=True)\
                                                   .values_list('year', flat=True)
    events_per_structure = {}
    for structure in structures:
        to_evaluate = PublicEngagementEvent.objects.filter(structure=structure.office.organizational_structure,
                                                           start__year__in=active_years,
                                                           to_evaluate=True,
                                                           operator_taken_date__isnull=True,
                                                           created_by_manager=False).count()
        events_per_structure[structure.office.organizational_structure] = to_evaluate
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'events_per_structure': events_per_structure})


@login_required
@is_structure_evaluation_operator
def events(request, structure_slug):
    template = 'pem/operator/events.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:operator_dashboard'): _('Structure operator'),
                   '#': structure_slug.upper()}
    api_url = reverse('public_engagement_monitoring:api_evaluation_operator_events', kwargs={'structure_slug': structure_slug})
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'api_url': api_url,
                                      'structure_slug': structure_slug})


@login_required
@is_structure_evaluation_operator
def event(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.filter(pk=event_id,
                                                 structure__slug=structure_slug).first()
    if not event:
        messages.add_message(request, messages.ERROR,
                             "<b>{}</b>: {}".format(_('Alert'), _('URL access is not allowed')))
        return redirect('public_engagement_monitoring:operator_events', structure_slug=structure_slug)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:operator_dashboard'): _('Structure operator'),
                   reverse('public_engagement_monitoring:operator_events', kwargs={'structure_slug': structure_slug}): structure_slug.upper(),
                   '#': event.title}
    template = 'pem/operator/event.html'

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(event).pk,
                                   object_id=event.pk)

    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event': event,
                                      'logs': logs,
                                      'structure_slug': structure_slug})


@login_required
@is_structure_evaluation_operator
def take_event(request, structure_slug, event_id):
    event = get_object_or_404(PublicEngagementEvent,
                              pk=event_id,
                              structure__slug=structure_slug)

    if not event.can_be_handled_for_evaluation():
        messages.add_message(request, messages.DANGER, _("Access denied"))
        return redirect('public_engagement_monitoring:operator_events',
                        structure_slug=structure_slug)

    event.operator_taken_by = request.user
    event.operator_taken_date = timezone.now()
    event.modified_by = request.user
    event.save()
    messages.add_message(request, messages.SUCCESS,
                         _("Event handled successfully"))

    log_action(user=request.user,
               obj=event,
               flag=CHANGE,
               msg="[Operatore {}] Iniziativa presa in carico".format(structure_slug))

    # invia email al referente/compilatore
    subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('handled'))
    body = "{} {} {}".format(request.user, _('is evaluating the event'), '.')
    send_email_to_event_referents(event, subject, body)

    return redirect('public_engagement_monitoring:operator_event',
                    structure_slug=structure_slug,
                    event_id=event_id)


@login_required
@is_structure_evaluation_operator
@is_editable_by_operator
def event_basic_info(request, structure_slug, event_id, event=None):
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:operator_dashboard'): _('Structure operator'),
                   reverse('public_engagement_monitoring:operator_events', kwargs={'structure_slug': structure_slug}): structure_slug.upper(),
                   reverse('public_engagement_monitoring:operator_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                   '#': _('General informations')}

    template = 'pem/event_basic_info.html'
    form = PublicEngagementEventOperatorForm(request=request, instance=event)
    # post
    if request.method == 'POST':
        form = PublicEngagementEventOperatorForm(request=request,
                                         instance=event,
                                         data=request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.modified_by = request.user
            event.save()

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg="[Operatore {}] Informazioni generali modificate".format(structure_slug))

            messages.add_message(request, messages.SUCCESS,
                                 _("Modified general informations successfully"))

            # invia email al referente/compilatore
            subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('data modified'))
            body = '{} {} {}'.format(request.user, _('has modified the data of the event'), '.')

            send_email_to_event_referents(event, subject, body)

            return redirect("public_engagement_monitoring:operator_event",
                            structure_slug=structure_slug,
                            event_id=event_id)

        else:  # pragma: no cover
            messages.add_message(request, messages.ERROR,
                                 '<b>{}</b>: {}'.format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs, 'event': event, 'form': form})


@login_required
@is_structure_evaluation_operator
@is_editable_by_operator
def event_data(request, structure_slug, event_id, event=None):
    result = management.event_data(request=request,
                                   structure_slug=structure_slug,
                                   event_id=event_id,
                                   event=event)
    if result == True:
        return redirect("public_engagement_monitoring:operator_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_structure_evaluation_operator
@is_editable_by_operator
def event_people(request, structure_slug, event_id, event=None):
    result = management.event_people(request=request,
                                     structure_slug=structure_slug,
                                     event_id=event_id,
                                     event=event)
    if result == True:
        return redirect("public_engagement_monitoring:operator_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_structure_evaluation_operator
@is_editable_by_operator
def event_people_delete(request, structure_slug, event_id, person_id, event=None):
    result = management.event_people_delete(request=request,
                                            structure_slug=structure_slug,
                                            event_id=event_id,
                                            event=event,
                                            person_id=person_id,
                                            by_manager=True)
    if result == True:
        return redirect("public_engagement_monitoring:operator_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_structure_evaluation_operator
def event_evaluation(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.filter(pk=event_id,
                                                 structure__slug=structure_slug).first()

    if not event:
        messages.add_message(request, messages.DANGER, _("Access denied"))
        return redirect('public_engagement_monitoring:operator_events',
                        structure_slug=structure_slug)

    if not event.is_ready_for_evaluation():
        messages.add_message(request, messages.DANGER, _("Access denied"))
        return redirect('public_engagement_monitoring:operator_event',
                        structure_slug=structure_slug,
                        event_id=event_id)

    form = PublicEngagementEventEvaluationForm()
    template = 'pem/event_evaluation.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:operator_dashboard'): _('Structure operator'),
                   reverse('public_engagement_monitoring:operator_events', kwargs={'structure_slug': structure_slug}): structure_slug.upper(),
                   reverse('public_engagement_monitoring:operator_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                   '#': _('Evaluation')}

    if request.method == 'POST':
        form = PublicEngagementEventEvaluationForm(data=request.POST)
        if form.is_valid():
            event.operator_evaluation_date = timezone.now()
            event.operator_evaluation_success = form.cleaned_data['success']
            event.operator_evaluated_by = request.user
            event.operator_notes = form.cleaned_data['notes']
            event.modified_by = request.user
            event.save()

            log_result = "approvata" if form.cleaned_data['success'] else "rifiutata"
            msg = "[Operatore {}] Esito valutazione: {}".format(structure_slug, log_result)
            if not form.cleaned_data['success']:
                msg += ' {}'.format(event.operator_notes)

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg=msg)

            messages.add_message(request, messages.SUCCESS, _("Evaluation completed"))

            # email
            result = _('approved') if form.cleaned_data['success'] else _('not approved')
            subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('Evaluation completed'))
            body = "{} {} {}".format(request.user, _('has evaluated the event with the result'), result)
            send_email_to_event_referents(event, subject, body)

            if form.cleaned_data['success']:
                if event.data.patronage_requested:
                    send_email_to_patronage_operators(
                        event.structure, subject, body)
                else:
                    send_email_to_managers(subject, body)

            return redirect("public_engagement_monitoring:operator_event",
                            structure_slug=structure_slug,
                            event_id=event_id)
        else:
            messages.add_message(request, messages.ERROR,
                                 "<b>{}</b>: {}".format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs, 'event': event, 'form': form, 'structure_slug': structure_slug})


@login_required
@is_structure_evaluation_operator
def event_reopen_evaluation(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.filter(pk=event_id,
                                                 structure__slug=structure_slug).first()
    if not event:
        messages.add_message(request, messages.DANGER, _("Access denied"))
        return redirect('public_engagement_monitoring:operator_events',
                        structure_slug=structure_slug)

    if not event.evaluation_can_be_reviewed():
        messages.add_message(request, messages.DANGER, _("Access denied"))
        return redirect('public_engagement_monitoring:operator_event',
                        structure_slug=structure_slug,
                        event_id=event_id)

    event.operator_evaluation_date = None
    event.modified_by = request.user
    event.save()

    log_action(user=request.user,
               obj=event,
               flag=CHANGE,
               msg="[Operatore {}] Valutazione riaperta".format(structure_slug))

    messages.add_message(request, messages.SUCCESS, _("Evaluation reopened"))

    # email
    subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('evaluation reopened'))
    body = "{} {} {}".format(request.user, _('has reopened evaluation of the event'), '.')
    send_email_to_event_referents(event, subject, body)

    if event.data.patronage_requested:
        send_email_to_patronage_operators(event.structure, subject, body)
    else:
        send_email_to_managers(subject, body)

    return redirect("public_engagement_monitoring:operator_event",
                    structure_slug=structure_slug,
                    event_id=event_id)
