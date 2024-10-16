from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from organizational_area.decorators import belongs_to_an_office

from . forms import *
from . models import User
from . jwts import encrypt_to_jwe, decrypt_from_jwe
from . settings import *


@login_required
@belongs_to_an_office
def users(request):
    template = 'users.html'
    if request.user.is_superuser:
        users = User.objects.filter(is_active=True)
    else:
        users = User.objects.filter(is_active=True,
                                    created_by=request.user)
    data = {'users': users}
    return render(request, template, data)


@login_required
@belongs_to_an_office
def new_user(request):
    template = 'new_user.html'
    form = UserForm()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            # gender = form.cleaned_data['gender']
            codice_fiscale = form.cleaned_data['codice_fiscale']

            User.objects.create(username=codice_fiscale,
                                first_name=first_name,
                                last_name=last_name,
                                email=email,
                                # gender=gender,
                                codice_fiscale=codice_fiscale,
                                created_by=request.user)

            messages.add_message(request, messages.SUCCESS,
                                 _("User created"))

            return redirect('unical_accounts:users')
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {strip_tags(v)}")
    data = {'form': form}
    return render(request, template, data)


@login_required
@belongs_to_an_office
def edit_user(request, user_tax_code):
    template = 'edit_user.html'
    # if user has been created by current user
    # and hasn't ever made first access
    user = get_object_or_404(User,
                             is_active=True,
                             codice_fiscale=user_tax_code)

    if user.created_by != request.user or user.last_login:
        messages.add_message(request, messages.ERROR,
                             _("You haven't privileges to edit this user"))
        return redirect('unical_accounts:users')

    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(instance=user, data=request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.codice_fiscale = form.cleaned_data['codice_fiscale']
            user.save()

            messages.add_message(request, messages.SUCCESS,
                                 _("User successfully updated"))

            return redirect('unical_accounts:users')
        else:  # pragma: no cover
            for k, v in form.errors.items():
                messages.add_message(request, messages.ERROR,
                                     f"<b>{form.fields[k].label}</b>: {strip_tags(v)}")
    data = {'form': form}
    return render(request, template, data)


@login_required
def account(request):
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   '#': _('Account')}
    template = "account.html"
    context = {'breadcrumbs': breadcrumbs}
    return render(request, template, context)


@login_required
def changeData(request):
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   reverse('unical_accounts:account'): _('Account'),
                   '#': _('Edit')}
    initial = {}
    for field in EDITABLE_FIELDS:
        initial[field] = getattr(request.user, field)
    form = UserDataForm(initial=initial)
    template = "change_user_data.html"
    user = request.user
    user_email = user.email

    if request.POST:
        form = UserDataForm(request.POST, instance=user)
        if form.is_valid():
            email = form.cleaned_data.pop('email', '')
            if len(form.cleaned_data) > 1:
                user = form.save(commit=False)
                user.manual_user_update = timezone.now()
                user.save()
                messages.add_message(
                    request, messages.SUCCESS, _("Data saved successfully")
                )

            if 'email' in EDITABLE_FIELDS and email != user_email:
                base_url = request.build_absolute_uri(
                    reverse("unical_accounts:confirm_email")
                )
                token = f'{request.user.id}|{email}|{timezone.now()}'
                encrypted_data = encrypt_to_jwe(token)
                url = f'{base_url}?token={encrypted_data}'

                print(url)

                body=_("Confirm your email by clicking here {}").format(url)
                msg_body = f'{MSG_HEADER.format(hostname=settings.DEFAULT_HOST)}{body}{MSG_FOOTER}'
                result = send_mail(
                    subject=_("Email confirmation"),
                    message=msg_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=True,
                )
                messages.add_message(
                    request, messages.INFO, _("An email has been sent to the address you indicated. Click on the link in the message to confirm the new data")
                )
            return redirect("unical_accounts:change_data")
        else:
            messages.add_message(
                request, messages.ERROR, _("Wrong data")
            )

    context = {'form': form,
               'title': _("Edit personal data"),
               'breadcrumbs': breadcrumbs}
    return render(request, template, context)


@login_required
def confirmEmail(request):
    token = request.GET.get('token')
    if not token:
        messages.add_message(
            request, messages.ERROR, _("Missing token")
        )
        return redirect("unical_accounts:change_data")

    try:
        data = decrypt_from_jwe(token).decode()
        items = data.split("|")
    except:
        messages.add_message(
            request, messages.ERROR, _("Invalid token")
        )
        return redirect("unical_accounts:change_data")

    user_id = items[0]
    email = items[1]
    timestamp = items[2]

    user = get_object_or_404(User, pk=user_id)
    token_date = parse_datetime(timestamp)
    time_diff = timezone.now() - token_date

    token_life_expired = time_diff.total_seconds() / 60 > CHANGE_EMAIL_TOKEN_LIFE
    token_invalid = user.manual_user_update and token_date < user.manual_user_update

    if token_life_expired or token_invalid:
        messages.add_message(
            request, messages.ERROR, _("Expired token")
        )
        return redirect("unical_accounts:change_data")

    user.email = email
    user.manual_user_update = timezone.now()
    user.save(update_fields=['email', 'manual_user_update'])
    messages.add_message(
        request, messages.SUCCESS, _("Email updated successfully")
    )
    return redirect("unical_accounts:account")
