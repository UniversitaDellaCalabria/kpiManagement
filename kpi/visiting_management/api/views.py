from django.contrib.auth import get_user_model
from django_filters.rest_framework import *

from rest_framework import filters, generics, permissions

from organizational_area.api.views import *
from unical_accounts.api.views import *

from . permissions import IsVisitingOperator



class OrganizationalStructureList(OrganizationalStructureList):
    permission_classes = [permissions.IsAuthenticated,
                          IsVisitingOperator]
    queryset = OrganizationalStructure.objects.filter(is_active=True,
                                                      is_visiting_enabled=True)

class OrganizationalStructureDetail(OrganizationalStructureDetail):
    permission_classes = [permissions.IsAuthenticated,
                          IsVisitingOperator]
    queryset = OrganizationalStructure.objects.filter(is_active=True,
                                                      is_visiting_enabled=True)


class VisitingUserList(UserList):
    permission_classes = [permissions.IsAuthenticated,
                          IsVisitingOperator]


class VisitingUserDetail(UserDetail):
    permission_classes = [permissions.IsAuthenticated,
                          IsVisitingOperator]
