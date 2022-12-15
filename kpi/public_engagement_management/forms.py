from django import forms
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget, BootstrapItaliaSelectWidget

from .models import PublicEngagement, PublicEngagementPartner, Goal


class PublicEngagementForm(forms.ModelForm):

    goal = forms.ModelMultipleChoiceField(label=_('Goals AGENDA ONU 2030'),
                                            required=True,
                                            queryset=None,
                                            widget=forms.CheckboxSelectMultiple())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['goal'].queryset = Goal.objects.all()

    class Meta:
        model = PublicEngagement
        fields = [
            'subscription_date',
            'duration',
            'subject',
            'goal',
            'requirements_one',
            'requirements_two',
            'requirements_three',
            'note',
            'is_active',
        ]

        labels = {
            'subscription_date': _('Subscription Date of the Protocol'),
            'duration': _('Duration (Months) of the Protocol'),
            'subject': _('Subject of the Protocol (briefly describe max 500 characters)'),
            'requirements_one': _('Involves non-profit activity (No production of profit for the department)'),
            'requirements_two': _('Involves activities aimed at non-academic audiences (even outside the university campus)'),
            'requirements_three': _('Has a social value (meets one or more social objectives of the Agenda 2030 of ONU or pursues other social purposes)'),
            'note': _('Any additional notes on the registered Protocol (report briefly below max 500 characters)'),
            'is_active': _('Enabled'),
        }

        help_texts = {
            'requirements_one': _('If this option is not selected the entry will not be evaluated'),
            'requirements_two': _('If this option is not selected the entry will not be evaluated'),
            'requirements_three': _('If this option is not selected the entry will not be evaluated'),
        }

        widgets = {
            'subscription_date': BootstrapItaliaDateWidget,
            'subject': forms.Textarea(attrs={'rows': 2}),
            'note': forms.Textarea(attrs={'rows': 2})
        }

    class Media:
        js = ('js/textarea-autosize.js',)


class PublicEngagementPartnerForm(forms.ModelForm):

    class Meta:
        model = PublicEngagementPartner
        fields = ['partner', 'is_head']
        labels = {
            'partner': _('Partner'),
            'is_head': _('Head'),
        }
        widgets = {'partner': BootstrapItaliaSelectWidget}

    class Media:
        js = ('js/textarea-autosize.js',)
