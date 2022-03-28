from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from organizational_area.decorators import belongs_to_an_office


@login_required
@belongs_to_an_office
def dashboard(request):
    template = 'dashboard.html'
    d = {}
    return render(request, template, d)
