from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import TarjetaFidelidad, ProgresoFidelidad


@login_required
@require_POST
def canjear(request, tarjeta_id):
    tarjeta = get_object_or_404(TarjetaFidelidad, id=tarjeta_id)
    progreso = get_object_or_404(ProgresoFidelidad, usuario=request.user, tarjeta=tarjeta)

    if progreso.recompensa_disponible:
        progreso.visitas_acumuladas -= tarjeta.visitas_requeridas
        progreso.recompensas_canjeadas += 1
        progreso.save()
        messages.success(request, f'¡Canjeaste tu recompensa en {tarjeta.local.nombre}: {tarjeta.recompensa_descripcion}!')
    else:
        messages.info(request, 'Aún no tienes suficientes visitas para canjear esta recompensa.')

    return redirect('locales:detalle', slug=tarjeta.local.slug)