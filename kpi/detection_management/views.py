from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from detection_management.decorators import can_manage_structure_detections
from detection_management.forms import DetectionForm
from detection_management.settings import *
from detection_management.models import Detection


@transaction.atomic
def _save_detection(structure, form):

    detection = form.save()
    detection.code = structure.name
    detection.save()

@login_required
@belongs_to_an_office
def dashboard(request):

    template = 'dashboard_detections.html'

    # get offices that I'm able to manage
    offices = OrganizationalStructureOfficeEmployee.objects\
                                                   .filter(employee=request.user,
                                                           office__slug=DETECTION_OFFICE_SLUG,
                                                           office__is_active=True,
                                                           office__organizational_structure__is_active=True)\
                                                   .select_related('office').order_by('office__name')
    d = {'my_offices': offices}


    return render(request, template, d)


@login_required
@can_manage_structure_detections
def structure_detections(request, structure_slug, structure=None):
    """
    param structure comes from @can_manage_structure_detections
    """
    d = {'structure': structure}
    template = 'detections.html'
    return render(request, template, d)


@login_required
@can_manage_structure_detections
def structure_detection(request, structure_slug, detection_pk, structure=None):
    """
    param structure comes from @can_manage_structure_detections
    """
    detection = get_object_or_404(Detection,
                                 Q(code=structure.name),
                                 pk=detection_pk,)

    d = {'detection': detection,
         'structure': structure}
    template = 'detection.html'
    return render(request, template, d)


@login_required
@can_manage_structure_detections
def new_structure_detection(request, structure_slug, structure=None):
    """
    param structure comes from @can_manage_structure_detections
    """
    form = DetectionForm(structure=structure)
    if request.POST:
        form.fields['code']=structure.name
        form = DetectionForm(request.POST, structure=structure)
        if form.is_valid():
            _save_detection(form=form, structure=structure)

            messages.add_message(request, messages.SUCCESS,
                                 _("Detection created"))
            return redirect('detection:structure_detections',
                            structure_slug=structure_slug)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'structure': structure}
    template = 'new_detection.html'
    return render(request, template, d)


@login_required
@can_manage_structure_detections
def edit_structure_detection(request, structure_slug, detection_pk, structure=None):
    """
    param structure comes from @can_manage_structure_detections
    """
    detection = get_object_or_404(Detection,
                                 Q(code=structure.name),
                                 pk=detection_pk,)
    form = DetectionForm(instance=detection,
                        structure=structure)
    if request.POST:
        form = DetectionForm(instance=detection,
                            structure=structure,
                            data=request.POST)
        if form.is_valid():

            _save_detection(form=form, structure=structure)

            messages.add_message(request, messages.SUCCESS,
                                 _("Detection edited"))
            return redirect('detection:structure_detections',
                            structure_slug=structure_slug)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'structure': structure,
         'detection': detection}
    template = 'edit_detection.html'
    return render(request, template, d)
