from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from organizational_area.models import *

from template.utils import *

from .. decorators.generic import *
from .. decorators.manager import *
from .. forms import *
from .. models import *
from .. settings import *
from .. utils import *

from public_engagement_monitoring.views import management


@login_required
@is_manager
def dashboard(request):
    template = 'pem/manager/dashboard.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   '#': _('Manager')}
    structures = OrganizationalStructure.objects.filter(is_active=True,
                                                        is_public_engagement_enabled=True,
                                                        is_internal=True)
    active_years = PublicEngagementAnnualMonitoring.objects\
                                                   .filter(is_active=True)\
                                                   .values_list('year', flat=True)
    events_per_structure = {}
    for structure in structures:
        to_evaluate = PublicEngagementEventData.objects.filter(Q(
            patronage_requested=True,
            event__patronage_granted=True
        ) |
            Q(patronage_requested=False),
            event__structure=structure,
            event__start__year__in=active_years,
            event__to_evaluate=True,
            event__operator_evaluation_success=True,
            event__manager_taken_date__isnull=True).count()
        events_per_structure[structure] = to_evaluate
    return render(request,
                  template,
                  {'breadcrumbs': breadcrumbs,
                   'events_per_structure': events_per_structure})


@login_required
@is_manager
def events(request, structure_slug):
    template = 'pem/manager/events.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   '#': '{}'.format(structure_slug)}
    api_url = reverse('public_engagement_monitoring:api_manager_events', kwargs={'structure_slug': structure_slug})
    return render(request, template, {'api_url': api_url,
                                      'breadcrumbs': breadcrumbs,
                                      'events': events,
                                      'structure_slug': structure_slug})


@login_required
@is_manager
def new_event_choose_referent(request, structure_slug):
    request.session.pop('referent', None)
    template = 'pem/event_new.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                   '#': _("New")}

    if request.method == 'POST':

        referent_id = requests.post('{}{}'.format(API_DECRYPTED_ID, '/'),
                                    data={
                                        'id': request.POST['referent_id']},
                                    headers={'Authorization': 'Token {}'.format(settings.STORAGE_TOKEN)})
        if referent_id.status_code != 200:
            return custom_message(request, _("Access denied"), 403)

        # recupero dati completi del referente (in entrambi i casi)
        # es: genere
        response = requests.get('{}{}'.format(API_ADDRESSBOOK_FULL, referent_id.json()),
                                headers={'Authorization': 'Token {}'.format(settings.STORAGE_TOKEN)})
        if response.status_code != 200:
            return custom_message(request, _("Access denied"), 403)

        referent_data = response.json()['results']
        if not referent_data.get('Email'):
            return custom_message(request, _("The person selected does not have an email"), 403)


        # creo o recupero l'utente dal db locale
        # controllo se esiste già (i dati locali potrebbero differire da quelli presenti nelle API)
        referent_user = get_user_model().objects.filter(
            username=referent_data['Taxpayer_ID']).first()
        # aggiorno il dato sul genere (potrebbe non essere presente localmente)
        if referent_user and not referent_user.gender:
            referent_user.gender = referent_data['Gender']
            referent_user.save(update_fields=['gender'])
        # se non esiste localmente lo creo
        if not referent_user:
            referent_user = get_user_model().objects.create(username=referent_data['Taxpayer_ID'],
                                                            matricola_dipendente=referent_data['ID'],
                                                            first_name=referent_data['Name'],
                                                            last_name=referent_data['Surname'],
                                                            codice_fiscale=referent_data['Taxpayer_ID'],
                                                            email=referent_data['Email'][0],
                                                            gender=referent_data['Gender'])
        # se l'utente è stato disattivato
        if not referent_user.is_active:
            return custom_message(request, _("Access denied"), 403)

        # salviamo il referente corrente in sessione
        request.session['referent'] = referent_user.pk
        return redirect('public_engagement_monitoring:manager_new_event_basic_info',
                        structure_slug=structure_slug)

    return render(request, template, {'breadcrumbs': breadcrumbs})


@login_required
@is_manager
def new_event_basic_info(request, structure_slug):
    # se non è stato scelto il referente nella fase iniziale
    if not request.session.get('referent'):
        return custom_message(request, _("Event referent is mandatory"), 403)

    template = 'pem/event_basic_info.html'
    form = PublicEngagementEventOperatorForm(
        request=request, structure_slug=structure_slug)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                   reverse('public_engagement_monitoring:manager_new_event_choose_referent', kwargs={'structure_slug': structure_slug}): _('New'),
                   '#': _('General informations')}

    # post
    if request.method == 'POST':
        form = PublicEngagementEventOperatorForm(request=request,
                                         structure_slug=structure_slug,
                                         data=request.POST)
        if form.is_valid():

            year = form.cleaned_data['start'].year
            # check sull'anno di inizio dell'evento
            if not PublicEngagementAnnualMonitoring.year_is_active(year):
                messages.add_message(
                    request, messages.ERROR, "<b>{}</b>: {} {}".format(_('Alert'), _('Monitoring activity year'), '{} {}'.format(year, _('has been disabled'))))
            else:
                event = form.save(commit=False)
                event.created_by = request.user
                event.modified_by = request.user
                event.referent = get_user_model().objects.get(
                    pk=request.session.get('referent'))
                event.to_evaluate = True
                event.operator_evaluation_success = True
                event.manager_taken_date = timezone.now()
                event.manager_taken_by = request.user
                event.save()

                log_action(user=request.user,
                           obj=event,
                           flag=ADDITION,
                           msg='{}: {}'.format(structure_slug, _('added')))

                messages.add_message(
                    request, messages.SUCCESS, _("First step completed successfully. Now proceed to enter the data"))
                # elimino dalla sessione il referente scelto all'inizio
                request.session.pop('referent', None)
                return redirect('public_engagement_monitoring:manager_event',
                                structure_slug=structure_slug,
                                event_id=event.pk)
        else:  # pragma: no cover
            messages.add_message(request, messages.ERROR,
                                 "<b>{}</b>: {} {}".format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs, 'form': form})


