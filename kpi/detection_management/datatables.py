import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datatables_ajax.datatables import DjangoDatatablesServerProc


from . decorators import can_manage_structure_detections
from . models import Detection


_columns = ['pk', 'code', 'reference_date',
            'detection_date', 'num', 'den', 'value', 'is_active' ]


class DetectionDTD(DjangoDatatablesServerProc):

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
            is_active = params.get('is_active', '')
            code = params.get('code', '')
            if start:
                self.aqs = self.aqs.filter(reference_date__gte=start)
            if end:
                self.aqs = self.aqs.filter(reference_date__lte=end)
            if code:
                self.aqs = self.aqs.filter(code=code)
            if is_active:
                self.aqs = self.aqs.filter(is_active=is_active)
            if text:
                self.aqs = self.aqs.filter(
                    Q(code__description__icontains=text) |
                    Q(code__code__icontains=text))

@csrf_exempt
@login_required
@can_manage_structure_detections
def datatables_structure_detections(request, structure_slug, structure=None):
    """
    :return: JsonResponse
    """

    detections = Detection.objects.filter(structure=structure,
                                          code__is_active=True)
    dtd = DetectionDTD(request, detections, _columns)
    return JsonResponse(dtd.get_dict())
