from django.forms import ModelForm

from bootstrap_italia_template.widgets import BootstrapItaliaSelectWidget

from . models import User
from . settings import EDITABLE_FIELDS, REQUIRED_FIELDS


class UserForm(ModelForm):
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


class UserDataForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in EDITABLE_FIELDS:
            if field in REQUIRED_FIELDS:
                self.fields[field].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'email' in EDITABLE_FIELDS:
            instance.email = self.initial['email']
        if commit:
            instance.save()
        return instance

    class Meta:
        model = User
        fields = EDITABLE_FIELDS
        labels = {'email': 'E-mail'}
