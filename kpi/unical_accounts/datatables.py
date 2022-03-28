import json

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from datatables_ajax.datatables import DjangoDatatablesServerProc


from . models import User

_columns = ['pk', 'last_name', 'first_name', 'codice_fiscale', 'email']


class UserDTD(DjangoDatatablesServerProc):

    def get_queryset(self):
        """
        Sets DataTable tickets common queryset
        """
        self.aqs = self.queryset
        if self.search_key:
            params = json.loads(self.search_key)
            text = params.get('text', '')
            if text:
                self.aqs = self.aqs.filter(
                    Q(last_name__icontains=text) |
                    Q(first_name__icontains=text) |
                    Q(codice_fiscale__icontains=text) |
                    Q(email__icontains=text))


@csrf_exempt
@login_required
def datatables_users(request):
    """
    :return: JsonResponse
    """

    users = User.objects.filter(is_active=True)
    dtd = UserDTD(request, users, _columns)
    return JsonResponse(dtd.get_dict())
