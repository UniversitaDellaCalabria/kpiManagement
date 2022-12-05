from django import forms
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import BootstrapItaliaDateWidget, BootstrapItaliaSelectWidget

from .models import PublicEngagement, PublicEngagementPartner


class PublicEngagementForm(forms.ModelForm):

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
            'subscription_date': _('Subscription Date'),
            'duration': _('Duration (Months)'),
            'subject': _('Subject'),
            'goal': _('Goals AGENDA ONU 2030'),
            'requirements_one': _('Non-profit activity (No production of profit)'),
            'requirements_two': _('Activities aimed at non-academic audiences'),
            'requirements_three': _('Social value (social inclusion, fight against inequalities, etc.)'),
            'note': _('Notes'),
            'is_active': _('Enabled'),
        }

        help_texts = {
            'requirements_one': _('If this option is not selected the entry will not be evaluated'),
            'requirements_two': _('If this option is not selected the entry will not be evaluated'),
            'requirements_three': _('If this option is not selected the entry will not be evaluated'),
            'goal': _('Obiettivo 1 - Porre fine alla povertà, in tutte le sue forme <br> '
                      'Obiettivo 2 -  Porre fine alla fame, raggiungere la sicurezza alimentare, migliorare la nutrizione e promuovere un’agricoltura sostenibile <br> '
                      'Obiettivo 3 - Assicurare la salute e il benessere per tutti e per tutte le età <br> '
                      'Obiettivo 4 -  Assicurare un’istruzione di qualità, equa ed inclusiva, e promuovere opportunità di apprendimento permanente per tutti <br> '
                      'Obiettivo 5 - Raggiungere l’uguaglianza di genere e l’empowerment di tutte le donne e le ragazze <br> '
                      'Obiettivo 10 - Ridurre l’ineguaglianza all’interno di e fra le Nazioni <br> '
                      'Obiettivo 16 - Promuovere società pacifiche e più inclusive per uno sviluppo sostenibile; offrire l’accesso alla giustizia per tutti e creare organismi efficienti, responsabili e inclusivi a tutti i livelli.'),
        }

        widgets = {
            'subscription_date': BootstrapItaliaDateWidget,
            'subject': forms.Textarea(attrs={'rows': 2}),
            'goal': forms.Textarea(attrs={'rows': 2}),
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
