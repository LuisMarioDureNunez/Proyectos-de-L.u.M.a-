# urls_mejoras.py - URLs para las nuevas funcionalidades increíbles
from django.urls import path
from .views_mejoras import *

urlpatterns = [
    # Dashboard Interactivo
    path('dashboard/interactivo/', dashboard_interactivo, name='dashboard_interactivo'),
    
    # Galería de Obras
    path('obras/galeria/', galeria_obras, name='galeria_obras'),
    
    # Calendario de Obras
    path('obras/calendario/', calendario_obras, name='calendario_obras'),
    
    # Notificaciones
    path('api/notificaciones/', api_notificaciones, name='api_notificaciones'),
    path('notificaciones/', lista_notificaciones, name='lista_notificaciones'),
    path('notificaciones/<int:notificacion_id>/leer/', marcar_notificacion_leida, name='marcar_notificacion_leida'),
    
    # Estadísticas
    path('api/estadisticas/', api_estadisticas_dashboard, name='api_estadisticas_dashboard'),
    
    # Búsqueda Global
    path('api/busqueda/', busqueda_global, name='busqueda_global'),
]