from django.contrib import admin

from template.admin import AbstractCreatedModifiedBy

from .models import Detection, DetectionCode, StructureDetectionCode


@admin.register(Detection)
class DetectionAdmin(AbstractCreatedModifiedBy):
    list_display = ('structure', 'code', 'reference_date',
                    'value', 'is_active')
    search_fields = ('structure__name', 'code__code')
    list_filter = ('structure__name', 'code__code', 'reference_date')


@admin.register(DetectionCode)
class DetectionCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'is_active')


@admin.register(StructureDetectionCode)
class StructureDetectionCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'structure')
