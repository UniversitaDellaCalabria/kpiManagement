import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datatables_ajax.datatables import DjangoDatatablesServerProc


from . decorators import can_manage_structure_visitings
from . models import Visiting


_columns = ['pk', 'visitor', 'from_structure', 'to_structure',
            'mission', 'start_date', 'end_date', 'is_active']


class VisitingDTD(DjangoDatatablesServerProc):

    def get_queryset(self):
        """
        Sets DataTable tickets common queryset
        """
        self.aqs = self.queryset
        if self.search_key:
            params = json.loads(self.search_key)
            start = params.get('start', '')
            end = params.get('end', '')
            text = params.get('text', '')
            mission = params.get('mission', '')
            is_active = params.get('is_active', '')
            if start:
                self.aqs = self.aqs.filter(start_date=start)
            if end:
                self.aqs = self.aqs.filter(end_date=end)
            if mission:
                self.aqs = self.aqs.filter(mission=mission)
            if is_active:
                self.aqs = self.aqs.filter(is_active=is_active)
            if text:
                self.aqs = self.aqs.filter(
                    Q(visitor__last_name__icontains=text) |
                    Q(from_structure__name__icontains=text) |
                    Q(to_structure__name__icontains=text))


@csrf_exempt
@login_required
@can_manage_structure_visitings
def datatables_structure_visitings(request, structure_slug, structure=None):
    """
    :return: JsonResponse
    """

    visitings = Visiting.objects.filter(Q(from_structure=structure) |
                                        Q(to_structure=structure))
    dtd = VisitingDTD(request, visitings, _columns)
    return JsonResponse(dtd.get_dict())
