from django.db.models import Q

from rest_framework import permissions

from ... models import PublicEngagementAnnualMonitoring, PublicEngagementEvent
from .. permissions import IsManager
from . generic import PublicEngagementEventList


class PublicEngagementEventList(PublicEngagementEventList):

    permission_classes = [permissions.IsAuthenticated,
                          IsManager]

    def get_queryset(self, **kwargs):
        """
        """
        events = PublicEngagementEvent.objects\
            .prefetch_related('data')\
            .prefetch_related('report')\
            .select_related('referent')\
            .select_related('structure')\
            .filter(structure__slug=self.kwargs['structure_slug'],
                    structure__is_active=True)

        status = self.request.query_params.get('status')
        if status=='approved':
            events = events.filter(operator_evaluation_success=True,
                                   operator_evaluation_date__isnull=False)
        elif status=='rejected':
            events = events.filter(operator_evaluation_success=False,
                                   operator_evaluation_date__isnull=False)
        return events
