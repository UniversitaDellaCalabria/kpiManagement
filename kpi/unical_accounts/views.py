from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.html import strip_tags
from django.utils.translation import gettext_lazy as _

from organizational_area.decorators import belongs_to_an_office


from . forms import UserForm
from . models import User


@login_required
@belongs_to_an_office
def users(request):
    template = 'users.html'
    users = User.objects.filter(is_active=True)
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
