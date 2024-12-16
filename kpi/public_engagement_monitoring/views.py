import csv
import datetime
import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from template.utils import *

from . decorators import *
from . forms import *
from . models import *
from . settings import *
from . utils import *


@login_required
def dashboard(request):
    template = 'public_engagement_monitoring_dashboard.html'
    return render(request, template, {})


@login_required
@can_view_events
def user_dashboard(request):
    template = 'public_engagement_monitoring_user_dashboard.html'
    events = PublicEngagementEvent.objects.filter(Q(referent=request.user) | Q(created_by=request.user))
    return render(request, template, {'events': events})


@login_required
def new(request):
    template = 'public_engagement_monitoring_new.html'

    if request.method == 'POST':
        user_is_referent = request.POST['user_is_referent']
        user_is_referent = True if user_is_referent == 'true' else False

        # se non è il referente e non è abilitato
        if not user_is_referent and not check_user_linked_to_office(request.user, [VALIDATOR_INTERMIDIATE, VALIDATOR_FINAL]):
            raise PermissionDenied()

        # se è il referente ma non è un docente
        if user_is_referent and not user_is_teacher(matricola=request.user.matricola_dipendente):
            raise PermissionDenied()

        # se il referente non sono io, recupero la matricola in chiaro
        if not user_is_referent:
            referent_id = requests.post(f'{API_DECRYPTED_ID}/',
                                        data={'id': request.POST['referent_id']},
                                        headers={'Authorization': f'Token {settings.STORAGE_TOKEN}'})

            if referent_id.status_code != 200:
                raise PermissionDenied()

        # recupero dati completi del referente (in entrambi i casi)
        # es: genere
        response = requests.get(f'{API_ADDRESSBOOK_FULL}{referent_id.json()}/', headers={'Authorization': f'Token {settings.STORAGE_TOKEN}'})
        if response.status_code != 200:
            raise PermissionDenied()

        referent_data = response.json()['results']

        # creo o recupero l'utente dal db locale
        if not user_is_referent:
            referent_user = get_user_model().objects.get_or_create(username=referent_data['Taxpayer_ID'],
                                                                   matricola_dipendente=referent_data['ID'],
                                                                   first_name=referent_data['Name'],
                                                                   last_name=referent_data['Surname'],
                                                                   codice_fiscale=referent_data['Taxpayer_ID'],
                                                                   email=referent_data['Email'][0],
                                                                   gender=referent_data['Gender'])[0]
            # se l'utente è stato disattivato
            if not referent_user.is_active:
                raise PermissionDenied()

        # salviamo il referente corrente in sessione
        request.session['referente'] = referent_user.pk
        return redirect('public_engagement_monitoring:new_step_1')

    return render(request, template, {})


@login_required
def new_step_1(request):
    # se non è stato scelto il referente nella fase iniziale
    if not request.session.get('referente'): raise PermissionDenied()

    template = 'public_engagement_monitoring_new_step_1.html'
    form = PublicEngagementEventForm(request=request)

    # post
    if request.method == 'POST':
        form = PublicEngagementEventForm(request=request, data=request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            structure = form.cleaned_data['referent_organizational_structure']

            referent = get_user_model().objects.get(pk=request.session.get('referente'))
            event = PublicEngagementEvent.objects.create(created_by=request.user,
                                                         modified_by=request.user,
                                                         title=title,
                                                         start=start,
                                                         end=end,
                                                         referent=referent,
                                                         referent_organizational_structure=structure)

            messages.add_message(request, messages.SUCCESS, "Primo step completato con successo. Ora procedi all'inserimento dei dati")
            # elimino dalla sessione il referente scelto all'inizio
            del request.session['referente']
            return redirect('public_engagement_monitoring:event_fase1')
        else:  # pragma: no cover
            messages.add_message(request, messages.ERROR,
                                 f"<b>Attenzione</b>: correggli gli errori nel form")
    return render(request, template, {'form': form})


@login_required
def event(request, event_id):
    template = 'public_engagement_monitoring_event.html'
    event = get_object_or_404(PublicEngagementEvent, pk=pk)
    return render(request, template, {'event': event})


@login_required
@can_view_and_edit_event
def event(request, event_id, event=None):
    template = 'public_engagement_monitoring_event.html'
    return render(request, template, {'event': event})


@login_required
@can_view_and_edit_event
@check_year
def event_fase1(request, event_id, event=None):
    template = 'public_engagement_monitoring_event_fase1.html'
    instance = PublicEngagementEventData.objects.filter(event=event).first()
    form = PublicEngagementEventDataForm(instance=instance)
    if request.method == 'POST':
        form = PublicEngagementEventDataForm(instance=instance,
                                             data=request.POST)
        if form.is_valid():
            fase1 = form.save(commit=False)
            fase1.event = event
            fase1.modified_by = request.user
            if not instance:
                fase1.created_by = request.user
            fase1.save()
            form.save_m2m()
            messages.add_message(request, messages.SUCCESS, "Dati aggiornati con successo")
            return redirect("public_engagement_monitoring:event", event_id=event.pk)
        else:
            messages.add_message(request, messages.ERROR,
                                 f"<b>Attenzione</b>: correggli gli errori nel form")
    return render(request, template, {'event': event, 'form': form})


