from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from organizational_area.models import *

from . models import *
from . settings import *
from . utils import user_is_teacher


def can_view_events(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        if user_is_teacher(request.user.matricola_dipendente):
            return func_to_decorate(*original_args, **original_kwargs)
        user_is_in_valid_office = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                                       office__is_active=True,
                                                                                       office__organizational_structure__is_active=True,
                                                                                       office__slug__in=[VALIDATOR_INTERMIDIATE,
                                                                                                         VALIDATOR_FINAL]).exists()
        if user_is_in_valid_office:
            return func_to_decorate(*original_args, **original_kwargs)
        raise PermissionDenied()
    return new_func


def can_view_and_edit_event(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        event_id = original_kwargs['event_id']
        event = get_object_or_404(PublicEngagementEvent, pk=event_id)
        original_kwargs['event'] = event

        # se sono il referente dell'evento
        if event.referent == request.user:
            return func_to_decorate(*original_args, **original_kwargs)

        # se sono un validatore di ateneo
        is_manager = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                          office__is_active=True,
                                                                          office__organizational_structure__is_active=True,
                                                                          office__slug=VALIDATOR_FINAL).exists()
        if is_manager:
            return func_to_decorate(*original_args, **original_kwargs)

        # se sono un validatore di struttura e la struttura dell'evento è la mia
        is_operator = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                           office__is_active=True,
                                                                           office__organizational_structure__is_active=True,
                                                                           office__organizational_structure=event.referent_organizational_structure,
                                                                           office__slug=VALIDATOR_INTERMIDIATE).exists()
        if is_operator:
            return func_to_decorate(*original_args, **original_kwargs)

        raise PermissionDenied()
    return new_func


def check_year(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        event = original_kwargs['event']
        # controllo sugli anni per cui l'attività è abilitata
        active_years = PublicEngagementAnnualMonitoring.objects.filter(is_active=True).values_list('year', flat=True)
        if event.start.year not in active_years:
            raise PermissionDenied()
        return func_to_decorate(*original_args, **original_kwargs)
    return new_func
