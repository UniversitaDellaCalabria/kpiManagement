from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from organizational_area.models import *

from .. models import *
from .. settings import *
from .. utils import *


def is_manager(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        if user_is_manager(request.user):
            return func_to_decorate(*original_args, **original_kwargs)
        messages.add_message(request, messages.DANGER, _('Access denied'))
        return redirect("public_engagement_monitoring:dashboard")
    return new_func


def is_editable_by_manager(func_to_decorate):
    """
    controlla che l'attuale stato dell'evento
    renda editabile dall'utente i dati
    tutti i controlli sui permessi dell'utente vengono fatti da
    altri decoratori
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        event_id = original_kwargs['event_id']
        event = get_object_or_404(PublicEngagementEvent, pk=event_id)
        if event.is_editable_by_manager():
            original_kwargs['event'] = event
            return func_to_decorate(*original_args, **original_kwargs)
        messages.add_message(request, messages.DANGER, _('Access denied'))
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=structure_slug,
                        event_id=event_id)
    return new_func


def has_report_editable_by_manager(func_to_decorate):
    """
    controlla che l'attuale stato dell'evento
    renda editabile dall'utente il report
    tutti i controlli sui permessi dell'utente vengono fatti da
    altri decoratori
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        event = original_kwargs.get('event') or get_object_or_404(PublicEngagementEvent, pk=original_kwargs['event_id'])
        if event.has_report_editable_by_manager():
            return func_to_decorate(*original_args, **original_kwargs)
        messages.add_message(request, messages.DANGER, _('Access denied'))
        return redirect("public_engagement_monitoring:manager_event",
                        structure_slug=original_kwargs['structure_slug'],
                        event_id=original_kwargs['event_id'])
    return new_func
