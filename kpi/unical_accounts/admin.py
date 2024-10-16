from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    readonly_fields = ('date_joined', 'last_login', 'manual_user_update')
    list_display = ('username', 'matricola_dipendente',
                    'matricola_studente', 'email', 'is_active',
                    'is_staff', 'is_superuser', )
    list_editable = ('is_active', 'is_staff', 'is_superuser',)
    fieldsets = (
        (None, {'fields': (('username', 'is_active', 'is_staff', 'is_superuser', ),
                           ('password'),
                           )
                }),
        (_('Angrafica'), {'fields': (('first_name', 'last_name'),
                                     ('matricola_dipendente',
                                      'matricola_studente'),
                                     'email',
                                     ('codice_fiscale',),
                                     ('gender',
                                      'place_of_birth', 'birth_date',),
                                     )
                          }),

        (_('Permissions'), {'fields': ('groups', 'user_permissions'),
                            'classes': ('collapse',)
                            }),


        (_('Date accessi sistema'), {'fields': (('date_joined',
                                                 'last_login',
                                                 'manual_user_update' ))
                                     }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
