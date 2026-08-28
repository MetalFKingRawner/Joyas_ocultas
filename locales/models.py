from django.db import models
from django.utils.text import slugify


class TipoGema(models.Model):
    nombre = models.CharField(max_length=50)
    color_hex = models.CharField(max_length=7)
    descripcion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nombre


class Mood(models.Model):
    nombre = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, null=True)
    icono = models.CharField(max_length=50, blank=True)
    descripcion = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class Local(models.Model):
    RANGO_PRECIO_CHOICES = [
        ('$', '$'),
        ('$$', '$$'),
        ('$$$', '$$$'),
    ]

    nombre = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    descripcion_corta = models.CharField(max_length=200)
    historia = models.TextField(help_text="Storytelling del fundador/local")

    direccion = models.CharField(max_length=200)
    latitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitud = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    telefono = models.CharField(max_length=20, blank=True)

    rango_precio = models.CharField(max_length=3, choices=RANGO_PRECIO_CHOICES, default='$')
    horario_apertura = models.TimeField()
    horario_cierre = models.TimeField()
    dias_operacion = models.CharField(max_length=100, help_text="Ej: Lun-Sáb")

    moods = models.ManyToManyField(Mood, related_name='locales')
    gema_principal = models.ForeignKey(TipoGema, on_delete=models.PROTECT, related_name='locales_principales')

    es_camaleonico = models.BooleanField(default=False, help_text="¿Cambia de gema/mood según la hora?")
    gema_secundaria = models.ForeignKey(
        TipoGema, null=True, blank=True,
        related_name='locales_secundarios', on_delete=models.SET_NULL
    )

    es_socio_fundador = models.BooleanField(default=False)
    es_ficticio = models.BooleanField(default=True, help_text="Marca si es un local de demo, no un negocio real")
    activo = models.BooleanField(default=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre


class FotoLocal(models.Model):
    local = models.ForeignKey(Local, related_name='fotos', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='locales/')
    es_portada = models.BooleanField(default=False)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"Foto de {self.local.nombre}"