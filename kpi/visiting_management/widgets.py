import os
from django.forms.widgets import *
from django.urls import reverse


class BootstrapItaliaAPISelectVisitorWidget(Select):
    template_name = 'widgets/api_select_user.html'

    def __init__(self,  *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)


class BootstrapItaliaAPISelectStructureWidget(Select):
    template_name = 'widgets/api_select_structure.html'

    def __init__(self,  *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)


import os
from django.forms.widgets import ClearableFileInput
from django.urls import reverse


class UrlValueWrapper:
    """
    Un wrapper che espone un attributo .url modificabile 
    e si comporta come una stringa per il nome del file.
    """
    def __init__(self, original_file, custom_url):
        self.file = original_file
        self.url = custom_url # Qui non abbiamo il blocco della property

    def __str__(self):
        return str(self.file)

    def __getattr__(self, name):
        # Passa qualsiasi altra chiamata (es. .size, .path) al file originale
        return getattr(self.file, name)

        
class CustomFileWidget(ClearableFileInput):
        
    def render(self, name, value, attrs=None, renderer=None):
        # Qui hai accesso a 'name'
        self.current_field_name = name
        return super().render(name, value, attrs, renderer)
        
    def format_value(self, value):
        """
        'value' qui è l'oggetto FieldFile. 
        Se esiste, possiamo manipolare come appare nel link.
        """
        if value and hasattr(value, 'url'):
            response = None
            if self.current_field_name == 'document':
                response = reverse(
                    "visiting:download_document",
                    kwargs={
                        "structure_slug": self.attrs.structure_slug,
                        "pk": value.instance.visiting_pk
                    },
                )
                
            if response:
                return UrlValueWrapper("Download", response)
                
        return str(value)
