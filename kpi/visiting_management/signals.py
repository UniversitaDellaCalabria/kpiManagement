from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from . models import Visiting
import os


@receiver(pre_save, sender=Visiting)
def delete_old_files_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return False

    # Lista dei campi file da monitorare
    file_fields = ['document']

    for field_name in file_fields:
        old_file = getattr(old_instance, field_name)
        new_file = getattr(instance, field_name)

        # Se il file è cambiato (o rimosso), eliminiamo il vecchio dal disco
        if old_file and old_file != new_file:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

            
@receiver(post_delete, sender=Visiting)
def delete_master_files(sender, instance, **kwargs):
    """Elimina i file fisici quando viene eliminato un master"""
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)
