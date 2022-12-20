from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from organizational_area.models import (OrganizationalStructure,
                                        OrganizationalStructureOfficeEmployee)

from template.utils import check_user_permission_on_model

from . models import Visiting
from . settings import VISITING_OFFICE_SLUG


def can_view_structure_visitings(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        structure_slug = original_kwargs['structure_slug']
        if not structure_slug:
            raise Exception(_("Structure slug missing"))
        structure = get_object_or_404(OrganizationalStructure,
                                      slug=structure_slug,
                                      is_active=True)
        if not request.user.is_superuser and not check_user_permission_on_model(request.user, Visiting):
            office = get_object_or_404(OrganizationalStructureOfficeEmployee,
                                       employee=request.user,
                                       office__slug=VISITING_OFFICE_SLUG,
                                       office__is_active=True,
                                       office__organizational_structure=structure)
        original_kwargs['structure'] = structure
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def can_manage_structure_visitings(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]



        structure_slug = original_kwargs['structure_slug']
        if not structure_slug:
            raise Exception(_("Structure slug missing"))
        structure = get_object_or_404(OrganizationalStructure,
                                      slug=structure_slug,
                                      is_active=True)
        if not request.user.is_superuser:
            office = get_object_or_404(OrganizationalStructureOfficeEmployee,
                                       employee=request.user,
                                       office__slug=VISITING_OFFICE_SLUG,
                                       office__is_active=True,
                                       office__organizational_structure=structure)
        original_kwargs['structure'] = structure
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func
