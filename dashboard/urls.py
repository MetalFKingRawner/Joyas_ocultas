from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('<slug:slug>/', views.dashboard_local, name='local'),
]