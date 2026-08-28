from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Local, Mood
from django.db.models import Avg
from visitas.models import Visita, Resena


def detalle_local(request, slug):
    local = get_object_or_404(Local, slug=slug, activo=True)
    fotos = local.fotos.all()
    moods = local.moods.all()

    context = {
        'local': local,
        'fotos': fotos,
        'moods': moods,
    }
    return render(request, 'locales/detalle.html', context)

def explorar(request):
    mood_slug = request.GET.get('mood')
    moods = Mood.objects.all()
    ahora = timezone.localtime().time()

    mood_seleccionado = None
    if mood_slug:
        mood_seleccionado = Mood.objects.filter(slug=mood_slug).first()
        locales_qs = Local.objects.filter(activo=True, moods__slug=mood_slug).distinct()
    else:
        locales_qs = Local.objects.filter(activo=True)

    resultados = []
    for local in locales_qs:
        score = 0
        if mood_seleccionado:
            score += 70
        abierto_ahora = local.horario_apertura <= ahora <= local.horario_cierre
        if abierto_ahora:
            score += 30
        resultados.append({'local': local, 'score': score, 'abierto_ahora': abierto_ahora})

    resultados.sort(key=lambda r: r['score'], reverse=True)

    context = {
        'moods': moods,
        'mood_seleccionado': mood_seleccionado,
        'resultados': resultados,
    }
    return render(request, 'locales/explorar.html', context)

def detalle_local(request, slug):
    local = get_object_or_404(Local, slug=slug, activo=True)
    fotos = local.fotos.all()
    moods = local.moods.all()
    resenas = local.resenas.select_related('usuario').all()
    promedio = resenas.aggregate(Avg('calificacion'))['calificacion__avg']

    ha_visitado = False
    mi_resena = None
    if request.user.is_authenticated:
        ha_visitado = Visita.objects.filter(usuario=request.user, local=local).exists()
        mi_resena = resenas.filter(usuario=request.user).first()

    tarjeta_fidelidad = getattr(local, 'tarjeta_fidelidad', None)
    progreso_fidelidad = None
    if tarjeta_fidelidad and tarjeta_fidelidad.activa and request.user.is_authenticated:
        from fidelidad.models import ProgresoFidelidad
        progreso_fidelidad, _ = ProgresoFidelidad.objects.get_or_create(
            usuario=request.user, tarjeta=tarjeta_fidelidad
        )

    context = {
        'local': local,
        'fotos': fotos,
        'moods': moods,
        'resenas': resenas,
        'promedio': promedio,
        'ha_visitado': ha_visitado,
        'mi_resena': mi_resena,
        'tarjeta_fidelidad': tarjeta_fidelidad,
        'progreso_fidelidad': progreso_fidelidad,
    }
    return render(request, 'locales/detalle.html', context)