from django_filters.rest_framework import *

from rest_framework import filters, generics, permissions

from template.api.pagination import KpiPagination

from ... utils import *
from .. serializers import *


class PublicEngagementEventList(generics.ListAPIView):

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PublicEngagementEventSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter,
                       filters.OrderingFilter]
    filterset_fields = ['title', 'start', 'end',
                        'referent__last_name',
                        'to_evaluate',
                        'operator_evaluation_success']
    search_fields = ['title', 'referent__last_name', 'structure__name']
    pagination_class = KpiPagination
    ordering_fields = ['start', 'end', 'title']
    ordering = ['-start']
