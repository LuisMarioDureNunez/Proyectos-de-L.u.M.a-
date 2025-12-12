#!/usr/bin/env python
"""
Script para crear un superusuario automáticamente
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import UsuarioPersonalizado

def crear_superuser():
    """Crear superusuario si no existe"""
    try:
        # Verificar si ya existe un superusuario
        if UsuarioPersonalizado.objects.filter(is_superuser=True).exists():
            print("Ya existe un superusuario")
            return
        
        # Crear superusuario
        admin = UsuarioPersonalizado.objects.create_user(
            username='admin',
            email='admin@luma.py',
            password='123',
            first_name='Administrador',
            last_name='LUMA',
            rol='admin',
            is_staff=True,
            is_superuser=True
        )
        
        print("Superusuario creado exitosamente:")
        print(f"   Usuario: admin")
        print(f"   Contraseña: 123")
        print(f"   Email: admin@luma.py")
        
    except Exception as e:
        print(f"Error al crear superusuario: {e}")

def crear_usuarios_demo():
    """Crear usuarios de demostración"""
    usuarios_demo = [
        {
            'username': 'constructor1',
            'email': 'constructor@luma.py',
            'password': '123',
            'first_name': 'Juan',
            'last_name': 'Constructor',
            'rol': 'constructor'
        },
        {
            'username': 'cliente1',
            'email': 'cliente@luma.py',
            'password': '123',
            'first_name': 'María',
            'last_name': 'Cliente',
            'rol': 'cliente'
        },
        {
            'username': 'vendedor1',
            'email': 'vendedor@luma.py',
            'password': '123',
            'first_name': 'Carlos',
            'last_name': 'Vendedor',
            'rol': 'vendedor'
        }
    ]
    
    for usuario_data in usuarios_demo:
        try:
            if not UsuarioPersonalizado.objects.filter(username=usuario_data['username']).exists():
                UsuarioPersonalizado.objects.create_user(**usuario_data)
                print(f"Usuario {usuario_data['username']} creado")
            else:
                print(f"Usuario {usuario_data['username']} ya existe")
        except Exception as e:
            print(f"Error creando {usuario_data['username']}: {e}")

if __name__ == '__main__':
    print("Creando usuarios del sistema LUMA...")
    crear_superuser()
    crear_usuarios_demo()
    print("Proceso completado!")