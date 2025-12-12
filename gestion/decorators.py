from django.shortcuts import redirect
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from functools import wraps

def rol_requerido(roles_permitidos):
    """
    Decorator para verificar que el usuario tenga uno de los roles permitidos
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, '🔐 Debes iniciar sesión para acceder a esta página')
                return redirect('login')
            
            if request.user.es_administrador():
                return view_func(request, *args, **kwargs)
                
            if request.user.rol in roles_permitidos:
                return view_func(request, *args, **kwargs)
            
            messages.error(request, f'❌ No tienes permisos para acceder a esta sección. Se requiere: {", ".join(roles_permitidos)}')
            return redirect('dashboard')
        return _wrapped_view
    return decorator

def permiso_requerido(permiso):
    """
    Decorator para verificar permisos específicos
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, '🔐 Debes iniciar sesión')
                return redirect('login')
            
            if request.user.has_perm(permiso) or request.user.es_administrador():
                return view_func(request, *args, **kwargs)
            
            messages.error(request, f'❌ Permiso denegado. Se requiere: {permiso}')
            return redirect('dashboard')
        return _wrapped_view
    return decorator

# Decoradores específicos por rol
def admin_required(view_func):
    return rol_requerido(['admin'])(view_func)

def vendedor_required(view_func):
    return rol_requerido(['admin', 'vendedor'])(view_func)

def cliente_required(view_func):
    return rol_requerido(['admin', 'vendedor', 'cliente'])(view_func)

# Decoradores específicos por permiso
def puede_gestionar_productos(view_func):
    return permiso_requerido('gestion.puede_gestionar_productos')(view_func)

def puede_ver_reportes(view_func):
    return permiso_requerido('gestion.puede_ver_reportes')(view_func)

def puede_gestionar_usuarios(view_func):
    return permiso_requerido('gestion.puede_gestionar_usuarios')(view_func)