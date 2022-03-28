from django.contrib import admin
from .models import VisitingCollaboration


class VisitingCollaborationAdminInline(admin.TabularInline):
    #list_display = ('visitor', 'from_structure', 'to_structure')
    #search_fields = ('visitor__last_name',)
    #list_filter = ('from_structure', 'to_structure')
    model = VisitingCollaboration
    extra = 0
