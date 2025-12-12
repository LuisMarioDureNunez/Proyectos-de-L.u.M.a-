#!/usr/bin/env python
"""
Test simple del sistema de login
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import UsuarioPersonalizado

def test_basico():
    """Test básico del sistema"""
    print("=" * 50)
    print("TEST BASICO DEL SISTEMA")
    print("=" * 50)
    
    # Verificar usuarios
    print("\n1. USUARIOS EN EL SISTEMA:")
    usuarios = UsuarioPersonalizado.objects.all()
    for user in usuarios:
        print(f"   - {user.username} (Rol: {user.rol}) - Activo: {user.is_active}")
    
    # Verificar admin
    admin = UsuarioPersonalizado.objects.filter(username='admin').first()
    if admin:
        print(f"\n2. USUARIO ADMIN: OK")
        print(f"   - Password correcto: {admin.check_password('123')}")
        print(f"   - Es superuser: {admin.is_superuser}")
        print(f"   - Es staff: {admin.is_staff}")
    else:
        print("\n2. USUARIO ADMIN: NO ENCONTRADO")
    
    print("\n3. URLS PARA PROBAR:")
    print("   http://127.0.0.1:8000/ - Inicio")
    print("   http://127.0.0.1:8000/accounts/login/ - Login normal")
    print("   http://127.0.0.1:8000/emergency-login/ - Login de emergencia")
    print("   http://127.0.0.1:8000/test-login/ - Pagina de prueba")
    
    print("\n4. CREDENCIALES DE PRUEBA:")
    print("   admin / 123")
    print("   constructor1 / 123")
    print("   cliente1 / 123")
    
    print("\n" + "=" * 50)
    print("EJECUTA: python manage.py runserver")
    print("=" * 50)

if __name__ == '__main__':
    test_basico()