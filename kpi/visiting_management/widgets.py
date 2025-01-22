from django.forms.widgets import *


class BootstrapItaliaAPISelectVisitorWidget(Select):
    template_name = 'widgets/api_select_user.html'

    def __init__(self,  *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)


class BootstrapItaliaAPISelectStructureWidget(Select):
    template_name = 'widgets/api_select_structure.html'

    def __init__(self,  *attrs, **kwargs):
        super().__init__(*attrs, **kwargs)
