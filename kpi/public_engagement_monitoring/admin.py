from django.contrib import admin

from template.admin import AbstractCreatedModifiedBy

from .models import *


@admin.register(PublicEngagementAnnualMonitoring)
class PublicEngagementAnnualMonitoringAdmin(AbstractCreatedModifiedBy):
    list_display = ('year', 'is_active')
    list_editable = ('is_active',)


@admin.register(PublicEngagementEventType)
class PublicEngagementEventTypeAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active')


@admin.register(PublicEngagementEventMethodOfExecution)
class PublicEngagementEventMethodOfExecutionAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active')


@admin.register(PublicEngagementEventTarget)
class PublicEngagementEventTargetAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active')


@admin.register(PublicEngagementEventPromoChannel)
class PublicEngagementEventPromoChannelAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active')


@admin.register(PublicEngagementEventPromoTool)
class PublicEngagementEventPromoToolAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active')


@admin.register(PublicEngagementEventRecipient)
class PublicEngagementEventRecipientAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_active')


@admin.register(PublicEngagementEvent)
class PublicEngagementEventAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in PublicEngagementEvent._meta.fields if field.name != "id"]
    list_display = ('title', 'start', 'end')


@admin.register(PublicEngagementEventData)
class PublicEngagementEventDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PublicEngagementEventData._meta.fields if field.name != "id"]
