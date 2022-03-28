from django import forms

from bootstrap_italia_template.widgets import BootstrapItaliaSelectWidget

from . models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'codice_fiscale',
                  # 'gender',
                  'email', ]
        # labels = {'name': _('Nome'),
        # 'description': _('Descrizione'),
        # 'allowed_users': _('Solo i seguenti utenti possono effettuare richieste')}
        widgets = {'gender': BootstrapItaliaSelectWidget}
        # help_texts = {'date_start': _("Formato {}. Lasciare vuoto  per non impostare"
        # "").format(settings.DEFAULT_DATETIME_FORMAT.replace('%','')),
        # 'date_end': _("Formato {}. Lasciare vuoto  per non impostare"
        # "").format(settings.DEFAULT_DATETIME_FORMAT.replace('%',''))}

    # class Media:
        # js = ('js/textarea-autosize.js',)
