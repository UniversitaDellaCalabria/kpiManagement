import requests

from copy import deepcopy

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, redirect, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from organizational_area.models import *
from organizational_area.utils import user_in_office

from template.utils import *

from .. decorators.generic import *
from .. decorators.user import *
from .. forms import *
from .. models import *
from .. settings import *
from .. utils import *


@login_required
@can_manage_public_engagement
def events(request):
    template = 'pem/user/events.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   '#': _('Events')}
    api_url = request.build_absolute_uri(
        reverse('public_engagement_monitoring:api_user_events'))
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'api_url': api_url})


@login_required
def new_event_choose_referent(request):
    request.session.pop('referent', None)
    template = 'pem/event_new.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:user_events'): _('Events'),
                   '#': _('New')}

    if request.method == 'POST':
        user_is_referent = request.POST['user_is_referent']
        user_is_referent = True if user_is_referent == 'true' else False

        # se è il referente ma non è un docente
        if user_is_referent and not user_is_teacher(matricola=request.user.matricola_dipendente):
            return custom_message(request, _("Access denied"), 403)

        # se il referente non sono io, recupero la matricola in chiaro
        if not user_is_referent:
            referent_id = requests.post(f'{API_DECRYPTED_ID}/',
                                        data={
                                            'id': request.POST['referent_id']},
                                        headers={'Authorization': f'Token {settings.STORAGE_TOKEN}'})
            if referent_id.status_code != 200:
                return custom_message(request, _("Access denied"), 403)

        # recupero dati completi del referente (in entrambi i casi)
        # es: genere
        response = requests.get(f'{API_ADDRESSBOOK_FULL}{referent_id.json()}/',
                                headers={'Authorization': f'Token {settings.STORAGE_TOKEN}'})
        if response.status_code != 200:
            return custom_message(request, _("Access denied"), 403)

        referent_data = response.json()['results']
        if not referent_data.get('Email'):
            return custom_message(request, _("The person selected does not have an email"), 403)

        # creo o recupero l'utente dal db locale
        if not user_is_referent:
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
        return redirect('public_engagement_monitoring:user_new_event_basic_info')

    return render(request, template, {'breadcrumbs': breadcrumbs, 'compiled_by_user': True})


@login_required
@can_manage_public_engagement
def new_event_basic_info(request):
    # se non è stato scelto il referente nella fase iniziale
    if not request.session.get('referent'):
        return custom_message(request, _("Event referent is mandatory"), 403)

    template = 'pem/event_basic_info.html'
    form = PublicEngagementEventForm(request=request)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:user_events'): _('Events'),
                   reverse('public_engagement_monitoring:user_new_event_choose_referent'): _('New'),
                   '#': _('General informations'),}

    # post
    if request.method == 'POST':
        form = PublicEngagementEventForm(request=request, data=request.POST)
        if form.is_valid():

            year = form.cleaned_data['start'].year
            # check sull'anno di inizio dell'evento
            if not PublicEngagementAnnualMonitoring.year_is_active(year):
                messages.add_message(
                    request, messages.ERROR, f"<b>{_('Alert')}</b>: {_('Monitoring activity year')} {year} {_('has been disabled')}")
            else:
                event = form.save(commit=False)
                event.created_by = request.user
                event.modified_by = request.user
                event.referent = get_user_model().objects.get(
                    pk=request.session.get('referent'))
                event.save()

                log_action(user=request.user,
                           obj=event,
                           flag=ADDITION,
                           msg='Aggiunto')

                messages.add_message(
                    request, messages.SUCCESS, _("First step completed successfully. Now proceed to enter the data"))
                # elimino dalla sessione il referente scelto all'inizio
                request.session.pop('referent', None)
                return redirect('public_engagement_monitoring:user_event',
                                event_id=event.pk)
        else:  # pragma: no cover
            messages.add_message(request, messages.ERROR,
                                 f"<b>{_('Alert')}</b>: {_('the errors in the form below need to be fixed')}")
    return render(request, template, {'breadcrumbs': breadcrumbs, 'form': form})


