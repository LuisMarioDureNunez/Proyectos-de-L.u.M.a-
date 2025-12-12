# gestion/views_login_simple.py - LOGIN ULTRA SIMPLE
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)

@csrf_protect
def login_ultra_simple(request):
    """Vista de login ultra simple que siempre funciona"""
    
    # Si ya está autenticado, ir al dashboard
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    
    # Procesar POST
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None and user.is_active:
                login(request, user)
                messages.success(request, f'Bienvenido {user.username}!')
                
                # Redirigir al dashboard
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url and next_url != '/':
                    return redirect(next_url)
                return redirect('/dashboard/')
            else:
                messages.error(request, 'Usuario o contrasena incorrectos.')
        else:
            messages.error(request, 'Completa todos los campos.')
    
    # Mostrar formulario siempre
    return render(request, 'registration/login.html', {
        'next': request.GET.get('next', '')
    })

def test_debug(request):
    """Vista de debug para probar"""
    from gestion.models import UsuarioPersonalizado
    
    usuarios = UsuarioPersonalizado.objects.all()[:5]
    usuarios_html = '<br>'.join([f'{u.username} ({u.rol}) - Activo: {u.is_active}' for u in usuarios])
    
    return HttpResponse(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Debug - Sistema LUMA</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .info {{ background: #f0f0f0; padding: 15px; margin: 10px 0; border-radius: 5px; }}
            .success {{ background: #d4edda; color: #155724; }}
            .error {{ background: #f8d7da; color: #721c24; }}
            a {{ color: #007bff; text-decoration: none; margin: 0 10px; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>🔍 DEBUG - Sistema LUMA</h1>
        
        <div class="info">
            <h3>Estado del Usuario</h3>
            <p><strong>Autenticado:</strong> {request.user.is_authenticated}</p>
            <p><strong>Usuario:</strong> {request.user}</p>
            <p><strong>Es superuser:</strong> {getattr(request.user, 'is_superuser', False)}</p>
        </div>
        
        <div class="info">
            <h3>Información de la Petición</h3>
            <p><strong>Método:</strong> {request.method}</p>
            <p><strong>Ruta:</strong> {request.path}</p>
            <p><strong>GET params:</strong> {dict(request.GET)}</p>
            <p><strong>POST params:</strong> {dict(request.POST) if request.method == 'POST' else 'N/A'}</p>
        </div>
        
        <div class="info">
            <h3>Usuarios en el Sistema</h3>
            <p>{usuarios_html}</p>
        </div>
        
        <div class="info">
            <h3>Enlaces de Prueba</h3>
            <a href="/accounts/login/">🔐 Login</a>
            <a href="/dashboard/">📊 Dashboard</a>
            <a href="/">🏠 Inicio</a>
            <a href="/emergency-login/">🚨 Login Emergencia</a>
            <a href="/test-login/">🧪 Test Login</a>
        </div>
        
        <div class="info">
            <h3>Test Rápido de Login</h3>
            <form method="post" action="/accounts/login/" style="display: inline-block; margin: 10px;">
                <input type="hidden" name="csrfmiddlewaretoken" value="{request.META.get('CSRF_COOKIE', 'test')}">
                <input type="hidden" name="username" value="admin">
                <input type="hidden" name="password" value="123">
                <button type="submit" style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer;">
                    Login como Admin
                </button>
            </form>
        </div>
        
        <p><small>Timestamp: {request.META.get('HTTP_DATE', 'N/A')}</small></p>
    </body>
    </html>
    """)