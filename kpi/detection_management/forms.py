from django import forms
from django.utils.translation import gettext_lazy as _
from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget, BootstrapItaliaSelectWidget, HiddenInput
from . models import Detection

class DetectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.structure = kwargs.pop('structure')
        super().__init__(*args, **kwargs)
        self.fields['code'].required = False

    class Meta:
        model = Detection
        fields = ['code',
                  'date',
                  'num',
                  'den',
                  'value',
                  ]

        labels = {
            'code': _('Codice'),
            'date': _('Data di Rilevazione'),
            'num': _('Numeratore'),
            'den': _('Denominatore'),
            'value': _('Valore KPI'),
        }

        widgets = {'code': HiddenInput,
                   'date': BootstrapItaliaDateWidget}

    class Media:
        js = ('js/textarea-autosize.js',)