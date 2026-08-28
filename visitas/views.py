import io

from django.urls import reverse
import qrcode
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone

from usuarios.models import GemaColeccionada
from .models import CodigoQR, Visita
from fidelidad.models import ProgresoFidelidad

from django.shortcuts import render
from locales.models import Local
from .forms import ResenaForm
from .models import Resena

def qr_imagen(request, codigo_unico):
    qr_obj = get_object_or_404(CodigoQR, codigo_unico=codigo_unico)
    url_escaneo = request.build_absolute_uri(f'/visitas/escanear/{codigo_unico}/')

    img = qrcode.make(url_escaneo)
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return HttpResponse(buffer.getvalue(), content_type='image/png')


def escanear(request, codigo_unico):
    qr_obj = get_object_or_404(CodigoQR, codigo_unico=codigo_unico)

    if not request.user.is_authenticated:
        return redirect('visitas:bienvenida', codigo_unico=codigo_unico)

    local = qr_obj.local
    usuario = request.user
    hoy = timezone.localtime().date()

    ya_visito_hoy = Visita.objects.filter(usuario=usuario, local=local, fecha_hora__date=hoy).exists()
    if ya_visito_hoy:
        messages.info(request, f'Ya registraste tu visita a {local.nombre} hoy. ¡Vuelve mañana!')
        return redirect('locales:detalle', slug=local.slug)

    Visita.objects.create(usuario=usuario, local=local)

    _, gema_nueva = GemaColeccionada.objects.get_or_create(
        usuario=usuario,
        local=local,
        defaults={'tipo_gema': local.gema_principal},
    )

    if gema_nueva:
        messages.success(request, f'¡Visita registrada! Desbloqueaste la gema {local.gema_principal.nombre} de {local.nombre}.')
    else:
        messages.success(request, f'¡Visita registrada en {local.nombre}!')

    tarjeta = getattr(local, 'tarjeta_fidelidad', None)
    if tarjeta and tarjeta.activa:
        progreso, _ = ProgresoFidelidad.objects.get_or_create(usuario=usuario, tarjeta=tarjeta)
        progreso.visitas_acumuladas += 1
        progreso.save()

        if progreso.recompensa_disponible:
            messages.success(request, f'¡Tu tarjeta de fidelidad en {local.nombre} está lista para canjear!')

    from usuarios.services import verificar_insignias
    nuevas_insignias = verificar_insignias(usuario)
    for insignia in nuevas_insignias:
        messages.success(request, f'¡Insignia desbloqueada! {insignia.nombre}')

    return redirect('locales:detalle', slug=local.slug)

@login_required
def escribir_resena(request, slug):
    local = get_object_or_404(Local, slug=slug)
    ha_visitado = Visita.objects.filter(usuario=request.user, local=local).exists()

    if not ha_visitado:
        messages.info(request, 'Necesitas visitar y escanear el QR de este local antes de poder reseñarlo.')
        return redirect('locales:detalle', slug=local.slug)

    resena, _ = Resena.objects.get_or_create(
        usuario=request.user, local=local, defaults={'calificacion': 5}
    )

    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Gracias por tu reseña verificada!')
            return redirect('locales:detalle', slug=local.slug)
    else:
        form = ResenaForm(instance=resena)

    return render(request, 'visitas/resena_form.html', {'form': form, 'local': local})

def bienvenida_negocio(request, codigo_unico):
    qr_obj = get_object_or_404(CodigoQR, codigo_unico=codigo_unico)
    local = qr_obj.local

    if request.user.is_authenticated:
        return redirect('visitas:escanear', codigo_unico=codigo_unico)

    url_escaneo = reverse('visitas:escanear', args=[codigo_unico])
    context = {
        'local': local,
        'url_login': f"{reverse('usuarios:login')}?next={url_escaneo}",
        'url_registro': f"{reverse('usuarios:registro')}?next={url_escaneo}&ref={local.slug}",
    }
    return render(request, 'visitas/bienvenida.html', context)