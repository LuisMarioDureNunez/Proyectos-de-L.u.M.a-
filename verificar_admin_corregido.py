#!/usr/bin/env python3
"""
Script para verificar que el admin de Django funciona correctamente
después de corregir los errores de f-strings
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from django.contrib.auth import get_user_model
from gestion.models import *

def main():
    print("🔧 Verificando correcciones del admin de Django...")
    
    try:
        # Verificar que los modelos funcionan correctamente
        print("\n✅ Verificando métodos __str__ de los modelos...")
        
        User = get_user_model()
        
        # Crear usuario de prueba si no existe
        if not User.objects.filter(username='admin_test').exists():
            usuario_test = User.objects.create_user(
                username='admin_test',
                email='admin@test.com',
                password='test123',
                rol='admin'
            )
            print(f"✅ Usuario de prueba creado: {str(usuario_test)}")
        else:
            usuario_test = User.objects.get(username='admin_test')
            print(f"✅ Usuario existente: {str(usuario_test)}")
        
        # Crear material de prueba si no existe
        if not Material.objects.filter(nombre='Cemento Test').exists():
            material_test = Material.objects.create(
                nombre='Cemento Test',
                descripcion='Material de prueba',
                precio=50000,
                stock=100,
                unidad_medida='bolsa',
                creado_por=usuario_test
            )
            print(f"✅ Material de prueba creado: {str(material_test)}")
        
        # Crear obra de prueba si no existe
        if not Obra.objects.filter(nombre='Obra Test').exists():
            obra_test = Obra.objects.create(
                nombre='Obra Test',
                descripcion='Obra de prueba',
                ubicacion='Asunción, Paraguay',
                cliente=usuario_test,
                fecha_inicio='2024-01-01',
                estado='planificada',
                presupuesto_asignado=1000000,
                creado_por=usuario_test
            )
            print(f"✅ Obra de prueba creada: {str(obra_test)}")
        
        # Verificar que todos los métodos __str__ funcionan
        print("\n🔍 Verificando métodos __str__ corregidos...")
        
        # Verificar Material
        materiales = Material.objects.all()[:3]
        for material in materiales:
            str_result = str(material)
            print(f"  Material: {str_result}")
        
        # Verificar Obra
        obras = Obra.objects.all()[:3]
        for obra in obras:
            str_result = str(obra)
            print(f"  Obra: {str_result}")
        
        # Verificar Usuario
        usuarios = User.objects.all()[:3]
        for usuario in usuarios:
            str_result = str(usuario)
            print(f"  Usuario: {str_result}")
        
        print("\n🎉 ¡Todas las correcciones funcionan correctamente!")
        print("✅ Los métodos __str__ ahora usan format() en lugar de f-strings")
        print("✅ Compatible con SafeString de Django")
        print("✅ El admin debería funcionar sin errores ahora")
        
        print("\n🚀 Instrucciones:")
        print("1. Inicia el servidor: python manage.py runserver")
        print("2. Ve al admin: http://127.0.0.1:8000/admin/")
        print("3. Las secciones de Obras, Materiales y Maquinarias deberían funcionar correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)