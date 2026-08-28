from django.conf import settings
from django.db import models

from locales.models import Local


class TarjetaFidelidad(models.Model):
    local = models.OneToOneField(Local, related_name='tarjeta_fidelidad', on_delete=models.CASCADE)
    visitas_requeridas = models.PositiveSmallIntegerField(default=5)
    recompensa_descripcion = models.CharField(max_length=200, help_text="Ej: Bebida gratis, 15% de descuento")
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"Fidelidad {self.local.nombre} ({self.visitas_requeridas} visitas)"


class ProgresoFidelidad(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='progresos_fidelidad')
    tarjeta = models.ForeignKey(TarjetaFidelidad, on_delete=models.CASCADE, related_name='progresos')
    visitas_acumuladas = models.PositiveSmallIntegerField(default=0)
    recompensas_canjeadas = models.PositiveSmallIntegerField(default=0)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('usuario', 'tarjeta')

    @property
    def recompensa_disponible(self):
        return self.visitas_acumuladas >= self.tarjeta.visitas_requeridas

    @property
    def porcentaje(self):
        return min(100, int((self.visitas_acumuladas / self.tarjeta.visitas_requeridas) * 100))

    def __str__(self):
        return f"{self.usuario} · {self.tarjeta.local.nombre} ({self.visitas_acumuladas}/{self.tarjeta.visitas_requeridas})"