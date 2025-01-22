from django.contrib.auth import get_user_model
from django_filters.rest_framework import *

from rest_framework import filters, generics, permissions

from template.api.pagination import KpiPagination

from . serializers import *


class UserList(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    search_fields = ['last_name','codice_fiscale']
    pagination_class = KpiPagination
    ordering = ['-last_name']
    queryset = get_user_model().objects.filter(is_active=True)


class UserDetail(generics.RetrieveAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = get_user_model().objects.filter(is_active=True)
