from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

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
def dashboard(request, structure=None):
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
    years_query = Q()
    for year in active_years:
        years_query |= Q(start__year=year)
    event_counts = PublicEngagementEvent.objects.filter(
        years_query,
        structure__pk__in=structures
    ).values("structure__id").annotate(
        approved_count=Count("id", filter=Q(operator_evaluation_success=True,
                                            operator_evaluation_date__isnull=False)),
        created_by_manager_count=Count("id", filter=Q(created_by_manager=True)),
    )
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event_counts': event_counts,
                                      'structures': structures})


@login_required
@is_manager
def events(request, structure_slug, structure=None):
    template = 'pem/manager/events.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   '#': structure.name}
    api_url = reverse('public_engagement_monitoring:api_manager_events', kwargs={'structure_slug': structure_slug})
    return render(request, template, {'api_url': api_url,
                                      'breadcrumbs': breadcrumbs,
                                      'events': events,
                                      'structure_slug': structure_slug})


@login_required
@is_manager
def new_event_choose_referent(request, structure_slug, structure=None):
    request.session.pop('referent', None)
    template = 'pem/event_new.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): structure.name,
                   '#': _("New")}

    if request.method == 'POST':

        referent_id = requests.post('{}{}'.format(API_DECRYPTED_ID, '/'),
                                    data={
                                        'id': request.POST['referent_id']},
                                    headers={'Authorization': 'Token {}'.format(settings.STORAGE_TOKEN)})
        if referent_id.status_code != 200:
            messages.add_message(request, messages.ERROR, _("Access denied"))
            return redirect('public_engagement_monitoring:manager_new_event_choose_referent',
                            structure_slug=structure_slug)

        # recupero dati completi del referente (in entrambi i casi)
        # es: genere
        response = requests.get('{}{}'.format(API_ADDRESSBOOK_FULL, referent_id.json()),
                                headers={'Authorization': 'Token {}'.format(settings.STORAGE_TOKEN)})
        if response.status_code != 200:
            messages.add_message(request, messages.ERROR, _("Access denied"))
            return redirect('public_engagement_monitoring:manager_new_event_choose_referent',
                            structure_slug=structure_slug)

        referent_data = response.json()['results']
        if not referent_data.get('Email'):
            messages.add_message(request, messages.ERROR, _("The person selected does not have an email"))
            return redirect('public_engagement_monitoring:manager_new_event_choose_referent',
                            structure_slug=structure_slug)


        # creo o recupero l'utente dal db locale
        # controllo se esiste già (i dati locali potrebbero differire da quelli presenti nelle API)
        referent_user = get_user_model().objects.filter(
            codice_fiscale=referent_data['Taxpayer_ID']).first()
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
                                                            email=next(iter(referent_data['Email']), None),
                                                            gender=referent_data['Gender'])
        # se l'utente è stato disattivato
        if not referent_user.is_active:
            messages.add_message(request, messages.ERROR, _("Access denied"))
            return redirect('public_engagement_monitoring:manager_new_event_choose_referent',
                            structure_slug=structure_slug)

        # salviamo il referente corrente in sessione
        request.session['referent'] = referent_user.pk
        return redirect('public_engagement_monitoring:manager_new_event_basic_info',
                        structure_slug=structure_slug)

    return render(request, template, {'breadcrumbs': breadcrumbs})


