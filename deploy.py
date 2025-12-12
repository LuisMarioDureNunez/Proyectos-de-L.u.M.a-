#!/usr/bin/env python3
"""
Script de despliegue automático para Mi Tienda Django
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Ejecuta un comando y muestra el resultado"""
    print(f"\n🎯 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"Salida: {e.stderr}")
        return False

def deploy():
    """Función principal de despliegue"""
    print("🚀 INICIANDO DESPLIEGUE DE MI TIENDA DJANGO")
    print("=" * 50)
    
    # 1. Verificar que estamos en el directorio correcto
    if not os.path.exists('manage.py'):
        print("❌ Error: No se encuentra manage.py. Ejecuta desde la raíz del proyecto.")
        return False
    
    # 2. Instalar dependencias
    if not run_command("pip install -r requirements.txt", "Instalando dependencias"):
        return False
    
    # 3. Ejecutar migraciones
    if not run_command("python manage.py migrate", "Ejecutando migraciones"):
        return False
    
    # 4. Colectar archivos estáticos
    if not run_command("python manage.py collectstatic --noinput", "Recolectando archivos estáticos"):
        return False
    
    # 5. Crear superusuario si no existe
    create_superuser = input("¿Crear superusuario? (s/n): ").lower().strip()
    if create_superuser in ['s', 'si', 'sí', 'y', 'yes']:
        run_command("python manage.py createsuperuser", "Creando superusuario")
    
    # 6. Verificar que todo funciona
    if not run_command("python manage.py check --deploy", "Verificando configuración de producción"):
        return False
    
    print("\n🎉 ¡DESPLIEGUE COMPLETADO EXITOSAMENTE!")
    print("\n📋 Próximos pasos:")
    print("1. Ejecuta: python manage.py runserver")
    print("2. Abre: http://127.0.0.1:8000")
    print("3. Para producción usa: gunicorn mi_tienda.wsgi:application")
    
    return True

if __name__ == "__main__":
    deploy()