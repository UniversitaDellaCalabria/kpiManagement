from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from organizational_area.models import (OrganizationalStructure,
                                        OrganizationalStructureOfficeEmployee)

from . models import Detection
from . settings import DETECTION_OFFICE_SLUG


def can_manage_structure_detections(func_to_decorate):
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
                                       office__slug=DETECTION_OFFICE_SLUG,
                                       office__is_active=True,
                                       office__organizational_structure=structure)
        original_kwargs['structure'] = structure
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func


def structure_detection_is_accessible(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        detection = get_object_or_404(Detection,
                                      structure=original_kwargs['structure'],
                                      pk=original_kwargs['detection_pk'])
        if not detection.code.is_active:
            raise Exception(_("Detection code is disabled"))
        original_kwargs['detection'] = detection
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func