@login_required
@is_manager
def new_event_basic_info(request, structure_slug, structure=None):
    # se non è stato scelto il referente nella fase iniziale
    if not request.session.get('referent'):
        messages.add_message(request, messages.ERROR, _("Event referent is mandatory"))
        return redirect('public_engagement_monitoring:manager_new_event_choose_referent',
                        structure_slug=structure_slug)

    template = 'pem/event_basic_info.html'
    form = PublicEngagementEventOperatorForm(
        request=request, structure_slug=structure_slug)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): structure.name,
                   reverse('public_engagement_monitoring:manager_new_event_choose_referent', kwargs={'structure_slug': structure_slug}): _('New'),
                   '#': _('General informations')}

    # post
    if request.method == 'POST':
        form = PublicEngagementEventOperatorForm(request=request,
                                         structure_slug=structure_slug,
                                         data=request.POST)
        if form.is_valid():

            year = form.cleaned_data['start'].year
            event = form.save(commit=False)

            # check sull'anno di inizio dell'evento
            # non valido per i manager!
            # if not PublicEngagementAnnualMonitoring.year_is_active(year):
                # messages.add_message(
                    # request, messages.ERROR, "<b>{}</b>: {} {}".format(_('Alert'), _('Monitoring activity year'), '{} {}'.format(year, _('has been disabled'))))
            if not event.is_over():
                messages.add_message(request,
                                     messages.ERROR, _("It is possible to add only ex-post events"))
            else:
                event.created_by = request.user
                event.modified_by = request.user
                event.referent = get_user_model().objects.get(
                    pk=request.session.get('referent'))
                event.created_by_manager = True
                event.save()

                log_action(user=request.user,
                           obj=event,
                           flag=ADDITION,
                           msg="[Operatore di Ateneo] Iniziativa creata")

                messages.add_message(
                    request, messages.SUCCESS, _("First step completed successfully. Now proceed to enter the data"))
                # elimino dalla sessione il referente scelto all'inizio
                request.session.pop('referent', None)
                return redirect('public_engagement_monitoring:manager_event',
                                structure_slug=structure_slug,
                                event_id=event.pk)
        else:  # pragma: no cover
            messages.add_message(request, messages.ERROR,
                                 "<b>{}</b>: {}".format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs, 'form': form})


@login_required
@is_manager
def event(request, structure_slug, event_id, structure=None):
    event = PublicEngagementEvent.objects.filter(pk=event_id,
                                                 structure__slug=structure_slug).first()

    if not event:
        return redirect('public_engagement_monitoring:manager_events', structure_slug=structure_slug)

    template = 'pem/manager/event.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): structure.name,
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
@is_editable_by_manager
def event_basic_info(request, structure_slug, event_id, event=None, structure=None):
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): structure.name,
                   reverse('public_engagement_monitoring:manager_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                   '#': _('General informations')}

    template = 'pem/event_basic_info.html'
    form = PublicEngagementEventOperatorForm(request=request,
                                             instance=event)
    # post
    if request.method == 'POST':
        form = PublicEngagementEventOperatorForm(request=request,
                                         instance=event,
                                         data=request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            if event.created_by_manager and not event.is_over():
                messages.add_message(request, messages.ERROR, _("It is possible to add only ex-post events"))
                return redirect("public_engagement_monitoring:manager_event",
                                structure_slug=structure_slug,
                                event_id=event_id)
            event.edited_by_manager = True
            event.modified_by = request.user
            event.save()

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg="[Operatore di Ateneo] Informazioni generali modificate")

            messages.add_message(request, messages.SUCCESS,
                                 _("Modified general informations successfully"))

            # invia email al referente/compilatore
            subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, _('Data modified'))
            body = '{} {} {}'.format(request.user, _('has modified the data of the event'), '.')

            send_email_to_event_referents(event, subject, body)

            # invia email agli operatori dipartimentali
            send_email_to_operators(event.structure, subject, body)

            return redirect("public_engagement_monitoring:manager_event",
                            structure_slug=structure_slug,
                            event_id=event_id)

        else:  # pragma: no cover
            messages.add_message(request, messages.ERROR,
                                 '<b>{}</b>: {}'.format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs, 'event': event, 'form': form})


@login_required
@is_manager
@is_editable_by_manager
def event_data(request, structure_slug, event_id, event=None, structure=None):
    result = management.event_data(request=request,
                                   structure_slug=structure_slug,
                                   event_id=event_id,
                                   event=event,
                                   by_manager=True,
                                   structure=structure)
    if result == True:
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_manager
@is_editable_by_manager
def event_people(request, structure_slug, event_id, event=None, structure=None):
    result = management.event_people(request=request,
                                     structure_slug=structure_slug,
                                     event_id=event_id,
                                     event=event,
                                     by_manager=True,
                                     structure=structure)
    if result == True:
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@require_POST
@is_manager
@is_editable_by_manager
def event_people_delete(request, structure_slug, event_id, person_id, event=None, structure=None):
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
@is_editable_by_manager
def event_structures(request, structure_slug, event_id, event=None, structure=None):
    result = management.event_structures(request=request,
                                         structure_slug=structure_slug,
                                         event_id=event_id,
                                         event=event,
                                         by_manager=True,
                                         structure=structure)
    if result == True:
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@require_POST
@is_manager
@is_editable_by_manager
def event_structures_delete(request, structure_slug, event_id, structure_id, event=None, structure=None):
    result = management.event_structures_delete(request=request,
                                                structure_slug=structure_slug,
                                                event_id=event_id,
                                                event=event,
                                                structure_id=structure_id,
                                                by_manager=True)
    if result == True:
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return result


