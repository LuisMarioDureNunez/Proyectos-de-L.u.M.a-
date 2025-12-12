from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Crear un router para las vistas de la API
router = DefaultRouter()

# Registrar solo las vistas que existen en tu views.py
router.register('materiales', views.MaterialViewSet, basename='materiales')
router.register('obras', views.ObraViewSet, basename='obras') 
router.register('presupuestos', views.PresupuestoViewSet, basename='presupuestos')
router.register('notificaciones', views.NotificacionViewSet, basename='notificaciones')

urlpatterns = [
    # Endpoints de autenticación
    path('auth/login/', views.LoginAPIView.as_view(), name='api_login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('auth/profile/', views.UserProfileAPIView.as_view(), name='api_profile'),
    
    # Dashboard
    path('dashboard/', views.DashboardAPIView.as_view(), name='api_dashboard'),
    
    # Presupuesto rápido
    path('presupuesto-rapido/', views.PresupuestoRapidoAPIView.as_view(), name='api_presupuesto_rapido'),
    
    # Incluir rutas del router
    path('', include(router.urls)),
]

# Endpoint home de la API
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_home(request):
    return Response({
        'message': 'Bienvenido a la API de Gestión de Obras',
        'endpoints': {
            'auth': {
                'login': '/api/v1/auth/login/',
                'logout': '/api/v1/auth/logout/',
                'profile': '/api/v1/auth/profile/',
            },
            'data': {
                'materiales': '/api/v1/materiales/',
                'obras': '/api/v1/obras/',
                'presupuestos': '/api/v1/presupuestos/',
                'notificaciones': '/api/v1/notificaciones/',
            },
            'dashboard': '/api/v1/dashboard/',
            'presupuesto_rapido': '/api/v1/presupuesto-rapido/',
        },
        'version': '1.0'
    })

# Agregar el home a las URLs
urlpatterns.insert(0, path('', api_home, name='api_home'))