from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext_lazy as _

# from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from template.utils import check_user_permission_on_dashboard, log_action

from . decorators import *
from . forms import *
from . models import *
from . settings import *


@transaction.atomic
def _save_public_engagement(structure, form, **kwargs):
    """
    Save public_engagement from form.
    Passing additional fields in kwargs.
    """
    public_engagement = form.save(commit=False)
    public_engagement.structure = structure

    # additional fields
    for k, v in kwargs.items():
        setattr(public_engagement, k, v)
        # update_fields.append(k)

    public_engagement.save()


    # set new goals
    PublicEngagementGoal.objects.filter(public_engagement=public_engagement).delete()
    goals = form.cleaned_data['goal']
    for goal in goals:
        PublicEngagementGoal.objects.create(public_engagement=public_engagement, goal=goal)

    return public_engagement


@transaction.atomic
def _save_public_engagement_partner(public_engagement, form, **kwargs):
    """
    Save public_engagement partner from form.
    Passing additional fields in kwargs.
    """
    public_engagement_partner = form.save(commit=False)
    public_engagement_partner.public_engagement = public_engagement

    # additional fields
    for k, v in kwargs.items():
        setattr(public_engagement_partner, k, v)
        # update_fields.append(k)

    public_engagement_partner.save()
    return public_engagement_partner


@login_required
# @belongs_to_an_office
def dashboard(request):

    template = 'dashboard_public_engagements.html'
    offices = check_user_permission_on_dashboard(request.user,
                                                 PublicEngagement,
                                                 PUBLIC_ENGAGEMENT_OFFICE_SLUG)
    if not offices:
        messages.add_message(request, messages.ERROR,
                             _("Permission denied"))
        return redirect('template:dashboard')

    d = {'my_offices': offices}

    return render(request, template, d)

@login_required
def info(request):
    offices = check_user_permission_on_dashboard(request.user,
                                                 PublicEngagement,
                                                 PUBLIC_ENGAGEMENT_OFFICE_SLUG)
    if not offices:
        messages.add_message(request, messages.ERROR,
                             _("Permission denied"))
        return redirect('template:dashboard')

    template = 'info_public_engagement.html'
    return render(request, template, {})


@login_required
@can_view_structure_public_engagements
def structure_public_engagements(request, structure_slug, structure=None):
    """
    param structure comes from @can_manage_structure_public_engagements
    """
    d = {'structure': structure}
    template = 'public_engagements.html'
    return render(request, template, d)


@login_required
@can_view_structure_public_engagements
def structure_public_engagement(request, structure_slug,
                                public_engagement_pk, structure=None):
    """
    param structure comes from @can_manage_structure_public_engagements
    """
    public_engagement = get_object_or_404(PublicEngagement,
                                          structure=structure,
                                          pk=public_engagement_pk)

    goals = PublicEngagementGoal.objects.filter(public_engagement=public_engagement)

    partners = PublicEngagementPartner.objects\
                                      .filter(public_engagement=public_engagement)\
                                      .select_related('partner')

    public_engagement_logs = LogEntry.objects.filter(content_type_id=ContentType.objects.get_for_model(public_engagement).pk,
                                                     object_id=public_engagement.pk)

    d = {'goals': goals,
         'partners': partners,
         'public_engagement_logs': public_engagement_logs,
         'public_engagement': public_engagement,
         'structure': structure}
    template = 'public_engagement.html'
    return render(request, template, d)


@login_required
@can_manage_structure_public_engagements
def structure_public_engagement_new(request, structure_slug, structure=None):
    """
    param structure comes from @can_manage_structure_public_engagements
    """
    form = PublicEngagementForm()
    if request.POST:
        form = PublicEngagementForm(request.POST)
        if form.is_valid():

            public_engagement = _save_public_engagement(form=form,
                                                        structure=structure,
                                                        created_by=request.user)

            log_action(user=request.user,
                       obj=public_engagement,
                       flag=ADDITION,
                       msg=[{'added': {}}])

            messages.add_message(request, messages.SUCCESS,
                                 _("Social Engagement created"))
            return redirect('public_engagement:structure_public_engagements',
                            structure_slug=structure_slug)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'structure': structure}
    template = 'new_public_engagement.html'
    return render(request, template, d)


