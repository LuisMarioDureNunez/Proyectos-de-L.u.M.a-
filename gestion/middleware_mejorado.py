# gestion/middleware_mejorado.py - MIDDLEWARE PROFESIONAL SIN BUCLES
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect
import re
import logging

logger = logging.getLogger(__name__)

class PermisosMiddlewareMejorado:
    """Middleware profesional de permisos sin bucles de redirección"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # Rutas completamente públicas (no requieren autenticación)
        self.rutas_publicas = [
            '/accounts/login/',
            '/accounts/logout/',
            '/registro/',
            '/admin/login/',
            '/static/',
            '/media/',
            '/favicon.ico',
            '/robots.txt',
            '/sitemap.xml'
        ]
        
        # Rutas que requieren autenticación pero no permisos especiales
        self.rutas_autenticadas = [
            '/dashboard/',
            '/perfil/',
            '/obras/',
            '/presupuestos/',
        ]
        
        # Rutas con permisos específicos
        self.rutas_con_permisos = {
            # Solo administradores
            r'^/materiales/': 'es_administrador',
            r'^/maquinarias/': 'es_administrador', 
            r'^/herramientas/': 'es_administrador',
            r'^/gestion/usuarios/': 'es_administrador',
            r'^/admin/usuarios/': 'es_administrador',
            r'^/reportes/': 'es_administrador',
            
            # Administradores y constructores
            r'^/obras/nueva/': 'puede_gestionar_obras',
            r'^/obras/editar/': 'puede_gestionar_obras',
            r'^/obras/eliminar/': 'puede_gestionar_obras',
            r'^/presupuestos/nuevo/': 'puede_gestionar_obras',
            r'^/presupuestos/replantear/': 'puede_gestionar_obras',
            
            # Solo clientes
            r'^/presupuestos/solicitar/': 'es_cliente',
            r'^/presupuestos/aceptar/': 'es_cliente',
            r'^/presupuestos/rechazar/': 'es_cliente',
        }

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        """Procesar vista y verificar permisos - SIN BUCLES"""
        
        # Obtener la ruta actual
        path = request.path
        
        # 1. SIEMPRE PERMITIR RUTAS PÚBLICAS Y DE LOGIN
        if self.es_ruta_publica(path) or self.es_ruta_de_login(path):
            return None
            
        # 2. VERIFICAR AUTENTICACIÓN SOLO PARA RUTAS PROTEGIDAS
        if not request.user.is_authenticated:
            # Solo redirigir si NO es una ruta de login/registro
            if path not in ['/accounts/login/', '/registro/', '/']:
                return HttpResponseRedirect(f'/accounts/login/?next={path}')
            return None
        
        # 3. VERIFICAR PERMISOS ESPECÍFICOS SOLO SI ESTÁ AUTENTICADO
        return self.verificar_permisos_especificos(request, path)
    
    def es_ruta_publica(self, path):
        """Verificar si la ruta es completamente pública"""
        return any(path.startswith(ruta) for ruta in self.rutas_publicas)
    
    def es_ruta_de_login(self, path):
        """Verificar si es una ruta de login/registro"""
        rutas_login = [
            '/accounts/login/',
            '/accounts/logout/', 
            '/registro/',
            '/admin/login/',
            '/test-login/',
            '/verificar-usuario/',
            '/cambiar-password/'
        ]
        return any(path.startswith(ruta) for ruta in rutas_login)
    
    def verificar_permisos_especificos(self, request, path):
        """Verificar permisos específicos para rutas protegidas"""
        
        # Verificar cada patrón de ruta con permisos
        for patron, metodo_permiso in self.rutas_con_permisos.items():
            if re.match(patron, path):
                # Verificar si el usuario tiene el permiso requerido
                if hasattr(request.user, metodo_permiso):
                    tiene_permiso = getattr(request.user, metodo_permiso)()
                    if not tiene_permiso:
                        messages.error(request, f'❌ No tienes permisos para acceder a esta sección')
                        return HttpResponseRedirect('/dashboard/')
                else:
                    # Si el método no existe, denegar acceso
                    messages.error(request, f'❌ Permisos no configurados correctamente')
                    return HttpResponseRedirect('/dashboard/')
                break
        
        return None

class AuditoriaMiddlewareMejorado:
    """Middleware mejorado para auditoría de acciones"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.logger = logging.getLogger('auditoria')
        
        # Acciones importantes a registrar
        self.acciones_importantes = {
            'POST': [
                '/obras/nueva/', '/obras/editar/', 
                '/presupuestos/solicitar/', '/presupuestos/nuevo/',
                '/materiales/nuevo/', '/materiales/editar/',
                '/maquinarias/nueva/', '/herramientas/nueva/',
                '/accounts/login/', '/registro/'
            ],
            'DELETE': [
                '/obras/eliminar/', '/presupuestos/eliminar/',
                '/materiales/eliminar/', '/maquinarias/eliminar/',
                '/herramientas/eliminar/'
            ],
            'GET': [
                '/admin/usuarios/', '/reportes/', '/dashboard/'
            ]
        }

    def __call__(self, request):
        # Registrar antes de procesar
        self.registrar_acceso(request)
        
        response = self.get_response(request)
        
        # Registrar después de procesar si es necesario
        if request.method in ['POST', 'DELETE'] and hasattr(request, 'user') and request.user.is_authenticated:
            self.registrar_accion_post(request, response)
            
        return response
    
    def registrar_acceso(self, request):
        """Registrar acceso a rutas importantes"""
        if not hasattr(request, 'user') or not request.user.is_authenticated:
            return
            
        path = request.path
        method = request.method
        
        # Verificar si es una acción importante
        if method in self.acciones_importantes:
            for ruta_importante in self.acciones_importantes[method]:
                if ruta_importante in path:
                    self.log_accion(request, f"ACCESO_{method}", path)
                    break
    
    def registrar_accion_post(self, request, response):
        """Registrar resultado de acciones POST/DELETE"""
        if response.status_code in [200, 201, 302]:  # Éxito
            self.log_accion(request, f"EXITO_{request.method}", request.path)
        elif response.status_code >= 400:  # Error
            self.log_accion(request, f"ERROR_{request.method}", request.path, response.status_code)
    
    def log_accion(self, request, tipo_accion, path, status_code=None):
        """Registrar acción en logs"""
        try:
            usuario = request.user.username if hasattr(request, 'user') and request.user.is_authenticated else 'Anónimo'
            ip = self.get_client_ip(request)
            user_agent = request.META.get('HTTP_USER_AGENT', 'Desconocido')[:100]
            
            mensaje = f"[{tipo_accion}] Usuario: {usuario} | IP: {ip} | Ruta: {path}"
            if status_code:
                mensaje += f" | Status: {status_code}"
            
            # Log en consola para desarrollo
            print(f"AUDITORIA: {mensaje}")
            
            # Log en archivo para producción
            self.logger.info(mensaje, extra={
                'usuario': usuario,
                'ip': ip,
                'path': path,
                'user_agent': user_agent,
                'tipo_accion': tipo_accion
            })
            
        except Exception as e:
            print(f"Error en auditoria: {e}")
    
    def get_client_ip(self, request):
        """Obtener IP real del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Desconocida')
        return ip

class SecurityMiddleware:
    """Middleware adicional de seguridad"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        
        # IPs bloqueadas (ejemplo)
        self.ips_bloqueadas = set()
        
        # Límite de intentos por IP
        self.intentos_por_ip = {}
        self.max_intentos = 10
    
    def __call__(self, request):
        # Verificar IP bloqueada
        client_ip = self.get_client_ip(request)
        
        if client_ip in self.ips_bloqueadas:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("IP bloqueada por seguridad")
        
        # Verificar límite de intentos
        if self.excede_limite_intentos(client_ip):
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Demasiados intentos. Intenta más tarde.")
        
        response = self.get_response(request)
        
        # Agregar headers de seguridad
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
    
    def get_client_ip(self, request):
        """Obtener IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
        return ip
    
    def excede_limite_intentos(self, ip):
        """Verificar si la IP excede el límite de intentos"""
        import time
        
        ahora = time.time()
        
        # Limpiar intentos antiguos (más de 1 hora)
        if ip in self.intentos_por_ip:
            self.intentos_por_ip[ip] = [
                timestamp for timestamp in self.intentos_por_ip[ip] 
                if ahora - timestamp < 3600  # 1 hora
            ]
        
        # Contar intentos recientes
        intentos_recientes = len(self.intentos_por_ip.get(ip, []))
        
        if intentos_recientes >= self.max_intentos:
            return True
        
        # Registrar intento actual
        if ip not in self.intentos_por_ip:
            self.intentos_por_ip[ip] = []
        self.intentos_por_ip[ip].append(ahora)
        
        return False