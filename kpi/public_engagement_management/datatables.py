import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datatables_ajax.datatables import DjangoDatatablesServerProc


from . decorators import can_manage_structure_public_engagements
from . models import PublicEngagement


_columns = ['pk', 'subject', 'subscription_date', 'duration', 'is_active']


class PublicEngagementDTD(DjangoDatatablesServerProc):

    def get_queryset(self):
        """
        Sets DataTable tickets common queryset
        """
        self.aqs = self.queryset
        if self.search_key:
            params = json.loads(self.search_key)
            text = params.get('text', '')
            start = params.get('start', '')
            end = params.get('end', '')
            is_active = params.get('is_active', '')
            if start:
                self.aqs = self.aqs.filter(subscription_date__gte=start)
            if end:
                self.aqs = self.aqs.filter(subscription_date__lte=end)
            if is_active:
                self.aqs = self.aqs.filter(is_active=is_active)
            if text:
                self.aqs = self.aqs.filter(
                    Q(subject__icontains=text))


@csrf_exempt
@login_required
@can_manage_structure_public_engagements
def datatables_structure_public_engagements(request, structure_slug, structure=None):
    """
    :return: JsonResponse
    """

    public_engagements = PublicEngagement.objects.filter(Q(structure=structure))
    dtd = PublicEngagementDTD(request, public_engagements, _columns)
    return JsonResponse(dtd.get_dict())
