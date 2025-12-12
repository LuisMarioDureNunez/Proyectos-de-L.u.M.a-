#!/usr/bin/env python
"""
Script de diagnóstico para verificar el sistema de login
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from gestion.models import UsuarioPersonalizado

def diagnosticar_sistema():
    """Diagnosticar el sistema de login"""
    print("=" * 60)
    print("DIAGNOSTICO DEL SISTEMA DE LOGIN")
    print("=" * 60)
    
    # 1. Verificar usuarios
    print("\n1. VERIFICANDO USUARIOS:")
    usuarios = UsuarioPersonalizado.objects.all()
    if usuarios.exists():
        for user in usuarios:
            print(f"   OK {user.username} ({user.get_rol_display()}) - Activo: {user.is_active}")
    else:
        print("   ERROR No hay usuarios en el sistema")
        return False
    
    # 2. Verificar URLs
    print("\n2. VERIFICANDO URLS:")
    client = Client()
    
    urls_test = [
        ('home', '/'),
        ('login', '/accounts/login/'),
        ('registro', '/registro/'),
        ('test_login', '/test-login/'),
    ]
    
    for name, url in urls_test:
        try:
            response = client.get(url)
            status = "OK" if response.status_code in [200, 302] else "ERROR"
            print(f"   {status} {name}: {url} -> {response.status_code}")
        except Exception as e:
            print(f"   ERROR {name}: {url} -> ERROR: {e}")
    
    # 3. Test de login
    print("\n3. PROBANDO LOGIN:")
    try:
        # Intentar login con admin
        admin_user = UsuarioPersonalizado.objects.filter(username='admin').first()
        if admin_user:
            login_data = {
                'username': 'admin',
                'password': '123'
            }
            response = client.post('/accounts/login/', login_data)
            if response.status_code == 302:  # Redirección = login exitoso
                print("   OK Login con admin: EXITOSO")
            else:
                print(f"   ERROR Login con admin: FALLO ({response.status_code})")
        else:
            print("   ERROR Usuario admin no encontrado")
    except Exception as e:
        print(f"   ERROR en test de login: {e}")
    
    # 4. Verificar middleware
    print("\n4. VERIFICANDO MIDDLEWARE:")
    from django.conf import settings
    middleware_activo = 'gestion.middleware_mejorado.PermisosMiddlewareMejorado' in settings.MIDDLEWARE
    print(f"   {'OK' if middleware_activo else 'ERROR'} Middleware de permisos: {'ACTIVO' if middleware_activo else 'INACTIVO'}")
    
    # 5. Verificar configuracion
    print("\n5. VERIFICANDO CONFIGURACION:")
    print(f"   OK LOGIN_URL: {settings.LOGIN_URL}")
    print(f"   OK LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
    print(f"   OK LOGOUT_REDIRECT_URL: {settings.LOGOUT_REDIRECT_URL}")
    print(f"   OK AUTH_USER_MODEL: {settings.AUTH_USER_MODEL}")
    
    print("\n" + "=" * 60)
    print("DIAGNOSTICO COMPLETADO")
    print("=" * 60)
    
    return True

def crear_usuario_test():
    """Crear usuario de prueba si no existe"""
    try:
        if not UsuarioPersonalizado.objects.filter(username='admin').exists():
            admin = UsuarioPersonalizado.objects.create_user(
                username='admin',
                email='admin@test.com',
                password='123',
                rol='admin',
                is_staff=True,
                is_superuser=True
            )
            print(f"OK Usuario admin creado: {admin.username}")
        else:
            print("OK Usuario admin ya existe")
    except Exception as e:
        print(f"ERROR creando usuario: {e}")

def mostrar_urls_disponibles():
    """Mostrar todas las URLs disponibles"""
    print("\nURLS DISPONIBLES:")
    print("   http://127.0.0.1:8000/ - Página de inicio")
    print("   http://127.0.0.1:8000/accounts/login/ - Login")
    print("   http://127.0.0.1:8000/registro/ - Registro")
    print("   http://127.0.0.1:8000/dashboard/ - Dashboard")
    print("   http://127.0.0.1:8000/test-login/ - Página de prueba")
    print("   http://127.0.0.1:8000/admin/ - Admin de Django")

if __name__ == '__main__':
    crear_usuario_test()
    diagnosticar_sistema()
    mostrar_urls_disponibles()
    
    print("\nINSTRUCCIONES:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Abre: http://127.0.0.1:8000/test-login/")
    print("3. Usa las credenciales: admin / 123")
    print("4. Si hay problemas, revisa este diagnóstico")