@login_required
@can_manage_structure_public_engagements
def structure_public_engagement_edit(request, structure_slug, public_engagement_pk, structure=None):
    """
    param structure comes from @can_manage_structure_public_engagements
    """
    public_engagement = get_object_or_404(PublicEngagement,
                                          structure=structure,
                                          pk=public_engagement_pk)

    goals = PublicEngagementGoal.objects.filter(
        public_engagement=public_engagement).values_list('goal', flat=True)

    partners = PublicEngagementPartner.objects.filter(public_engagement=public_engagement)\
                                              .values_list('partner')

    form = PublicEngagementForm(instance=public_engagement,
                                initial={'goal': goals})

    if request.POST:
        form = PublicEngagementForm(instance=public_engagement,
                                    initial={'goal': goals},
                                    data=request.POST)
        changed_field_labels = _get_changed_field_labels_from_form(form,
                                                                   form.changed_data)
        if form.is_valid():
            public_engagement = _save_public_engagement(form=form,
                                      structure=structure,
                                      modified_by=request.user)

            log_action(user=request.user,
                       obj=public_engagement,
                       flag=CHANGE,
                       msg=[{'changed': {"fields": changed_field_labels}}])

            messages.add_message(request, messages.SUCCESS,
                                 _("Social Engagement edited"))
            return redirect('public_engagement:structure_public_engagement',
                            structure_slug=structure_slug,
                            public_engagement_pk=public_engagement.pk)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'partners': partners,
         'public_engagement': public_engagement,
         'structure': structure,
        }
    template = 'edit_public_engagement.html'
    return render(request, template, d)


@login_required
@can_manage_structure_public_engagements
def structure_public_engagement_partner_add(request,
                                            structure_slug,
                                            public_engagement_pk,
                                            structure=None):
    """
    param structure comes from @can_manage_structure_public_engagements
    """
    public_engagement = get_object_or_404(PublicEngagement,
                                          structure=structure,
                                          pk=public_engagement_pk)

    form = PublicEngagementPartnerForm()
    if request.POST:
        form = PublicEngagementPartnerForm(request.POST)
        if form.is_valid():

            partner = _save_public_engagement_partner(form=form,
                                                      public_engagement=public_engagement,
                                                      created_by=request.user)

            log_action(user=request.user,
                       obj=public_engagement,
                       flag=CHANGE,
                       msg=f"Added new partner {partner}")

            messages.add_message(request, messages.SUCCESS,
                                 _("Social Engagement partner created"))
            return redirect('public_engagement:structure_public_engagement',
                            structure_slug=structure_slug,
                            public_engagement_pk=public_engagement_pk)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'public_engagement': public_engagement,
         'structure': structure}
    template = 'public_engagement_partner.html'
    return render(request, template, d)


@login_required
@can_manage_structure_public_engagements
def structure_public_engagement_partner_edit(request,
                                             structure_slug,
                                             public_engagement_pk,
                                             partner_pk,
                                             structure=None):
    """
    param structure comes from @can_manage_structure_public_engagements
    """
    public_engagement = get_object_or_404(PublicEngagement,
                                          structure=structure,
                                          pk=public_engagement_pk)
    partner = get_object_or_404(PublicEngagementPartner,
                                public_engagement=public_engagement,
                                pk=partner_pk)

    form = PublicEngagementPartnerForm(instance=partner)
    if request.POST:
        form = PublicEngagementPartnerForm(instance=partner,
                                           data=request.POST)
        if form.is_valid():
            form.save()
            log_action(user=request.user,
                       obj=public_engagement,
                       flag=CHANGE,
                       msg=f"Edited partner {partner}")

            messages.add_message(request, messages.SUCCESS,
                                 _("Social Engagement partner edited"))
            return redirect('public_engagement:structure_public_engagement',
                            structure_slug=structure_slug,
                            public_engagement_pk=public_engagement_pk)
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {v}")

    d = {'form': form,
         'partner': partner,
         'public_engagement': public_engagement,
         'structure': structure}
    template = 'public_engagement_partner.html'
    return render(request, template, d)


@login_required
@can_manage_structure_public_engagements
def structure_public_engagement_partner_delete(request,
                                               structure_slug,
                                               public_engagement_pk,
                                               partner_pk,
                                               structure=None):
    """
    param structure comes from @can_manage_structure_public_engagements
    """
    public_engagement = get_object_or_404(PublicEngagement,
                                          structure=structure,
                                          pk=public_engagement_pk)
    partner = get_object_or_404(PublicEngagementPartner,
                                public_engagement=public_engagement,
                                pk=partner_pk)
    log_action(user=request.user,
               obj=public_engagement,
               flag=CHANGE,
               msg=f"Deleted partner {partner}")
    partner.delete()
    messages.add_message(request, messages.SUCCESS,
                        _("Social Engagement partner deleted"))
    return redirect('public_engagement:structure_public_engagement',
                    structure_slug=structure_slug,
                    public_engagement_pk=public_engagement_pk)
