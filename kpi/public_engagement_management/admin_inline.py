from django.contrib import admin
from .models import PublicEngagementPartner


class PublicEngagementPartnerAdminInline(admin.TabularInline):
    model = PublicEngagementPartner
    extra = 0
