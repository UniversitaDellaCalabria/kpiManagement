from django.contrib import admin

from .admin_inlines import *
from .models import *


class AbstractAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(OrganizationalStructureFunction)
class OrganizationalStructureFunctionAdmin(AbstractAdmin):
    pass


@admin.register(OrganizationalStructureType)
class OrganizationalStructureTypeAdmin(AbstractAdmin):
    pass


@admin.register(OrganizationalStructure)
class OrganizationalStructureAdmin(AbstractAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'structure_type',
                    'description',
                    'is_visiting_enabled',
                    'is_public_engagement_enabled',
                    'is_internal',
                    'is_active')
    list_filter = ('structure_type',
                   'is_visiting_enabled',
                   'is_public_engagement_enabled',
                   'is_internal',
                   'is_active')
    list_editable = ('is_visiting_enabled',
                     'is_public_engagement_enabled',
                     'is_internal',
                     'is_active')
    search_fields = ('name',)
    inlines = [OrganizationalStructureLocationInline,
               OrganizationalStructureOfficeInline,
               UserManageOrganizationalStructureInline]


@admin.register(OrganizationalStructureOffice)
class OrganizationalStructureOfficeAdmin(AbstractAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'organizational_structure', 'is_active')

    list_filter = ('organizational_structure__is_internal',
                   'organizational_structure__is_visiting_enabled',
                   'organizational_structure__is_public_engagement_enabled',
                   'organizational_structure',
                   'is_active')

    list_editable = ('is_active',)

    inlines = [OrganizationalStructureOfficeEmployeeInline,
               OrganizationalStructureOfficeLocationInline, ]


# @admin.register(TipoDotazione)
# class TipoDotazioneAdmin(admin.ModelAdmin):
    #list_display = ('nome', 'descrizione')


# @admin.register(Locazione)
# class LocazioneAdmin(admin.ModelAdmin):
    #list_display = ('nome', 'indirizzo', 'descrizione_breve',)


# @admin.register(OrganizationalStructureFunction)
# class OrganizationalStructureFunction(AbstractAdmin):
    # pass
