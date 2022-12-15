from django.contrib import admin
from .models import PublicEngagementPartner, PublicEngagementGoal


class PublicEngagementPartnerAdminInline(admin.TabularInline):
    model = PublicEngagementPartner
    extra = 0

class PublicEngagementGoalAdminInline(admin.TabularInline):
    model = PublicEngagementGoal
    extra = 0
