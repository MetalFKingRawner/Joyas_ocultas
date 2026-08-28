from django.urls import path
from . import views

app_name = 'visitas'

urlpatterns = [
    path('qr/<str:codigo_unico>.png', views.qr_imagen, name='qr_imagen'),
    path('bienvenida/<str:codigo_unico>/', views.bienvenida_negocio, name='bienvenida'),
    path('escanear/<str:codigo_unico>/', views.escanear, name='escanear'),
    path('resena/<slug:slug>/', views.escribir_resena, name='resena'),
]