from django.db.models.signals import post_save
from django.dispatch import receiver

from locales.models import Local
from .models import CodigoQR


@receiver(post_save, sender=Local)
def crear_qr_local(sender, instance, created, **kwargs):
    if created:
        CodigoQR.objects.get_or_create(local=instance)