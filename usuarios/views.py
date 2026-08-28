from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import RegistroForm
from fidelidad.models import ProgresoFidelidad
from locales.models import Local


def registro(request):
    if request.user.is_authenticated:
        return redirect('home')

    next_url = request.POST.get('next') or request.GET.get('next') or 'home'
    ref_slug = request.POST.get('ref') or request.GET.get('ref')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            if ref_slug:
                local_referente = Local.objects.filter(slug=ref_slug).first()
                if local_referente:
                    user.perfilusuario.referido_por = local_referente
                    user.perfilusuario.save()
            login(request, user)
            return redirect(next_url)
    else:
        form = RegistroForm()

    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def mi_pasaporte(request):
    gemas = request.user.gemas.select_related('local', 'tipo_gema')
    progresos = ProgresoFidelidad.objects.filter(
        usuario=request.user, visitas_acumuladas__gt=0
    ).select_related('tarjeta__local')
    insignias = request.user.insignias.select_related('insignia')

    context = {'gemas': gemas, 'progresos': progresos, 'insignias': insignias}
    return render(request, 'usuarios/pasaporte.html', context)