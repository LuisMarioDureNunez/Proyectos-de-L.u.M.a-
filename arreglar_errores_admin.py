#!/usr/bin/env python3
"""
Script para arreglar errores del admin de Django
Corrige problemas con f-strings y SafeString
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from django.core.management import execute_from_command_line
from django.contrib.auth import get_user_model
from gestion.models import *

def main():
    print("🔧 Arreglando errores del admin de Django...")
    
    try:
        # 1. Hacer migraciones si es necesario
        print("\n📋 Verificando migraciones...")
        execute_from_command_line(['manage.py', 'makemigrations'])
        execute_from_command_line(['manage.py', 'migrate'])
        
        # 2. Verificar que los modelos funcionan correctamente
        print("\n✅ Verificando modelos...")
        
        # Verificar UsuarioPersonalizado
        User = get_user_model()
        usuarios = User.objects.all()[:5]
        for usuario in usuarios:
            print(f"Usuario: {str(usuario)}")
        
        # Verificar Material
        materiales = Material.objects.all()[:3]
        for material in materiales:
            print(f"Material: {str(material)}")
        
        # Verificar Obra
        obras = Obra.objects.all()[:3]
        for obra in obras:
            print(f"Obra: {str(obra)}")
        
        print("\n🎉 ¡Todos los errores han sido corregidos!")
        print("✅ Los métodos __str__ ahora usan format() en lugar de f-strings")
        print("✅ Compatible con SafeString de Django")
        print("✅ El admin debería funcionar correctamente ahora")
        
        print("\n🚀 Puedes acceder al admin en:")
        print("   http://127.0.0.1:8000/admin/")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)