@login_required
@is_manager
def event(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.filter(pk=event_id,
                                                 structure__slug=structure_slug).first()

    if not event:
        return redirect('public_engagement_monitoring:manager_events', structure_slug=structure_slug)

    template = 'pem/manager/event.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                   '#': event.title}

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(event).pk,
                                   object_id=event.pk)

    return render(request,
                  template,
                  {'breadcrumbs': breadcrumbs,
                   'event': event,
                   'logs': logs,
                   'structure_slug': structure_slug})


@login_required
@is_manager
def take_event(request, structure_slug, event_id):
    event = get_object_or_404(PublicEngagementEvent,
                              pk=event_id, structure__slug=structure_slug)
    if not event.can_be_taken_by_manager():
        return custom_message(request, _("Access denied"), 403)
    event.manager_taken_by = request.user
    event.manager_taken_date = timezone.now()
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
    body = "{} {}".format(request.user, _('is evaluating the event'))
    send_email_to_event_referents(event, subject, body)

    # invia email agli operatori dipartimentali
    send_email_to_operators(event.structure, subject, body)

    return redirect('public_engagement_monitoring:manager_event',
                    structure_slug=structure_slug,
                    event_id=event_id)


@login_required
@is_manager
@is_editable_by_manager
def event_basic_info(request, structure_slug, event_id, event=None):
    result = management.event_basic_info(request=request,
                                         structure_slug=structure_slug,
                                         event_id=event_id,
                                         event=event,
                                         by_manager=True)
    if result == True:
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_manager
@is_editable_by_manager
def event_data(request, structure_slug, event_id, event=None):
    result = management.event_data(request=request,
                                   structure_slug=structure_slug,
                                   event_id=event_id,
                                   event=event,
                                   by_manager=True)
    if result == True:
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_manager
@is_editable_by_manager
def event_people(request, structure_slug, event_id, event=None):
    result = management.event_people(request=request,
                                     structure_slug=structure_slug,
                                     event_id=event_id,
                                     event=event,
                                     by_manager=True)
    if result == True:
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_manager
@is_editable_by_manager
def event_people_delete(request, structure_slug, event_id, person_id, event=None):
    result = management.event_people_delete(request=request,
                                            structure_slug=structure_slug,
                                            event_id=event_id,
                                            event=event,
                                            person_id=person_id,
                                            by_manager=True)
    if result == True:
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_manager
def event_evaluation(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.filter(pk=event_id,
                                                 structure__slug=structure_slug).first()
    if not event:
        return custom_message(request, _("Access denied"), 403)

    if not event.is_ready_for_manager_evaluation():
        return custom_message(request, _("Access denied"), 403)

    form = PublicEngagementEventEvaluationForm()
    template = 'pem/event_evaluation.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): '{}'.format(structure_slug),
                   reverse('public_engagement_monitoring:manager_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                   '#': _('Evaluation')}

    if request.method == 'POST':
        form = PublicEngagementEventEvaluationForm(data=request.POST)
        if form.is_valid():
            event.manager_evaluation_date = timezone.now()
            event.manager_evaluation_success = form.cleaned_data['success']
            event.manager_evaluated_by = request.user
            event.manager_notes = form.cleaned_data['notes']
            event.modified_by = request.user
            event.save()

            result = _('approved') if form.cleaned_data['success'] else _('not approved')
            msg = '{} - {}: {}'.format(structure_slug, _('evaluation completed'), result)
            if not form.cleaned_data['success']:
                msg += ' {}'.format(operator_notes)

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg=msg)

            messages.add_message(request, messages.SUCCESS, _("Evaluation completed"))

            # invia email al referente/compilatore
            subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('Evaluation completed'))
            body = "{} {}: {}".format(request.user, _('has evaluated the event with the result'), result)
            send_email_to_event_referents(event, subject, body)

            # invia email agli operatori dipartimentali
            send_email_to_operators(event.structure, subject, body)

            return redirect("public_engagement_monitoring:manager_event",
                            structure_slug=structure_slug,
                            event_id=event_id)
        else:
            messages.add_message(request, messages.ERROR,
                                 "<b>{}</b>: {} {}".format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs, 'event': event, 'form': form, 'structure_slug': structure_slug})


@login_required
@is_manager
def event_reopen_evaluation(request, structure_slug, event_id):
    event = PublicEngagementEvent.objects.filter(pk=event_id,
                                                 structure__slug=structure_slug).first()
    if not event:
        return custom_message(request, _("Access denied"), 403)

    if not event.can_manager_cancel_evaluation():
        return custom_message(request, _("Access denied"), 403)

    event.manager_evaluation_date = None
    event.modified_by = request.user
    event.save()

    log_action(user=request.user,
               obj=event,
               flag=CHANGE,
               msg='{}: {}'.format(structure_slug, _('evaluation reopened')))

    messages.add_message(request, messages.SUCCESS, _("Evaluation reopened"))

    # invia email al referente/compilatore
    subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('evaluation reopened'))
    body = "{} {}.".format(request.user, _('has reopened evaluation of the event'))
    send_email_to_event_referents(event, subject, body)

    # invia email agli operatori dipartimentali
    send_email_to_operators(event.structure, subject, body)

    return redirect("public_engagement_monitoring:manager_event",
                    structure_slug=structure_slug,
                    event_id=event_id)
