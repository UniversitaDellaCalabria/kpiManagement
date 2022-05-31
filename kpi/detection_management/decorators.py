from django.shortcuts import get_object_or_404

from organizational_area.models import (OrganizationalStructure,
                                        OrganizationalStructureOfficeEmployee)

from . settings import DETECTION_OFFICE_SLUG


def can_manage_structure_detections(func_to_decorate):
    """
    """
    def new_func(*original_args, **original_kwargs):
        request = original_args[0]
        structure_slug = original_kwargs['structure_slug']
        if not structure_slug:
            raise Exception
        structure = get_object_or_404(OrganizationalStructure,
                                      slug=structure_slug,
                                      is_active=True)
        office = get_object_or_404(OrganizationalStructureOfficeEmployee,
                                   employee=request.user,
                                   office__slug=DETECTION_OFFICE_SLUG,
                                   office__is_active=True,
                                   office__organizational_structure=structure)
        original_kwargs['structure'] = structure
        return func_to_decorate(*original_args, **original_kwargs)

    return new_func
