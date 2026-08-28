from django.contrib import admin
from .models import TipoGema, Mood, Local, FotoLocal


class FotoLocalInline(admin.TabularInline):
    model = FotoLocal
    extra = 1


@admin.register(Local)
class LocalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'gema_principal', 'rango_precio', 'es_socio_fundador', 'es_ficticio', 'activo']
    list_filter = ['gema_principal', 'es_ficticio', 'activo', 'moods']
    search_fields = ['nombre', 'descripcion_corta']
    prepopulated_fields = {'slug': ('nombre',)}
    filter_horizontal = ['moods']
    inlines = [FotoLocalInline]


admin.site.register(TipoGema)
admin.site.register(Mood)