from django.contrib import admin

from template.admin import AbstractCreatedModifiedBy

from .admin_inline import *
from .models import *


@admin.register(PublicEngagement)
class PublicEngagementAdmin(AbstractCreatedModifiedBy):
    list_display = ('subscription_date', 'duration', 'subject', 'structure')
    search_fields = ('subscription_date',)
    list_filter = ('structure',)
    inlines = (PublicEngagementPartnerAdminInline,)