@login_required
@has_access_to_my_event
def event(request, event_id, event=None):
    template = 'pem/user/event.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:user_events'): _('Events'),
                   '#': event.title}

    logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(event).pk,
                                   object_id=event.pk)

    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event': event,
                                      'logs': logs})


@login_required
@has_access_to_my_event
def event_basic_info(request, event_id, event=None):
    template = 'pem/event_basic_info.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:user_events'): _('Events'),
                   reverse('public_engagement_monitoring:user_event', kwargs={'event_id': event_id}): event.title,
                   '#': _('General informations'),}
    form = PublicEngagementEventForm(request=request, instance=event)

    if not event.is_editable_by_user():
        messages.add_message(
            request, messages.ERROR, _("It is no longer possible to change the general information of the event"))
        return redirect("public_engagement_monitoring:user_event",
                        event_id=event.pk)

    # post
    if request.method == 'POST':
        form = PublicEngagementEventForm(request=request,
                                         instance=event,
                                         data=request.POST)
        if form.is_valid():
            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg=_("data modified"))

            event = form.save(commit=False)
            event.modified_by = request.user
            event.save()
            messages.add_message(request, messages.SUCCESS,
                                 _("Modified general informations successfully"))
            return redirect("public_engagement_monitoring:user_event",
                            event_id=event.pk)
        else:  # pragma: no cover
            messages.add_message(request, messages.ERROR,
                                 f"<b>{_('Alert')}</b>: {_('the errors in the form below need to be fixed')}")
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event': event,
                                      'form': form})


@login_required
@has_access_to_my_event
@is_editable_by_user
def event_data(request, event_id, event=None):
    template = 'pem/event_data.html'
    instance = getattr(event, 'data', None)
    form = PublicEngagementEventDataForm(instance=instance)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:user_events'): _('Events'),
                   reverse('public_engagement_monitoring:user_event', kwargs={'event_id': event_id}): event.title,
                   '#': _("Event data")}

    if request.method == 'POST':

        form = PublicEngagementEventDataForm(instance=instance,
                                             data=request.POST,
                                             files=request.FILES)
        if form.is_valid():
            if not instance:
                log_action(user=request.user,
                           obj=event,
                           flag=CHANGE,
                           msg=_("Data inserted"))
            else:
                log_action(user=request.user,
                           obj=event,
                           flag=CHANGE,
                           msg=_("Data modified"))

            data = form.save(commit=False)
            data.event = event
            data.modified_by = request.user
            if not instance:
                data.created_by = request.user
            data.save()
            form.save_m2m()
            event.modified_by = request.user
            event.save()

            messages.add_message(request, messages.SUCCESS,
                                 _("Data updated successfully"))
            return redirect("public_engagement_monitoring:user_event",
                            event_id=event.pk)
        else:
            messages.add_message(request, messages.ERROR,
                                 f"<b>{_('Alert')}</b>: {_('the errors in the form below need to be fixed')}")
    return render(request, template, {'breadcrumbs': breadcrumbs, 'event': event, 'form': form})


