def _otorgar(usuario, slug):
    from .models import Insignia, InsigniaUsuario

    insignia = Insignia.objects.filter(slug=slug).first()
    if not insignia:
        return []

    _, creada = InsigniaUsuario.objects.get_or_create(usuario=usuario, insignia=insignia)
    return [insignia] if creada else []


def verificar_insignias(usuario):
    from locales.models import TipoGema
    from visitas.models import Visita

    nuevas = []
    gemas = usuario.gemas.select_related('tipo_gema')

    conteo_por_gema = {}
    for g in gemas:
        conteo_por_gema[g.tipo_gema.nombre] = conteo_por_gema.get(g.tipo_gema.nombre, 0) + 1

    if conteo_por_gema.get('Rubí', 0) >= 5:
        nuevas += _otorgar(usuario, 'cazador-de-rubies')

    visitas_amatista = Visita.objects.filter(
        usuario=usuario, local__gema_principal__nombre='Amatista'
    ).count()
    if visitas_amatista >= 10:
        nuevas += _otorgar(usuario, 'coleccionista-de-amatistas')

    total_tipos = TipoGema.objects.count()
    tipos_coleccionados = gemas.values('tipo_gema').distinct().count()
    if total_tipos and tipos_coleccionados >= total_tipos:
        nuevas += _otorgar(usuario, 'maestro-joyero')

    return nuevas