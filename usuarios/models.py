from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from locales.models import Local, TipoGema
from django.utils.text import slugify


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_explorador = models.CharField(max_length=50, blank=True)
    foto_perfil = models.ImageField(upload_to='perfiles/', blank=True, null=True)
    referido_por = models.ForeignKey(
        'locales.Local', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='usuarios_referidos'
    )
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_explorador or self.user.username

    @property
    def nombre_visible(self):
        return self.nombre_explorador or self.user.username


@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        PerfilUsuario.objects.get_or_create(user=instance)

class GemaColeccionada(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gemas')
    local = models.ForeignKey(Local, on_delete=models.CASCADE)
    tipo_gema = models.ForeignKey(TipoGema, on_delete=models.PROTECT)
    fecha_obtenida = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'local')
        ordering = ['-fecha_obtenida']

    def __str__(self):
        return f"{self.usuario} · {self.tipo_gema.nombre} de {self.local.nombre}"

class Insignia(models.Model):
    nombre = models.CharField(max_length=60)
    slug = models.SlugField(unique=True, blank=True)
    descripcion = models.CharField(max_length=200)
    icono = models.CharField(max_length=50, default='award')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class InsigniaUsuario(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='insignias')
    insignia = models.ForeignKey(Insignia, on_delete=models.CASCADE)
    fecha_obtenida = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'insignia')
        ordering = ['-fecha_obtenida']

    def __str__(self):
        return f"{self.usuario} · {self.insignia.nombre}"