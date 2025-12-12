#!/usr/bin/env python
"""
Test del login paso a paso
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from django.test import Client
from django.contrib.auth import authenticate
from gestion.models import UsuarioPersonalizado

def test_login_completo():
    """Test completo del login paso a paso"""
    print("=" * 60)
    print("TEST LOGIN PASO A PASO")
    print("=" * 60)
    
    # 1. Verificar usuario admin
    print("\n1. VERIFICANDO USUARIO ADMIN:")
    try:
        admin = UsuarioPersonalizado.objects.get(username='admin')
        print(f"   - Usuario encontrado: {admin.username}")
        print(f"   - Activo: {admin.is_active}")
        print(f"   - Staff: {admin.is_staff}")
        print(f"   - Superuser: {admin.is_superuser}")
        
        # Test de contraseña
        password_ok = admin.check_password('123')
        print(f"   - Password '123' correcta: {password_ok}")
        
        if not password_ok:
            print("   - ARREGLANDO PASSWORD...")
            admin.set_password('123')
            admin.save()
            print("   - Password actualizada")
            
    except UsuarioPersonalizado.DoesNotExist:
        print("   - ERROR: Usuario admin no encontrado")
        return False
    
    # 2. Test de autenticación Django
    print("\n2. TEST DE AUTENTICACION DJANGO:")
    user = authenticate(username='admin', password='123')
    if user:
        print(f"   - Autenticación exitosa: {user.username}")
    else:
        print("   - ERROR: Autenticación falló")
        return False
    
    # 3. Test de cliente HTTP
    print("\n3. TEST DE CLIENTE HTTP:")
    client = Client()
    
    # Test GET del login
    response = client.get('/accounts/login/')
    print(f"   - GET /accounts/login/: {response.status_code}")
    
    if response.status_code != 200:
        print("   - ERROR: Login no accesible")
        return False
    
    # Test POST del login
    login_data = {
        'username': 'admin',
        'password': '123'
    }
    
    response = client.post('/accounts/login/', login_data, follow=True)
    print(f"   - POST /accounts/login/: {response.status_code}")
    print(f"   - Redirecciones: {len(response.redirect_chain)}")
    
    if response.redirect_chain:
        for redirect in response.redirect_chain:
            print(f"     -> {redirect[0]} ({redirect[1]})")
    
    # 4. Verificar sesión
    print("\n4. VERIFICANDO SESION:")
    if hasattr(response, 'wsgi_request') and hasattr(response.wsgi_request, 'user'):
        user_in_session = response.wsgi_request.user
        print(f"   - Usuario en sesión: {user_in_session}")
        print(f"   - Autenticado: {user_in_session.is_authenticated}")
    else:
        print("   - No se puede verificar la sesión")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETADO")
    print("=" * 60)
    
    return True

def mostrar_urls_debug():
    """Mostrar URLs para debug"""
    print("\nURLs PARA DEBUG:")
    print("http://127.0.0.1:8000/debug/ - Información de debug")
    print("http://127.0.0.1:8000/accounts/login/ - Login simple")
    print("http://127.0.0.1:8000/emergency-login/ - Login de emergencia")
    print("http://127.0.0.1:8000/test-login/ - Página de pruebas")

if __name__ == '__main__':
    test_login_completo()
    mostrar_urls_debug()
    
    print("\nINSTRUCCIONES:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Ve a: http://127.0.0.1:8000/debug/")
    print("3. Luego prueba: http://127.0.0.1:8000/accounts/login/")
    print("4. Usa: admin / 123")