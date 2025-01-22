from django.db.models import Q


from rest_framework import permissions

from ... models import PublicEngagementEvent

# from .. permissions import *

from . generic import PublicEngagementEventList


class PublicEngagementEventList(PublicEngagementEventList):

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self, **kwargs):
        """
        """
        events = PublicEngagementEvent.objects\
            .prefetch_related('data')\
            .prefetch_related('report')\
            .select_related('referent')\
            .select_related('structure')\
            .filter(Q(referent=self.request.user) |
                    Q(created_by=self.request.user),
                    structure__is_active=True,
                    is_active=True)
        return events
