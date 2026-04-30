from django.apps import AppConfig


class VisitingManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'visiting_management'

    def ready(self):
        import visiting_management.signals  
