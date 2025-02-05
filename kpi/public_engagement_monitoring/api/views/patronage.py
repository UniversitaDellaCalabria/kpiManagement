from django.db.models import Q
from django.utils import timezone

from rest_framework import permissions

from ... models import PublicEngagementAnnualMonitoring, PublicEngagementEvent
from .. permissions import IsStructurePatronageOperator
from . generic import PublicEngagementEventList


class PublicEngagementEventList(PublicEngagementEventList):

    permission_classes = [permissions.IsAuthenticated,
                          IsStructurePatronageOperator]

    def get_queryset(self, **kwargs):
        """
        """
        events = PublicEngagementEvent.objects\
            .prefetch_related('data')\
            .prefetch_related('report')\
            .select_related('referent')\
            .select_related('structure')\
            .filter(structure__slug=self.kwargs['structure_slug'],
                    structure__is_active=True,
                    to_evaluate=True,
                    is_active=True,
                    data__patronage_requested=True)

        status = self.request.query_params.get('status')
        if status=='to_handle' or status=='to_evaluate':
            active_years = PublicEngagementAnnualMonitoring.objects\
                                                   .filter(is_active=True)\
                                                   .values_list('year', flat=True)

        if status=='to_handle':
            events = events.filter(
                start__year__in=active_years,
                data__patronage_requested=True,
                operator_evaluation_success=True,
                patronage_operator_taken_date__isnull=True,
                created_by_manager=False,
                start__gte=timezone.now()
            )
        elif status=='to_evaluate':
            events = events.filter(
                data__patronage_requested=True,
                start__year__in=active_years,
                patronage_operator_taken_date__isnull=False,
                patronage_granted_date__isnull=True,
                created_by_manager=False,
                start__gte=timezone.now()
            )
        elif status=='approved':
            events = events.filter(patronage_granted=True,
                                   patronage_granted_date__isnull=False)
        elif status=='rejected':
            events = events.filter(patronage_granted=False,
                                   patronage_granted_date__isnull=False)
        return events
