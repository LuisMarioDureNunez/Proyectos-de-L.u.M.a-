# gestion/context_processors.py
from django.conf import settings
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

def configuracion_global(request):
    """Context processor para variables globales del sistema"""
    
    # Información básica del sistema
    context = {
        'SITE_NAME': 'Mi Tienda Premium',
        'SITE_VERSION': '2.0.0',
        'COPYRIGHT_YEAR': datetime.now().year,
        'COMPANY_NAME': 'Luma Construction & Tech',
        'SUPPORT_EMAIL': 'soporte@mitienda.com',
        'DEBUG_MODE': settings.DEBUG,
    }
    
    # Información del usuario si está autenticado
    if request.user.is_authenticated:
        context.update({
            'USER_ROLE': getattr(request.user, 'rol', 'cliente'),
            'USER_PERMISSIONS': get_user_permissions(request.user),
            'USER_AVATAR': getattr(request.user, 'avatar', None),
            'USER_FULL_NAME': request.user.get_full_name() or request.user.username,
        })
        
        # Estadísticas rápidas para el dashboard
        if hasattr(request.user, 'es_administrador') and request.user.es_administrador():
            context.update(get_admin_stats())
    
    # Configuración de la aplicación
    context.update({
        'CURRENCY_SYMBOL': 'Gs.',
        'CURRENCY_CODE': 'PYG',
        'TIMEZONE': settings.TIME_ZONE,
        'LANGUAGE_CODE': settings.LANGUAGE_CODE,
        'MEDIA_URL': settings.MEDIA_URL,
        'STATIC_URL': settings.STATIC_URL,
    })
    
    return context

def get_user_permissions(user):
    """Obtener permisos del usuario para el frontend"""
    permissions = []
    
    if hasattr(user, 'es_administrador') and user.es_administrador():
        permissions.extend([
            'puede_ver_dashboard',
            'puede_gestionar_productos',
            'puede_ver_reportes',
            'puede_gestionar_usuarios',
            'puede_crear_producto',
            'puede_editar_producto',
            'puede_eliminar_producto',
        ])
    elif hasattr(user, 'es_vendedor') and user.es_vendedor():
        permissions.extend([
            'puede_ver_dashboard',
            'puede_gestionar_productos',
            'puede_ver_reportes',
            'puede_crear_producto',
            'puede_editar_producto',
        ])
    else:
        permissions.append('puede_ver_dashboard')
    
    return permissions

def get_admin_stats():
    """Obtener estadísticas rápidas para administradores"""
    try:
        from .models import Producto, Pedido
        
        return {
            'TOTAL_PRODUCTOS': Producto.objects.count(),
            'PRODUCTOS_BAJO_STOCK': Producto.objects.filter(stock__lt=10).count(),
            'PEDIDOS_PENDIENTES': Pedido.objects.filter(estado='pendiente').count() if hasattr(Pedido, 'objects') else 0,
            'USUARIOS_ACTIVOS': User.objects.filter(is_active=True).count(),
        }
    except Exception as e:
        # En caso de error, devolver estadísticas vacías
        return {
            'TOTAL_PRODUCTOS': 0,
            'PRODUCTOS_BAJO_STOCK': 0,
            'PEDIDOS_PENDIENTES': 0,
            'USUARIOS_ACTIVOS': 0,
        }

def info_sistema(request):
    """Context processor legacy - mantener por compatibilidad"""
    return {
        'SITE_NAME': 'Mi Tienda Premium',
        'SITE_VERSION': '2.0.0',
        'COPYRIGHT_YEAR': datetime.now().year,
    }