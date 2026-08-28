from django.contrib import admin
from .models import PerfilUsuario, GemaColeccionada, Insignia, InsigniaUsuario

admin.site.register(PerfilUsuario)
admin.site.register(GemaColeccionada)
admin.site.register(Insignia)
admin.site.register(InsigniaUsuario)