@login_required
@has_access_to_my_event
@is_editable_by_user
def event_people(request, event_id, event=None):
    data = getattr(event, 'data', None)
    if not data:
        messages.add_message(request, messages.ERROR,
                             f"<b>{_('Alert')}</b>: {_('event data required')}")
        return redirect("public_engagement_monitoring:user_event",
                        event_id=event.pk)

    template = 'pem/event_people.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:user_events'): _('Events'),
                   reverse('public_engagement_monitoring:user_event', kwargs={'event_id': event_id}): event.title,
                   '#': _('Involved personnel')}

    if request.method == 'POST':
        # recupero dati completi del referente (in entrambi i casi)
        # es: genere
        person_id = request.POST.get('person_id')
        if not person_id:
            return custom_message(request, _("Access denied"), 403)
        decrypted_id = requests.post(f'{API_DECRYPTED_ID}/',
                                     data={'id': request.POST['person_id']},
                                     headers={'Authorization': f'Token {settings.STORAGE_TOKEN}'})
        response = requests.get(f'{API_ADDRESSBOOK_FULL}{decrypted_id.json()}/', headers={
                                'Authorization': f'Token {settings.STORAGE_TOKEN}'})
        if response.status_code != 200:
            return custom_message(request, _("Access denied"), 403)
        person_data = response.json()['results']
        person = get_user_model().objects.filter(
            codice_fiscale=person_data['Taxpayer_ID']).first()
        # aggiorno il dato sul genere (potrebbe non essere presente localmente)
        if person and not person.gender:
            person.gender = person_data['Gender']
            person.save(update_fields=['gender'])
        # se non esiste localmente lo creo
        if not person:
            person = get_user_model().objects.create(username=person_data['Taxpayer_ID'],
                                                     matricola_dipendente=person_data['ID'],
                                                     first_name=person_data['Name'],
                                                     last_name=person_data['Surname'],
                                                     codice_fiscale=person_data['Taxpayer_ID'],
                                                     email=person_data['Email'][0],
                                                     gender=person_data['Gender'])
        if data.person.filter(pk=person.pk).exists():
            messages.add_message(request, messages.ERROR,
                                 f"{person} {_('already exists')}")
        else:
            data.person.add(person)
            data.modified_by = request.user
            data.save()
            event.modified_by = request.user
            event.save()

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg=f'{_("added")} {person.first_name} {person.last_name} {_("in involved personnel")}')

            messages.add_message(request, messages.SUCCESS,
                                 f"{person} {_('addedd successfully')}")
        return redirect("public_engagement_monitoring:user_event",
                        event_id=event.pk)
    return render(request, template, {'breadcrumbs': breadcrumbs, 'event': event})


@login_required
@has_access_to_my_event
@is_editable_by_user
def event_people_delete(request, event_id, person_id, event=None):
    if not person_id:
        return custom_message(request, _("Access denied"), 403)
    person = event.data.person.filter(pk=person_id).first()
    if not person:
        messages.add_message(request, messages.ERROR, _('Personnel does not exist'))
    else:
        event.data.person.remove(person)
        event.data.modified_by = request.user
        event.data.save()
        event.modified_by = request.user
        event.save()

        log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg=f'{_("Removed")} {person.first_name} {person.last_name} {_("from involved personnel")}')

        messages.add_message(request, messages.SUCCESS,
                             _("Successfully removed"))
    return redirect("public_engagement_monitoring:user_event", event_id=event.pk)


@login_required
@has_access_to_my_event
@report_editable
def event_report(request, event_id, event=None):
    template = 'pem/user/event_report.html'
    instance = PublicEngagementEventReport.objects.filter(event=event).first()
    form = PublicEngagementEventReportForm(instance=instance, event=event)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:user_events'): _('Events'),
                   reverse('public_engagement_monitoring:user_event', kwargs={'event_id': event_id}): event.title,
                   '#': _('Monitoring data')}

    if request.method == 'POST':
        form = PublicEngagementEventReportForm(instance=instance,
                                               event=event,
                                               data=request.POST)
        if form.is_valid():

            report = form.save(commit=False)
            report.event = event
            report.modified_by = request.user
            if not instance:
                report.created_by = request.user
            report.save()
            form.save_m2m()
            event.modified_by = request.user
            event.save()

            if not instance:
                log_action(user=request.user,
                           obj=event,
                           flag=CHANGE,
                           msg=_('Monitoring data loaded'))
            else:
                changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                           form.changed_data)
                log_action(user=request.user,
                           obj=event,
                           flag=CHANGE,
                           msg=_('Monitoring data modified'))

            messages.add_message(request, messages.SUCCESS,
                                 _('Monitoring data modified successfully'))
            return redirect("public_engagement_monitoring:user_event",
                            event_id=event.pk)
        else:
            messages.add_message(request, messages.ERROR,
                                 f"<b>{_('Alert')}</b>: {_('the errors in the form below need to be fixed')}")
    return render(request, template, {'breadcrumbs': breadcrumbs, 'event': event, 'form': form})


