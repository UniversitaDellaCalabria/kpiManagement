from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget, BootstrapItaliaSelectWidget

from template.widgets import *

from . models import Collaboration, Visiting
from . widgets import *


class VisitingForm(forms.ModelForm):
    collab = forms.ModelMultipleChoiceField(label=_('Collaboration'),
                                            required=True,
                                            queryset=None,
                                            widget=BootstrapItaliaMultiCheckboxWidget())

    def __init__(self, *args, **kwargs):
        self.structure = kwargs.pop('structure')
        super().__init__(*args, **kwargs)
        self.fields['collab'].queryset = Collaboration.objects.all()

    class Meta:
        model = Visiting
        fields = ['visitor',
                  'role',
                  'from_structure',
                  'to_structure',
                  'collab',
                  # 'mission',
                  'start_date',
                  'end_date',
                  'didactic_hour',
                  'effective_days',
                  'note',
                  'is_active',
                  ]

        labels = {
            'role': _('Role'),
            'from_structure': _('From'),
            'to_structure': _('To'),
            'collab': _('Collaborations'),
            'start_date': _('Start'),
            'end_date': _('End'),
            'didactic_hour': _('Teaching/research/seminar hours'),
            'effective_days': _('Effective days'),
            'note': _('Notes'),
            'is_active': _('Enabled'),
        }

        widgets = {'visitor': BootstrapItaliaAPISelectVisitorWidget,
                   'from_structure': BootstrapItaliaAPISelectStructureWidget,
                   'to_structure': BootstrapItaliaAPISelectStructureWidget,
                   'role': BootstrapItaliaSelectWidget,
                   'start_date': BootstrapItaliaDateWidget,
                   'end_date': BootstrapItaliaDateWidget,
                   'note': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)

    def clean(self):
        cleaned_data = super().clean()

        # if choosen structures are different from own
        from_structure = cleaned_data.get('from_structure')
        to_structure = cleaned_data.get('to_structure')
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        effective_days = cleaned_data.get('effective_days')

        if from_structure and from_structure != self.structure and to_structure != self.structure:
            self.add_error('from_structure',
                           _("The departure or arrival facility must match your home facility"))
            self.add_error('to_structure',
                           _("The departure or arrival facility must match your home facility"))

        if from_structure and to_structure and from_structure == to_structure:
            self.add_error('from_structure',
                           _("Structures must be different"))
            self.add_error('to_structure',
                           _("Structures must be different"))

        if start_date and end_date and start_date > end_date:
            self.add_error('start_date',
                           _("Start date is greater than end date"))
            self.add_error('end_date',
                           _("Start date is greater than end date"))

        if start_date and end_date:
            delta = end_date - start_date
            delta_days = delta.days + 1
            if effective_days > delta_days:
                self.add_error('effective_days',
                               _("Effective days are greater than difference bewteen dates") + ": " + str(delta_days))
