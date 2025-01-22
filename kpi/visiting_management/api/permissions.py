from organizational_area.models import OrganizationalStructure

from rest_framework.permissions import BasePermission

from template.utils import check_user_permission_on_dashboard

from .. models import Visiting
from .. settings import VISITING_OFFICE_SLUG


class IsVisitingOperator(BasePermission):
    def has_permission(self, request, view):
        offices = check_user_permission_on_dashboard(request.user,
                                                     Visiting,
                                                     VISITING_OFFICE_SLUG)
        if not offices:
            return False
        return True
