from django.contrib import admin
from django.contrib import admin

from .models import *

@admin.register(Detection)
class DetectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'num', 'den', 'value')
    search_fields = ('date',)
    list_filter = ('date',)