@login_required
@is_manager
@has_report_editable_by_manager
def event_report(request, structure_slug, event_id, structure=None):
    template = 'pem/user/event_report.html'
    event = get_object_or_404(PublicEngagementEvent, pk=event_id, structure__slug=structure_slug)
    instance = PublicEngagementEventReport.objects.filter(event=event).first()
    form = PublicEngagementEventReportForm(instance=instance)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): structure.name,
                   reverse('public_engagement_monitoring:manager_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                   '#': _('Monitoring data')}

    if request.method == 'POST':
        form = PublicEngagementEventReportForm(instance=instance,
                                               data=request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.event = event
            report.modified_by = request.user
            if not instance:
                report.created_by = request.user
            report.edited_by_manager = True
            report.save()

            form.save_m2m()
            event.edited_by_manager = True
            event.modified_by = request.user
            event.save()

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg="[Operatore di Ateneo] Dati di monitoraggio modificati" if instance else "[Operatore di Ateneo] Dati di monitoraggio inseriti")

            messages.add_message(request, messages.SUCCESS, _('Monitoring data modified successfully'))
            return redirect("public_engagement_monitoring:manager_event",
                            structure_slug=structure_slug,
                            event_id=event_id)
        else:
            messages.add_message(request, messages.ERROR,
                                 "<b>{}</b>: {}".format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event': event,
                                      'form': form,
                                      'structure_slug': structure_slug})


@login_required
@is_manager
@is_manageable_by_manager
def event_enable_disable(request, structure_slug, event_id, event=None, structure=None):
    template = 'pem/manager/event_change_status.html'
    form = PublicEngagementEventDisableEnableForm()

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('public_engagement_monitoring:dashboard'): _('Public engagement'),
                   reverse('public_engagement_monitoring:manager_dashboard'): _('Manager'),
                   reverse('public_engagement_monitoring:manager_events', kwargs={'structure_slug': structure_slug}): structure.name,
                   reverse('public_engagement_monitoring:manager_event', kwargs={'event_id': event_id, 'structure_slug': structure_slug}): event.title,
                   '#': _('Change status')}

    if request.method == 'POST':
        form = PublicEngagementEventDisableEnableForm(data=request.POST)
        if form.is_valid():
            event.is_active = not event.is_active
            event.disabled_notes = form.cleaned_data['notes']
            event.modified_by = request.user
            event.save()

            # invia email agli operatori dipartimentali
            # invia email al referente/compilatore
            if not event.created_by_manager:
                event_status = _('Disabled') if not event.is_active else _('Enabled')
                subject = '{} - "{}" - {}'.format(_('Public engagement'), event.title, event_status)
                body = '{} {}.'.format(request.user, _('has changed the status of the event'))
                if not event.is_active:
                    body += "\n{}: {}".format(_('Notes'), event.disabled_notes)

                send_email_to_event_referents(event, subject, body)
                send_email_to_operators(event.structure, subject, body)
                for involved_structure in event.data.involved_structure.all():
                    send_email_to_operators(
                        involved_structure,
                        subject,
                        '{}: {}\n\n{}'.format(
                            _('Notification for operators of involved structure'),
                            involved_structure.name,
                            body
                        )
                    )
                send_email_to_managers(subject, body)

            log_action(user=request.user,
                       obj=event,
                       flag=CHANGE,
                       msg="[Operatore di Ateneo] Iniziativa riabilitata" if event.is_active else "[Operatore di Ateneo] Iniziativa disabilitata")

            messages.add_message(request, messages.SUCCESS, _('Event status modified successfully'))

            return redirect("public_engagement_monitoring:manager_event",
                            structure_slug=structure_slug,
                            event_id=event_id)
        else:
            messages.add_message(request, messages.ERROR,
                                 "<b>{}</b>: {}".format(_('Alert'), _('the errors in the form below need to be fixed')))
    return render(request, template, {'breadcrumbs': breadcrumbs,
                                      'event': event,
                                      'form': form,
                                      'structure_slug': structure_slug})
