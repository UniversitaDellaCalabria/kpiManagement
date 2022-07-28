from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext_lazy as _

from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from template.utils import log_action

from . decorators import can_manage_structure_visitings
from . forms import VisitingForm
from . settings import *
from . models import Visiting, VisitingCollaboration


@transaction.atomic
def _save_visiting(structure, form, **kwargs):
    """
    Save visiting from form.
    Passing additional fields in kwargs.
    """
    visiting = form.save()

    visiting.mission = form.cleaned_data['to_structure'] != structure
    # update_fields = ['mission']

    # additional fields
    for k, v in kwargs.items():
        setattr(visiting, k, v)
        # update_fields.append(k)

    # visiting.save(update_fields=update_fields)
    visiting.save()

    # set new collaborations
    VisitingCollaboration.objects.filter(visiting=visiting).delete()
    collabs = form.cleaned_data['collab']
    for collab in collabs:
        VisitingCollaboration.objects.create(visiting=visiting,
                                             collab=collab)
    return visiting


@login_required
@belongs_to_an_office
def dashboard(request):

    template = 'dashboard_visitings.html'
    if request.user.is_superuser:
        offices = OrganizationalStructureOffice.objects\
                                               .filter(slug=VISITING_OFFICE_SLUG,
                                                       is_active=True,
                                                       organizational_structure__is_active=True)
    else:
        # get offices that I'm able to manage
        my_offices = OrganizationalStructureOfficeEmployee.objects\
                                                          .filter(employee=request.user,
                                                                  office__slug=VISITING_OFFICE_SLUG,
                                                                  office__is_active=True,
                                                                  office__organizational_structure__is_active=True)\
                                                          .select_related('office')
        offices = []
        for off in my_offices:
            offices.append(off.office)

    result = []
    for off in offices:
        visiting_out = Visiting.objects.filter(
            from_structure=off.organizational_structure).count()
        visiting_in = Visiting.objects.filter(
            to_structure=off.organizational_structure).count()
        result.append({'office': off,
                       'visiting_in': visiting_in,
                       'visiting_out': visiting_out})

    d = {'my_offices': result}

    return render(request, template, d)


@login_required
@can_manage_structure_visitings
def structure_visitings(request, structure_slug, structure=None):
    """
    param structure comes from @can_manage_structure_visitings
    """
    d = {'structure': structure}
    template = 'visitings.html'
    return render(request, template, d)


@login_required
@can_manage_structure_visitings
def structure_visiting(request, structure_slug, visiting_pk, structure=None):
    """
    param structure comes from @can_manage_structure_visitings
    """
    visiting = get_object_or_404(Visiting,
                                 Q(from_structure=structure) |
                                 Q(to_structure=structure),
                                 pk=visiting_pk,)

    collaborations = VisitingCollaboration.objects.filter(visiting=visiting)

    visiting_logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(visiting).pk,
                                            object_id=visiting.pk)

    d = {'collaborations': collaborations,
         'visiting_logs': visiting_logs,
         'visiting': visiting,
         'structure': structure}
    template = 'visiting.html'
    return render(request, template, d)


@login_required
@can_manage_structure_visitings
def new_structure_visiting(request, structure_slug, structure=None):
    """
    param structure comes from @can_manage_structure_visitings
    """
    form = VisitingForm(structure=structure)
    if request.POST:
        form = VisitingForm(request.POST, structure=structure)
        if form.is_valid():

            visiting = _save_visiting(form=form,
                                      structure=structure,
                                      created_by=request.user)

            log_action(user=request.user,
                       obj=visiting,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request, messages.SUCCESS,
                                 _("Visiting created"))
            return redirect('visiting:structure_visitings',
                            structure_slug=structure_slug)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'structure': structure}
    template = 'new_visiting.html'
    return render(request, template, d)


@login_required
@can_manage_structure_visitings
def edit_structure_visiting(request, structure_slug, visiting_pk, structure=None):
    """
    param structure comes from @can_manage_structure_visitings
    """
    visiting = get_object_or_404(Visiting,
                                 Q(from_structure=structure) |
                                 Q(to_structure=structure),
                                 pk=visiting_pk,)
    collaborations = VisitingCollaboration.objects.filter(
        visiting=visiting).values_list('collab', flat=True)
    form = VisitingForm(instance=visiting,
                        initial={'collab': collaborations},
                        structure=structure)
    if request.POST:
        form = VisitingForm(instance=visiting,
                            initial={'collab': collaborations},
                            structure=structure,
                            data=request.POST)
        changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                   form.changed_data)
        if form.is_valid():
            visiting = _save_visiting(form=form,
                                      structure=structure,
                                      modified_by=request.user)

            log_action(user=request.user,
                       obj=visiting,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request, messages.SUCCESS,
                                 _("Visiting edited"))
            return redirect('visiting:structure_visiting',
                            structure_slug=structure_slug,
                            visiting_pk=visiting.pk)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'structure': structure,
         'visiting': visiting}
    template = 'edit_visiting.html'
    return render(request, template, d)
