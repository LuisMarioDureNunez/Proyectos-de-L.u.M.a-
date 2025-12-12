#!/usr/bin/env python3
# manage_production.py - Script de gestión para producción

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description=""):
    """Ejecutar comando y mostrar resultado"""
    print(f"🔄 {description}")
    print(f"Ejecutando: {command}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Completado")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}")
        print(f"Error: {e.stderr}")
        return False

def setup_production():
    """Configurar entorno de producción"""
    print("🚀 Configurando entorno de producción...")
    
    commands = [
        ("pip install -r requirements.txt", "Instalando dependencias"),
        ("python manage.py collectstatic --noinput", "Recolectando archivos estáticos"),
        ("python manage.py migrate", "Aplicando migraciones"),
        ("python manage.py check --deploy", "Verificando configuración de despliegue"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            print("❌ Error en la configuración. Deteniendo proceso.")
            return False
    
    print("✅ Configuración de producción completada")
    return True

def create_superuser():
    """Crear superusuario si no existe"""
    print("👤 Creando superusuario...")
    
    # Verificar si ya existe un superusuario
    check_command = "python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); print('exists' if User.objects.filter(is_superuser=True).exists() else 'none')\""
    
    try:
        result = subprocess.run(check_command, shell=True, capture_output=True, text=True)
        if 'exists' in result.stdout:
            print("✅ Ya existe un superusuario")
            return True
    except:
        pass
    
    # Crear superusuario automáticamente
    create_command = """
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@mitienda.com', 'admin123')
    print('Superusuario creado: admin/admin123')
else:
    print('Usuario admin ya existe')
"
"""
    
    return run_command(create_command, "Creando superusuario automático")

def backup_database():
    """Crear backup de la base de datos"""
    print("💾 Creando backup de la base de datos...")
    
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.json"
    
    command = f"python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission > {backup_file}"
    
    if run_command(command, f"Creando backup en {backup_file}"):
        print(f"✅ Backup creado: {backup_file}")
        return backup_file
    return None

def restore_database(backup_file):
    """Restaurar base de datos desde backup"""
    if not os.path.exists(backup_file):
        print(f"❌ Archivo de backup no encontrado: {backup_file}")
        return False
    
    print(f"🔄 Restaurando base de datos desde {backup_file}...")
    
    commands = [
        ("python manage.py flush --noinput", "Limpiando base de datos"),
        (f"python manage.py loaddata {backup_file}", f"Cargando datos desde {backup_file}"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    print("✅ Base de datos restaurada correctamente")
    return True

def check_system():
    """Verificar estado del sistema"""
    print("🔍 Verificando estado del sistema...")
    
    checks = [
        ("python manage.py check", "Verificando configuración Django"),
        ("python manage.py showmigrations", "Verificando migraciones"),
        ("python manage.py collectstatic --dry-run --noinput", "Verificando archivos estáticos"),
    ]
    
    all_good = True
    for command, description in checks:
        if not run_command(command, description):
            all_good = False
    
    if all_good:
        print("✅ Sistema verificado correctamente")
    else:
        print("⚠️ Se encontraron algunos problemas")
    
    return all_good

def show_help():
    """Mostrar ayuda"""
    print("""
🛠️  Script de Gestión de Producción - Mi Tienda Premium

Comandos disponibles:
    setup       - Configurar entorno de producción completo
    superuser   - Crear superusuario automáticamente
    backup      - Crear backup de la base de datos
    restore     - Restaurar base de datos (requiere archivo)
    check       - Verificar estado del sistema
    help        - Mostrar esta ayuda

Ejemplos:
    python manage_production.py setup
    python manage_production.py backup
    python manage_production.py restore backup_20241201_120000.json
    python manage_production.py check

Variables de entorno requeridas para producción:
    - SECRET_KEY
    - DB_PASSWORD
    - EMAIL_HOST_USER
    - EMAIL_HOST_PASSWORD
    """)

def main():
    """Función principal"""
    if len(sys.argv) < 2:
        show_help()
        return
    
    command = sys.argv[1].lower()
    
    # Configurar Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
    
    try:
        import django
        django.setup()
    except Exception as e:
        print(f"❌ Error configurando Django: {e}")
        return
    
    if command == 'setup':
        setup_production()
        create_superuser()
        
    elif command == 'superuser':
        create_superuser()
        
    elif command == 'backup':
        backup_database()
        
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("❌ Especifica el archivo de backup: python manage_production.py restore backup_file.json")
            return
        restore_database(sys.argv[2])
        
    elif command == 'check':
        check_system()
        
    elif command == 'help':
        show_help()
        
    else:
        print(f"❌ Comando desconocido: {command}")
        show_help()

if __name__ == '__main__':
    main()