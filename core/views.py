from django.shortcuts import render
from locales.models import Local, Mood


def home(request):
    locales_destacados = Local.objects.filter(activo=True).order_by('?')[:3]
    moods = Mood.objects.all()[:4]

    context = {
        'locales_destacados': locales_destacados,
        'moods': moods,
    }
    return render(request, 'core/home.html', context)