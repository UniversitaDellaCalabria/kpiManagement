from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.translation import gettext_lazy as _

# from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from template.utils import check_user_permission_on_dashboard, log_action

from . decorators import *
from . forms import *
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
# @belongs_to_an_office
def dashboard(request):
    template = 'dashboard_visitings.html'

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   '#': 'Visiting/Mobilità docenti'}

    offices = check_user_permission_on_dashboard(request.user,
                                                 Visiting,
                                                 VISITING_OFFICE_SLUG)
    if not offices:
        messages.add_message(request, messages.ERROR,
                             _("Permission denied"))
        return redirect('template:dashboard')

    result = []
    for off in offices:
        visiting_out = Visiting.objects.filter(
            from_structure=off.organizational_structure).count()
        visiting_in = Visiting.objects.filter(
            to_structure=off.organizational_structure).count()
        result.append({'office': off,
                       'visiting_in': visiting_in,
                       'visiting_out': visiting_out})

    d = {'breadcrumbs': breadcrumbs, 'my_offices': result}

    return render(request, template, d)


@login_required
@can_view_structure_visitings
def structure_visitings(request, structure_slug, structure=None):
    """
    param structure comes from @can_manage_structure_visitings
    """
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('visiting:dashboard'): 'Visiting/Mobilità docenti',
                   '#': structure.name }
    d = {'breadcrumbs': breadcrumbs, 'structure': structure}
    template = 'visitings.html'
    return render(request, template, d)


@login_required
@can_view_structure_visitings
def structure_visiting(request, structure_slug, visiting_pk, structure=None):
    """
    param structure comes from @can_manage_structure_visitings
    """
    visiting = get_object_or_404(Visiting,
                                 Q(from_structure=structure) |
                                 Q(to_structure=structure),
                                 pk=visiting_pk,)

    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('visiting:dashboard'): 'Visiting/Mobilità docenti',
                   reverse('visiting:structure_visitings', kwargs={'structure_slug': structure_slug}): structure.name,
                   '#': visiting.pk}

    collaborations = VisitingCollaboration.objects.filter(visiting=visiting)

    visiting_logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(visiting).pk,
                                            object_id=visiting.pk)

    d = {'breadcrumbs': breadcrumbs,
         'collaborations': collaborations,
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
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('visiting:dashboard'): 'Visiting/Mobilità docenti',
                   reverse('visiting:structure_visitings', kwargs={'structure_slug': structure_slug}): structure.name,
                   '#': 'Nuovo' }
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
            messages.add_message(request, messages.ERROR,
                                 f"<b>Attenzione</b>: correggi gli errori nel form")

    d = {'breadcrumbs': breadcrumbs,
         'form': form,
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
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('visiting:dashboard'): 'Visiting/Mobilità docenti',
                   reverse('visiting:structure_visitings', kwargs={'structure_slug': structure_slug}): structure.name,
                   reverse('visiting:structure_visiting', kwargs={'structure_slug': structure_slug, 'visiting_pk': visiting_pk}): visiting.pk,
                   '#': 'Modifica' }

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
            messages.add_message(request, messages.ERROR,
                                 f"<b>Attenzione</b>: correggi gli errori nel form")

    d = {'breadcrumbs': breadcrumbs,
         'form': form,
         'structure': structure,
         'visiting': visiting}
    template = 'edit_visiting.html'
    return render(request, template, d)
