from django.urls import path
from . import views

app_name = 'locales'

urlpatterns = [
    path('explorar/', views.explorar, name='explorar'),
    path('local/<slug:slug>/', views.detalle_local, name='detalle'),
]