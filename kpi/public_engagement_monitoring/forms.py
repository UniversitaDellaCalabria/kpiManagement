from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from bootstrap_italia_template.widgets import *
from organizational_area.models import *

from template.widgets import *

from . models import *
from . settings import *
from . utils import user_is_manager
from . widgets import *


class PublicEngagementReferentForm(forms.Form):
    event_owner = forms.BooleanField(
        label=_("I'm the event referent"))


class PublicEngagementEventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        structure_slug = kwargs.pop('structure_slug', None)

        super().__init__(*args, **kwargs)

        if structure_slug:
            structures = OrganizationalStructure.objects.filter(
                slug=structure_slug)
            self.fields['structure'].queryset = structures

        if self.data:
            data = self.data.copy()
            data['start'] = f'{data["start_date"]} {data["start_time"]}'
            data['end'] = f'{data["end_date"]} {data["end_time"]}'
            self.data = data

    class Meta:
        model = PublicEngagementEvent
        fields = ['title', 'start', 'end', 'structure', ]
        widgets = {
            'start': BootstrapItaliaDateTimeWidget,
            'end': BootstrapItaliaDateTimeWidget,
        }

    def clean(self):
        cleaned_data = super().clean()

        start = cleaned_data.get('start')
        end = cleaned_data.get('end')

        if start and end and start > end:
            self.add_error(
                'start', "La data di inizio non può essere successiva a quella di fine")
            self.add_error(
                'end', "La data di inizio non può essere successiva a quella di fine")

        active_years = PublicEngagementAnnualMonitoring.objects.filter(
            is_active=True).values_list('year', flat=True)
        if start and start.year not in active_years:
            self.add_error(
                'start', f"Non è possibile inserire date per l'anno {start.year}")

        if end and end > timezone.now() and self.instance.id and getattr(self.instance, 'report', None):
            self.add_error(
                'end', "Poichè sono già presenti i dati di monitoraggio, l'iniziativa deve essere già terminata")

        if self.instance.id and getattr(self.instance, 'data', None) and ((end and end <= timezone.localtime()) or (start < timezone.localtime() + timezone.timedelta(days=EVALUATION_TIME_DELTA))):
            if self.instance.data.patronage_requested or self.instance.data.promo_tool.exists():
                self.add_error(
                'end', "I dati per la promozione dell'iniziativa (patrocinio, canali di promozione, ecc...) non sono consentiti se è già terminata. Modificali prima di aggiornare la data.")

        return cleaned_data


class PublicEngagementEventOperatorForm(PublicEngagementEventForm):
    class Meta:
        model = PublicEngagementEvent
        fields = ['title', 'start', 'end', 'structure']
        widgets = {
            'start': BootstrapItaliaDateTimeWidget,
            'end': BootstrapItaliaDateTimeWidget,
        }


class PublicEngagementEventDataForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        # se si stanno creando i dati per la prima volta
        # e l'evento è terminato
        if not self.instance.id and event.is_over():
            self.fields.pop('promo_channel', None)
            self.fields.pop('patronage_requested', None)
            self.fields.pop('poster', None)
            self.fields.pop('promo_tool', None)

    class Meta:
        model = PublicEngagementEventData
        fields = '__all__'
        exclude = ('id', 'created', 'created_by', 'modified',
                   'modified_by', 'event', 'person', 'structures')
        widgets = {
            'event_type': BootstrapItaliaRadioWidget(),
            'method_of_execution': BootstrapItaliaRadioWidget(),
            'geographical_dimension': BootstrapItaliaRadioWidget(),
            'organizing_subject': BootstrapItaliaRadioWidget(),
            'recipient': BootstrapItaliaMultiCheckboxWidget(),
            'target': BootstrapItaliaMultiCheckboxWidget(),
            'promo_channel': BootstrapItaliaMultiCheckboxWidget(),
            'promo_tool': BootstrapItaliaMultiCheckboxWidget(),
            'project_name': BootstrapItaliaAPISelectEventWidget(),
            'patronage_requested': BootstrapItaliaToggleWidget(),
            'description': forms.Textarea(attrs={'rows': 2})
        }

    class Media:
        js = ('js/textarea-autosize.js',)

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.id and self.instance.event == project_name:
            self.add_error('project_name', "Non è possibile collegare all'evento medesimo")

        promo_channel = cleaned_data.get('promo_channel')
        patronage_requested = cleaned_data.get('patronage_requested')
        promo_tool = cleaned_data.get('promo_tool')
        poster = cleaned_data.get('poster')

        if patronage_requested and not promo_tool:
            self.add_error(
                'promo_tool', _("Make at least one choice if you require patronage"))
        if promo_channel and not poster:
            self.add_error(
                'poster', _("Mandatory field if you require the event to be promoted on institutional communication channels"))

        return cleaned_data


class PublicEngagementEventReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event = kwargs.pop('event')
        super().__init__(*args, **kwargs)
        self.fields['other_structure'].queryset = self.fields['other_structure'].queryset.exclude(
            pk=event.structure.pk)

    class Meta:
        model = PublicEngagementEventReport
        fields = '__all__'
        exclude = ('id', 'created', 'created_by', 'modified',
                   'modified_by', 'event', 'edited_by_manager')
        widgets = {
            'other_structure': BootstrapItaliaMultiCheckboxWidget(),
            'scientific_area': BootstrapItaliaMultiCheckboxWidget(),
            'collaborator_type': BootstrapItaliaMultiCheckboxWidget(),
            'impact_evaluation': BootstrapItaliaToggleWidget(),
            'monitoring_activity': BootstrapItaliaToggleWidget(),
            'notes': forms.Textarea(attrs={'rows': 2})
        }
        help_texts = {
            'participants': 'Indicare una stima del numero di partecipanti',
            'budget': "Si intende il budget finanziario complessivo direttamente legato all'organizzazione/gestione dell'iniziativa. di Public Engagement. Qualora l'iniziativa è una sottoattività di un progetto più ampio non considerabile complessivamente come Public Engagement, è necessario scorporare e riportare solo il budget direttamente dedicato. Quando la compilazione avvenga prima che l'iniziativa sia conclusa indicare il budget previsto/stimato. Nel campo ‘euro’ possono essere inseriti solo numeri. Se l’iniziativa non ha previsto alcun budget finanziario, indicare 0 €",
            'other_structure': "Rispondere solo se l’ente organizzatore è “Università della Calabria"
        }

    class Media:
        js = ('js/textarea-autosize.js',)


class PublicEngagementEventEvaluationForm(forms.Form):
    success = forms.BooleanField(
        label='Esito positivo', required=False, widget=BootstrapItaliaToggleWidget)
    notes = forms.CharField(label='Note', widget=forms.Textarea(
        attrs={'rows': 2}), required=False)

    def clean(self):
        cleaned_data = super().clean()

        success = cleaned_data.get('success')
        notes = cleaned_data.get('notes')

        if not success and not notes:
            self.add_error('notes', "Note obbligatore in caso di esito negativo")

        return cleaned_data

    class Media:
        js = ('js/textarea-autosize.js',)


class PublicEngagementStructureForm(forms.Form):
    structure = forms.IntegerField(label=_('Structure'),
                                    required=True,
                                    widget=BootstrapItaliaAPISelectStructureWidget())
