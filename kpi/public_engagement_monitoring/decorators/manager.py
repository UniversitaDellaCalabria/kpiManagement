from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from organizational_area.models import *

from template.utils import custom_message

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
        return custom_message(request, _("Access denied"), 403)
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
        return custom_message(request, _("Access denied"), 403)
    return new_func
