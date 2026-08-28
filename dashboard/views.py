import datetime

from django.db.models import Count
from django.db.models.functions import ExtractHour
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from locales.models import Local
from visitas.models import Visita
from usuarios.models import GemaColeccionada
from fidelidad.models import ProgresoFidelidad


def dashboard_local(request, slug):
    local = get_object_or_404(Local, slug=slug)
    hoy = timezone.localdate()

    visitas_qs = Visita.objects.filter(local=local)
    total_visitas = visitas_qs.count()
    visitantes_unicos = visitas_qs.values('usuario').distinct().count()
    visitas_hoy = visitas_qs.filter(fecha_hora__date=hoy).count()

    clientes_recurrentes = (
        visitas_qs.values('usuario')
        .annotate(total=Count('id'))
        .filter(total__gt=1)
        .count()
    )

    hora_pico_qs = (
        visitas_qs.annotate(hora=ExtractHour('fecha_hora'))
        .values('hora')
        .annotate(total=Count('id'))
        .order_by('-total')[:3]
    )

    dias = [hoy - datetime.timedelta(days=i) for i in range(6, -1, -1)]
    visitas_por_dia = []
    for dia in dias:
        total = visitas_qs.filter(fecha_hora__date=dia).count()
        visitas_por_dia.append({'fecha': dia, 'total': total})
    maximo = max((d['total'] for d in visitas_por_dia), default=0) or 1
    for d in visitas_por_dia:
        d['porcentaje'] = int((d['total'] / maximo) * 100)

    gemas_otorgadas = GemaColeccionada.objects.filter(local=local).count()

    recompensas_canjeadas = 0
    tarjeta = getattr(local, 'tarjeta_fidelidad', None)
    if tarjeta:
        recompensas_canjeadas = sum(
            ProgresoFidelidad.objects.filter(tarjeta=tarjeta).values_list('recompensas_canjeadas', flat=True)
        )

    visitas_recientes = visitas_qs.select_related('usuario')[:8]

    usuarios_referidos = local.usuarios_referidos.count()

    context = {
        'local': local,
        'total_visitas': total_visitas,
        'visitantes_unicos': visitantes_unicos,
        'visitas_hoy': visitas_hoy,
        'clientes_recurrentes': clientes_recurrentes,
        'hora_pico_qs': hora_pico_qs,
        'visitas_por_dia': visitas_por_dia,
        'gemas_otorgadas': gemas_otorgadas,
        'recompensas_canjeadas': recompensas_canjeadas,
        'visitas_recientes': visitas_recientes,
        'tarjeta': tarjeta,
        'usuarios_referidos': usuarios_referidos,
    }
    return render(request, 'dashboard/dashboard_local.html', context)