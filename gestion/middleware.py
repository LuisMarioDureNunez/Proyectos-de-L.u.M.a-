# gestion/middleware.py
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
import re

class PermisosMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Definir rutas y permisos requeridos
        self.rutas_protegidas = {
            # Administradores
            r'^/materiales/.*$': lambda u: u.is_authenticated and u.es_administrador(),
            r'^/maquinarias/.*$': lambda u: u.is_authenticated and u.es_administrador(),
            r'^/herramientas/.*$': lambda u: u.is_authenticated and u.es_administrador(),
            r'^/admin/usuarios/.*$': lambda u: u.is_authenticated and u.es_administrador(),
            
            # Constructores y Administradores
            r'^/obras/nueva/$': lambda u: u.is_authenticated and u.puede_gestionar_obras(),
            r'^/obras/editar/.*$': lambda u: u.is_authenticated and u.puede_gestionar_obras(),
            r'^/presupuestos/nuevo/$': lambda u: u.is_authenticated and u.puede_gestionar_obras(),
            
            # Clientes específicos
            r'^/presupuestos/solicitar/$': lambda u: u.is_authenticated and u.rol == 'cliente',
            r'^/presupuestos/aceptar/.*$': lambda u: u.is_authenticated and u.rol == 'cliente',
            r'^/presupuestos/rechazar/.*$': lambda u: u.is_authenticated and u.rol == 'cliente',
        }

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Rutas públicas que no requieren autenticación
        rutas_publicas = [
            '/accounts/login/',
            '/registro/',
            '/admin/',
            '/static/',
            '/media/',
            '/favicon.ico'
        ]
        
        # Si la ruta es pública, permitir acceso
        if any(request.path.startswith(ruta) for ruta in rutas_publicas):
            return None
        
        # Si no está autenticado, redirigir al login
        if not request.user.is_authenticated:
            messages.warning(request, '🔐 Debes iniciar sesión para acceder a esta página')
            return redirect(f'/accounts/login/?next={request.path}')

        # Verificar permisos para rutas protegidas
        for ruta_pattern, permiso_requerido in self.rutas_protegidas.items():
            if re.match(ruta_pattern, request.path):
                if not permiso_requerido(request.user):
                    messages.error(request, '❌ No tienes permisos para acceder a esta página')
                    return redirect('dashboard')
                break

        return None

class AuditoriaMiddleware:
    """Middleware para registrar actividades importantes"""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Registrar acciones importantes
        if request.user.is_authenticated and request.method in ['POST', 'DELETE']:
            self.registrar_accion(request)
            
        return response

    def registrar_accion(self, request):
        """Registrar acción en logs"""
        accion = f"{request.method} {request.path}"
        usuario = request.user.username
        ip = self.get_client_ip(request)
        
        # Solo registrar acciones importantes
        acciones_importantes = [
            '/obras/nueva', '/obras/editar', '/obras/eliminar',
            '/presupuestos/solicitar', '/presupuestos/aceptar', '/presupuestos/rechazar',
            '/materiales/nuevo', '/materiales/editar', '/materiales/eliminar',
        ]
        
        if any(accion in request.path for accion in acciones_importantes):
            print(f"🔍 AUDITORIA: {usuario} desde {ip} - {accion}")

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip