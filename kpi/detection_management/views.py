from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from detection_management.decorators import *
from detection_management.forms import DetectionForm
from detection_management.settings import *
from detection_management.models import *

from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from template.utils import log_action


@transaction.atomic
def _save_detection(structure, form, **kwargs):

    detection = form.save(commit=False)
    detection.structure = structure
    detection.value = round(detection.num / detection.den, 2)

    # additional fields
    for k, v in kwargs.items():
        setattr(detection, k, v)

    detection.save()
    return detection


@login_required
@belongs_to_an_office
def dashboard(request):

    template = 'dashboard_detections.html'

    if request.user.is_superuser:
        offices = OrganizationalStructureOffice.objects\
                                               .filter(slug=DETECTION_OFFICE_SLUG,
                                                       is_active=True,
                                                       organizational_structure__is_active=True)
    else:
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
    codes = DetectionCode.objects.filter(is_active=True)
    d = {'codes': codes,
         'structure': structure}
    template = 'detections.html'
    return render(request, template, d)


@login_required
@can_manage_structure_detections
@structure_detection_is_accessible
def structure_detection(request, structure_slug, detection_pk,
                        structure=None, detection=None):
    """
    param structure comes from @can_manage_structure_detections
    param detection comes from @structure_detection_is_accessible
    """
    detection_logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(detection).pk,
                                             object_id=detection.pk)

    d = {'detection': detection,
         'detection_logs': detection_logs,
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
            detection = _save_detection(form=form,
                                        structure=structure,
                                        created_by=request.user)

            log_action(user=request.user,
                       obj=detection,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request, messages.SUCCESS,
                                 _("Enabling factor created"))
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
@structure_detection_is_accessible
def edit_structure_detection(request, structure_slug, detection_pk,
                             structure=None, detection=None):
    """
    param structure comes from @can_manage_structure_detections
    param detection comes from @structure_detection_is_accessible
    """
    detection = get_object_or_404(Detection,
                                  structure=structure,
                                  pk=detection_pk,)
    form = DetectionForm(instance=detection,
                         structure=structure)

    if request.POST:
        form = DetectionForm(instance=detection,
                             structure=structure,
                             data=request.POST)

        changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                   form.changed_data)

        if form.is_valid():

            _save_detection(form=form,
                            structure=structure,
                            modified_by=request.user)

            log_action(user=request.user,
                       obj=detection,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request, messages.SUCCESS,
                                 _("Enabling factor edited"))
            return redirect('detection:structure_detection',
                            structure_slug=structure_slug,
                            detection_pk=detection.pk)

        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'structure': structure,
         'detection': detection}
    template = 'edit_detection.html'
    return render(request, template, d)
