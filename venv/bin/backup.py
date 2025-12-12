#!/usr/bin/env python3
"""
Script de backup automático para la base de datos
"""

import os
import shutil
import datetime
from django.conf import settings

def backup_database():
    """Crea una copia de seguridad de la base de datos"""
    
    # Nombre del archivo de backup con fecha
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"backup_db_{timestamp}.sqlite3"
    backup_path = os.path.join('backups', backup_filename)
    
    # Crear directorio de backups si no existe
    os.makedirs('backups', exist_ok=True)
    
    # Ruta de la base de datos actual
    db_path = settings.DATABASES['default']['NAME']
    
    try:
        # Copiar archivo de base de datos
        shutil.copy2(db_path, backup_path)
        print(f"✅ Backup creado exitosamente: {backup_filename}")
        
        # Limitar a 10 backups máximo
        cleanup_old_backups()
        
        return True
    except Exception as e:
        print(f"❌ Error creando backup: {e}")
        return False

def cleanup_old_backups():
    """Elimina backups antiguos, mantiene solo los 10 más recientes"""
    backup_files = []
    
    for filename in os.listdir('backups'):
        if filename.startswith('backup_db_') and filename.endswith('.sqlite3'):
            file_path = os.path.join('backups', filename)
            backup_files.append((file_path, os.path.getctime(file_path)))
    
    # Ordenar por fecha de creación (más antiguos primero)
    backup_files.sort(key=lambda x: x[1])
    
    # Eliminar archivos sobrantes (mantener solo 10)
    while len(backup_files) > 10:
        oldest_file = backup_files.pop(0)
        os.remove(oldest_file[0])
        print(f"🗑️  Backup antiguo eliminado: {os.path.basename(oldest_file[0])}")

if __name__ == "__main__":
    print("💾 INICIANDO BACKUP DE BASE DE DATOS")
    print("=" * 40)
    backup_database()