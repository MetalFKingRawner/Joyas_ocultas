import uuid

from django.conf import settings
from django.db import models

from locales.models import Local


class CodigoQR(models.Model):
    local = models.OneToOneField(Local, related_name='qr', on_delete=models.CASCADE)
    codigo_unico = models.CharField(max_length=64, unique=True, editable=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.codigo_unico:
            self.codigo_unico = uuid.uuid4().hex
        super().save(*args, **kwargs)

    def __str__(self):
        return f"QR de {self.local.nombre}"


class Visita(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visitas')
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='visitas')
    fecha_hora = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_hora']

    def __str__(self):
        return f"{self.usuario} visitó {self.local.nombre} el {self.fecha_hora:%d/%m/%Y}"


CALIFICACION_CHOICES = [(i, str(i)) for i in range(1, 6)]


class Resena(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resenas')
    local = models.ForeignKey(Local, on_delete=models.CASCADE, related_name='resenas')
    calificacion = models.PositiveSmallIntegerField(choices=CALIFICACION_CHOICES)
    comentario = models.TextField(max_length=500, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_edicion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'local')
        ordering = ['-fecha_edicion']

    def __str__(self):
        return f"{self.usuario} · {self.local.nombre} ({self.calificacion}★)"