import csv
import datetime

from django.contrib import messages
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.admin.utils import _get_changed_field_labels_from_form
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext_lazy as _

# from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from template.utils import *

from . decorators import *
from . forms import *
from . models import *
from . settings import *


def _export_csv(data):
    # Create the HttpResponse object with the appropriate CSV header.
    name = f'social_engagement_{data["structure"]}_{data["year"]}.csv' if data['structure'] else f'social_engagement_{data["year"]}.csv'
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{name}"'},
    )

    writer = csv.writer(response, delimiter='$')
    entries = PublicEngagement.objects.filter(subscription_date__year=data['year'],
                                              is_active=True)\
                                      .order_by('subscription_date')
    if data['structure']:
        entries = entries.filter(structure=data['structure'])


    writer.writerow([_('Structure'),
                     _('Subject'),
                     _('Duration'),
                     _('Subscription date'),
                     _('Involves non-profit activity (No production of profit for the department)'),
                     _('Involves activities aimed at non-academic audiences (even outside the university campus)'),
                     _('Has a social value (meets one or more social objectives of the Agenda 2030 of ONU or pursues other social purposes)'),
                     _('Note'),
                     _('Partners'),
                     _('Partners number'),
                     _('Goals')])

    for e in entries:
        partners = PublicEngagementPartner.objects.filter(public_engagement=e).values_list('partner__name', flat=True)
        goals = PublicEngagementGoal.objects.filter(public_engagement=e).values_list('goal__name', flat=True)
        writer.writerow([e.structure,
                         e.subject,
                         e.duration,
                         e.subscription_date,
                         e.requirements_one,
                         e.requirements_two,
                         e.requirements_three,
                         e.note,
                         list(partners),
                         partners.count(),
                         list(goals)])
    return response


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

    is_manager = request.user.is_superuser or check_user_permission_on_model(request.user, PublicEngagement)

    template = 'dashboard_public_engagements.html'
    offices = check_user_permission_on_dashboard(request.user,
                                                 PublicEngagement,
                                                 PUBLIC_ENGAGEMENT_OFFICE_SLUG)
    if not offices:
        messages.add_message(request, messages.ERROR,
                             _("Permission denied"))
        return redirect('template:dashboard')

    form = PublicEngagementExportCSVForm()

    d = {'form': form,
         'my_offices': offices,
         'is_manager': is_manager}

    if is_manager:

        if request.POST:
            form = PublicEngagementExportCSVForm(data=request.POST)
            if form.is_valid():
                year = form.cleaned_data['year']
                structure = form.cleaned_data['structure']
                return _export_csv({'year': year, 'structure': structure})
            else:  # pragma: no cover
                for k, v in form.errors.items():
                    messages.add_message(request, messages.ERROR,
                                         f"<b>{form.fields[k].label}</b>: {v}")

        date_start = request.GET.get('date_start', None)
        date_end = request.GET.get('date_end', None)
        start = None
        end = None
        try:
            if date_start: start = datetime.datetime.strptime(date_start, "%Y-%m-%d").date()
            if date_end: end = datetime.datetime.strptime(date_end, "%Y-%m-%d").date()
        except:
            start = None
            end = None

        all_public_engagements = PublicEngagement.objects.filter(is_active=True)
        if start: all_public_engagements = all_public_engagements.filter(subscription_date__gte=start)
        if end: all_public_engagements = all_public_engagements.filter(subscription_date__lte=end)

        internal_str = OrganizationalStructure.objects\
                                              .filter(is_active=True,
                                                      is_internal=True)
        str_engagements = []
        for struct in internal_str:
            str_engagements.append(all_public_engagements.filter(structure=struct).count())


        goals_list = Goal.objects.filter(is_active=True)
        all_goals_results = PublicEngagementGoal.objects.filter(goal__is_active=True,
                                                                public_engagement__is_active=True)
        goals_results = []
        for goal in goals_list:
            if start: all_goals_results = all_goals_results.filter(public_engagement__subscription_date__gte=start)
            if end: all_goals_results = all_goals_results.filter(public_engagement__subscription_date__lte=end)
            goals_results.append(all_goals_results.filter(goal=goal).count())

        d.update({'date_start': date_start,
                  'date_end': date_end,
                  'goals_list': list(goals_list.values_list('name', flat=True)),
                  'goals_results': goals_results,
                  'internal_str': list(internal_str.values_list('name', flat=True)),
                  'str_engagements': str_engagements})

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
