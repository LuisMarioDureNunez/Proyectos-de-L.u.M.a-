#!/usr/bin/env python
"""Script para dar permisos de superusuario"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import UsuarioPersonalizado

try:
    user = UsuarioPersonalizado.objects.get(username='LUMApy')
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f'✅ Usuario {user.username} ahora es SUPERUSUARIO')
    print(f'   - is_superuser: {user.is_superuser}')
    print(f'   - is_staff: {user.is_staff}')
    print(f'   - Rol: {user.get_rol_display()}')
except UsuarioPersonalizado.DoesNotExist:
    print('❌ Usuario LUMApy no existe')
except Exception as e:
    print(f'❌ Error: {e}')
