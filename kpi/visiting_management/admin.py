from django.contrib import admin

from template.admin import AbstractCreatedModifiedBy

from .admin_inline import *
from .models import *


@admin.register(Visiting)
class VisitingAdmin(AbstractCreatedModifiedBy):
    list_display = ('visitor', 'from_structure', 'to_structure', 'role')
    search_fields = ('visitor__last_name',)
    list_filter = ('from_structure', 'to_structure', 'role__role_type')
    inlines = (VisitingCollaborationAdminInline,)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_type',)


@admin.register(Collaboration)
class CollaborationAdmin(admin.ModelAdmin):
    list_display = ('collab_type',)
