from django.urls import path
from . import views

app_name = 'fidelidad'

urlpatterns = [
    path('canjear/<int:tarjeta_id>/', views.canjear, name='canjear'),
]