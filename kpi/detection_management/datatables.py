import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datatables_ajax.datatables import DjangoDatatablesServerProc


from . decorators import can_manage_structure_detections
from . models import Detection


_columns = ['pk', 'code', 'date', 'num', 'den', 'value', ]


class DetectionDTD(DjangoDatatablesServerProc):

    def get_queryset(self):
        """
        Sets DataTable tickets common queryset
        """
        self.aqs = self.queryset
        """
        if self.search_key:
            params = json.loads(self.search_key)
            date = params.get('date', '')
            if date:
                self.aqs = self.aqs.filter(date=date)
        """

@csrf_exempt
@login_required
@can_manage_structure_detections
def datatables_structure_detections(request, structure_slug, structure=None):
    """
    :return: JsonResponse
    """

    detections = Detection.objects.filter(Q(code=structure.name))
    dtd = DetectionDTD(request, detections, _columns)
    return JsonResponse(dtd.get_dict())
