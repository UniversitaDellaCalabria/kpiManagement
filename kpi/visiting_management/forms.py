from django import forms
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget, BootstrapItaliaSelectWidget

from . models import Collaboration, Visiting


class VisitingForm(forms.ModelForm):
    collab = forms.ModelMultipleChoiceField(label=_('Collaboration'),
                                            required=True,
                                            queryset=None,
                                            widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        self.structure = kwargs.pop('structure')
        super().__init__(*args, **kwargs)
        self.fields['collab'].queryset = Collaboration.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        # if choosen structures are different from own
        from_structure = cleaned_data['from_structure']
        to_structure = cleaned_data['to_structure']
        start_date = cleaned_data['start_date']
        end_date = cleaned_data['end_date']

        if from_structure != self.structure and to_structure != self.structure:
            self.add_error('from_structure',
                           _("The departure or arrival facility must match your home facility"))
            self.add_error('to_structure',
                           _("The departure or arrival facility must match your home facility"))

        if from_structure == to_structure:
            self.add_error('from_structure',
                           _("Structures must be different"))
            self.add_error('to_structure',
                           _("Structures must be different"))

        if start_date > end_date:
            self.add_error('start_date',
                           _("Start date is greater than end date"))
            self.add_error('end_date',
                           _("Start date is greater than end date"))

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

                  ]

        widgets = {'visitor': BootstrapItaliaSelectWidget,
                   'from_structure': BootstrapItaliaSelectWidget,
                   'to_structure': BootstrapItaliaSelectWidget,
                   'role': BootstrapItaliaSelectWidget,
                   'start_date': BootstrapItaliaDateWidget,
                   'end_date': BootstrapItaliaDateWidget,
                   'note': forms.Textarea(attrs={'rows': 2})}

    class Media:
        js = ('js/textarea-autosize.js',)
