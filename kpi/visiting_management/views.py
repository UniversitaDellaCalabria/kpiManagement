from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from . decorators import can_manage_structure_visitings
from . forms import VisitingForm
from . settings import *
from . models import Visiting, VisitingCollaboration


@transaction.atomic
def _save_visiting(structure, form):

    visiting = form.save()

    visiting.mission = form.cleaned_data['to_structure'] != structure
    visiting.save(update_fields=['mission'])


    # set new collaborations
    VisitingCollaboration.objects.filter(visiting=visiting).delete()
    collabs = form.cleaned_data['collab']
    for collab in collabs:
        VisitingCollaboration.objects.create(visiting=visiting,
                                             collab=collab)


@login_required
@belongs_to_an_office
def dashboard(request):

    template = 'dashboard_visitings.html'

    # get offices that I'm able to manage
    offices = OrganizationalStructureOfficeEmployee.objects\
                                                   .filter(employee=request.user,
                                                           office__slug=VISITING_OFFICE_SLUG,
                                                           office__is_active=True,
                                                           office__organizational_structure__is_active=True)\
                                                   .select_related('office')
    d = {'my_offices': offices}

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

    d = {'collaborations': collaborations,
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

            _save_visiting(form=form, structure=structure)

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
        if form.is_valid():

            _save_visiting(form=form, structure=structure)

            messages.add_message(request, messages.SUCCESS,
                                 _("Visiting edited"))
            return redirect('visiting:structure_visitings',
                            structure_slug=structure_slug)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'structure': structure,
         'visiting': visiting}
    template = 'edit_visiting.html'
    return render(request, template, d)
