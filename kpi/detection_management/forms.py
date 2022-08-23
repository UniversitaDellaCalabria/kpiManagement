from django import forms
from django.utils.translation import gettext_lazy as _
from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget, BootstrapItaliaSelectWidget, HiddenInput
from . models import *


class DetectionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.structure = kwargs.pop('structure')
        super().__init__(*args, **kwargs)
        self.fields['code'].queryset = DetectionCode.objects.filter(is_active=True)

    def clean(self):
        cleaned_data = super().clean()

        # if code has changed then check if is available for
        # the structure
        # else if it's not changed ignore check (compatibility)
        if 'code' in self.changed_data:
            code = cleaned_data.get('code')
            str_code = StructureDetectionCode.objects.filter(structure=self.structure,
                                                             code=code).first()
            if not str_code:
                self.add_error('code',
                               _("Choosen code can be applied to this structure"))

        reference_date = cleaned_data.get('reference_date')
        detection_date = cleaned_data.get('detection_date')

        if reference_date > detection_date:
            self.add_error('detection_date',
                           _("Reference date is greater than detection date"))

    class Meta:
        model = Detection
        fields = ['code',
                  'reference_date',
                  'detection_date',
                  'num',
                  'den',
                  'note',
                  'is_active',
                  ]

        labels = {
            'code': _('Code'),
            'reference_date': _('Reference date'),
            'detection_date': _('Detection date'),
            'num': _('Numerator'),
            'den': _('Denominator'),
            'note': _('Notes'),
            'is_active': _('Enabled'),
        }

        widgets = {'reference_date': BootstrapItaliaDateWidget,
                   'detection_date': BootstrapItaliaDateWidget,
                   'note': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)
