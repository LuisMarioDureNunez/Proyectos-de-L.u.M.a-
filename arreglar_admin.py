#!/usr/bin/env python
"""
Arreglar contraseña del usuario admin
"""
import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import UsuarioPersonalizado

def arreglar_admin():
    """Arreglar contraseña del admin"""
    try:
        admin = UsuarioPersonalizado.objects.get(username='admin')
        admin.set_password('123')
        admin.save()
        print("OK: Contraseña del admin actualizada a '123'")
        
        # Verificar
        admin.refresh_from_db()
        if admin.check_password('123'):
            print("OK: Contraseña verificada correctamente")
        else:
            print("ERROR: La contraseña sigue siendo incorrecta")
            
    except UsuarioPersonalizado.DoesNotExist:
        print("ERROR: Usuario admin no encontrado")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == '__main__':
    arreglar_admin()