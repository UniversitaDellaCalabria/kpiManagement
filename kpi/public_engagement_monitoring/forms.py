from django import forms
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import (BootstrapItaliaDateWidget,
                                               BootstrapItaliaSelectWidget)

from organizational_area.models import *

from . models import *
from . settings import VALIDATOR_INTERMIDIATE, VALIDATOR_FINAL


class PublicEngagementReferentForm(forms.Form):
    event_owner = forms.BooleanField(label=_('Sono io il referenete dell\'iniziativa'))


class PublicEngagementEventForm(forms.ModelForm):
    class Meta:
        model = PublicEngagementEvent
        fields = ['title', 'start', 'end', 'referent_organizational_structure',]
        widgets = {
            'start': BootstrapItaliaDateWidget,
            'end': BootstrapItaliaDateWidget,
        }

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        # se non sono il referente (che è un docente)
        # posso solo scegliere tra le strutture in cui sono abilitato
        # come operatore dipartimentale o di ateneo
        if request.user != request.session.get('referente'):
            structures_id = OrganizationalStructureOfficeEmployee.objects.filter(employee=request.user,
                                                                                 office__is_active=True,
                                                                                 office__slug__in=[VALIDATOR_INTERMIDIATE,
                                                                                                   VALIDATOR_FINAL],
                                                                                 office__organizational_structure__is_active=True,
                                                                                 office__organizational_structure__is_public_engagement_enabled=True,
                                                                                 office__organizational_structure__is_internal=True,
                                                                                 ).values('office__organizational_structure')
            structures = OrganizationalStructure.objects.filter(pk__in=structures_id)
            self.fields['referent_organizational_structure'].queryset = structures


    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end and start > end:
            self.add_error('start', "La data di inizio non può essere successiva a quella di fine")
            self.add_error('end', "La data di inizio non può essere successiva a quella di fine")

        active_years = PublicEngagementAnnualMonitoring.objects.filter(is_active=True).values_list('year', flat=True)
        if start and start.year not in active_years:
            self.add_error('start', f"Non è possibile inserire date per l'anno {start.year}")


class PublicEngagementEventDataForm(forms.ModelForm):
    class Meta:
        model = PublicEngagementEventData
        fields = '__all__'
        exclude = ('id', 'created', 'created_by', 'modified',
                   'modified_by', 'event', 'person')
        labels = {'project_scoped': 'Si tratta di un’attività collegata a un progetto o a una iniziativa più ampia?'}
        help_texts = {'project_name': "Compilare se si è selezionata l'opzione precedente"}

    def clean(self):
        cleaned_data = super().clean()

        project_scoped = cleaned_data.get('project_scoped')
        project_name = cleaned_data.get('project_name')

        if project_scoped and not project_name:
            self.add_error('project_name', "Indicare il nome del progetto")
