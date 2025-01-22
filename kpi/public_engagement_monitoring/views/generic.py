from django.contrib.auth.decorators import login_required
from django.shortcuts import render, reverse
from django.utils.translation import gettext_lazy as _

# from organizational_area.decorators import belongs_to_an_office
from organizational_area.models import *

from template.utils import *

from .. decorators.generic import *
from .. forms import *
from .. models import *
from .. settings import *
from .. utils import *


@login_required
@can_manage_public_engagement
def dashboard(request):
    template = 'pem/dashboard.html'
    breadcrumbs = {reverse('template:dashboard'): _('Dashboard'),
                   '#': _('Public Engagement')}
    return render(request, template, {'breadcrumbs': breadcrumbs})