@login_required
@has_access_to_my_event
def event_request_evaluation(request, event_id, event=None):
    if event.is_ready_for_request_evaluation():
        event.to_evaluate = True
        event.evaluation_request_date = timezone.now()
        event.evaluation_request_by = request.user
        event.modified_by = request.user
        event.save()

        log_action(user=request.user,
                   obj=event,
                   flag=CHANGE,
                   msg=_('Evaluation request sent'))

        messages.add_message(request, messages.SUCCESS,
                             _('Evaluation request sent'))

        # invia email agli operatori del dipartimento
        subject = f'{_("Public engagement")} - "{event.title}" - {_("Evaluation request sent")}'
        body = f"{request.user} {_('requested the evaluation of the event')}. {_('Click here')}: {request.build_absolute_uri(reverse('public_engagement_monitoring:operator_event', kwargs={'structure_slug': event.structure.slug, 'event_id': event.pk}))}"
        send_email_to_operators(structure=event.structure,
                                subject=subject,
                                body=body)
    else:
        messages.add_message(request, messages.ERROR,
                             f"<b>{_('Alert')}</b>: {_('evaluation conditions are not satisfied')}")
    return redirect("public_engagement_monitoring:user_event",
                    event_id=event.pk)


@login_required
@has_access_to_my_event
def event_request_evaluation_cancel(request, event_id, event=None):
    if not event.can_user_cancel_evaluation_request():
        return custom_message(request, _("Access denied"), 403)

    event.to_evaluate = False
    event.modified_by = request.user
    event.save()

    log_action(user=request.user,
                   obj=event,
                   flag=CHANGE,
                   msg=_('Evaluation request cancelled'))

    messages.add_message(request, messages.SUCCESS,
                         _('Evaluation request cancelled'))

    # invia email agli operatori del dipartimento
    subject = f'{_("Public engagement")} - "{event.title}" - {_("Evaluation request cancelled")}'
    body = f"{request.user} {_('has cancelled the evaluation request')}"
    send_email_to_operators(structure=event.structure,
                            subject=subject,
                            body=body)

    return redirect("public_engagement_monitoring:user_event",
                    event_id=event.pk)


@login_required
@has_access_to_my_event
def event_clone(request, event_id, event=None):
    new_event = PublicEngagementEvent.objects.create(
        title=event.title,
        start=event.start,
        end=event.end,
        referent=event.referent,
        structure=event.structure,
        created_by=request.user,
        modified_by=request.user,
        created=timezone.now(),
        modified=timezone.now()
    )
    new_data = deepcopy(event.data)
    new_data.pk = None
    new_data.event = new_event
    new_data.created = timezone.now()
    new_data.modified = timezone.now()
    new_data.created_by = request.user
    new_data.modified_by = request.user
    new_data.save()

    new_data.person.set(event.data.person.all())
    new_data.recipient.set(event.data.recipient.all())
    new_data.target.set(event.data.target.all())
    new_data.promo_channel.set(event.data.promo_channel.all())
    new_data.promo_tool.set(event.data.promo_tool.all())

    messages.add_message(request, messages.SUCCESS,
                         f"{_('Event')} {event.title} {_('duplicated')}")
    return redirect("public_engagement_monitoring:user_event", event_id=new_event.pk)


@login_required
@has_access_to_my_event
def event_delete(request, event_id, event=None):
    if event.to_evaluate:
        return custom_message(request, _("Access denied"), 403)

    messages.add_message(request, messages.SUCCESS,
                         f"{_('Event')} {event.title} {_('removed')}")
    event.delete()
    return redirect("public_engagement_monitoring:user_events")
