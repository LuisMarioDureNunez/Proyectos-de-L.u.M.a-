# gestion/views_auth.py - VISTAS DE AUTENTICACIÓN MEJORADAS
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from .models import UsuarioPersonalizado
from .forms import FormularioRegistro
import logging

logger = logging.getLogger(__name__)

class LoginMejoradoView(View):
    """Vista de login mejorada sin bucles de redirección"""
    
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Si ya está autenticado, redirigir al dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        """Mostrar formulario de login"""
        form = self.form_class()
        context = {
            'form': form,
            'next': request.GET.get('next', ''),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Procesar login"""
        form = self.form_class(data=request.POST)
        next_url = request.POST.get('next') or request.GET.get('next') or '/dashboard/'
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Autenticar usuario
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    # Login exitoso
                    login(request, user)
                    
                    # Log de auditoría
                    logger.info(f"Login exitoso: {username} desde {self.get_client_ip(request)}")
                    
                    # Mensaje de bienvenida
                    messages.success(
                        request, 
                        f'¡Bienvenido {user.get_full_name() or user.username}! 🎉'
                    )
                    
                    # Redirigir según el rol
                    if next_url and next_url != '/':
                        return HttpResponseRedirect(next_url)
                    else:
                        return redirect('dashboard')
                else:
                    # Usuario inactivo
                    messages.error(request, '❌ Tu cuenta está desactivada. Contacta al administrador.')
                    logger.warning(f"Intento de login con cuenta inactiva: {username}")
            else:
                # Credenciales incorrectas
                messages.error(request, '❌ Usuario o contraseña incorrectos.')
                logger.warning(f"Intento de login fallido: {username} desde {self.get_client_ip(request)}")
        else:
            # Errores de formulario
            messages.error(request, '❌ Por favor, corrige los errores en el formulario.')
        
        # Si llegamos aquí, hubo un error
        context = {
            'form': form,
            'next': next_url,
        }
        return render(request, self.template_name, context)
    
    def get_client_ip(self, request):
        """Obtener IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Desconocida')
        return ip

class RegistroMejoradoView(View):
    """Vista de registro mejorada"""
    
    template_name = 'registration/registro.html'
    form_class = FormularioRegistro
    
    def dispatch(self, request, *args, **kwargs):
        # Si ya está autenticado, redirigir al dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        """Mostrar formulario de registro"""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """Procesar registro"""
        form = self.form_class(request.POST)
        
        if form.is_valid():
            try:
                # Crear usuario
                user = form.save(commit=False)
                user.rol = 'cliente'  # Por defecto, nuevos usuarios son clientes
                user.save()
                
                # Login automático
                login(request, user)
                
                # Log de auditoría
                logger.info(f"Nuevo registro: {user.username} desde {self.get_client_ip(request)}")
                
                # Mensaje de éxito
                messages.success(
                    request, 
                    f'¡Cuenta creada exitosamente! Bienvenido {user.get_full_name() or user.username} 🎉'
                )
                
                return redirect('dashboard')
                
            except Exception as e:
                logger.error(f"Error en registro: {e}")
                messages.error(request, '❌ Error al crear la cuenta. Intenta nuevamente.')
        else:
            messages.error(request, '❌ Por favor, corrige los errores en el formulario.')
        
        return render(request, self.template_name, {'form': form})
    
    def get_client_ip(self, request):
        """Obtener IP del cliente"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', 'Desconocida')
        return ip

@login_required
def logout_mejorado(request):
    """Logout mejorado con mensaje"""
    username = request.user.username
    
    # Log de auditoría
    logger.info(f"Logout: {username} desde {request.META.get('REMOTE_ADDR', 'Desconocida')}")
    
    # Logout
    logout(request)
    
    # Mensaje de despedida
    messages.info(request, f'👋 Hasta luego, {username}. Sesión cerrada correctamente.')
    
    return redirect('home')

def verificar_estado_usuario(request):
    """Vista para verificar el estado del usuario (AJAX)"""
    if request.user.is_authenticated:
        return JsonResponse({
            'authenticated': True,
            'username': request.user.username,
            'rol': request.user.rol,
            'full_name': request.user.get_full_name(),
        })
    else:
        return JsonResponse({'authenticated': False})

@csrf_protect
def cambiar_password(request):
    """Vista para cambiar contraseña"""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirmacion = request.POST.get('password_confirmacion')
        
        # Validaciones
        if not request.user.check_password(password_actual):
            messages.error(request, '❌ La contraseña actual es incorrecta.')
        elif password_nueva != password_confirmacion:
            messages.error(request, '❌ Las contraseñas nuevas no coinciden.')
        elif len(password_nueva) < 8:
            messages.error(request, '❌ La contraseña debe tener al menos 8 caracteres.')
        else:
            # Cambiar contraseña
            request.user.set_password(password_nueva)
            request.user.save()
            
            # Log de auditoría
            logger.info(f"Cambio de contraseña: {request.user.username}")
            
            messages.success(request, '✅ Contraseña cambiada exitosamente.')
            return redirect('gestionar_perfil')
    
    return render(request, 'registration/cambiar_password.html')

def test_login(request):
    """Vista de prueba para verificar que el login funciona"""
    context = {
        'usuarios_demo': [
            {'username': 'admin', 'password': '123', 'rol': 'Administrador'},
            {'username': 'constructor1', 'password': '123', 'rol': 'Constructor'},
            {'username': 'cliente1', 'password': '123', 'rol': 'Cliente'},
            {'username': 'vendedor1', 'password': '123', 'rol': 'Vendedor'},
        ]
    }
    return render(request, 'registration/test_login.html', context)