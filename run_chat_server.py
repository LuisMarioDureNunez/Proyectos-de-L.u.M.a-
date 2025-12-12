#!/usr/bin/env python
"""
Script para ejecutar el servidor ASGI con soporte para WebSockets
Ejecutar: python run_chat_server.py
"""
import os
import sys
import django
from django.core.management import execute_from_command_line

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
    
    print("Iniciando servidor LUMA con soporte para Chat WebSockets...")
    print("WebSockets habilitados en: ws://127.0.0.1:8000/ws/chat/")
    print("Servidor HTTP en: http://127.0.0.1:8000/")
    print("Chat LUMA funcionando correctamente")
    print("-" * 60)
    
    # Ejecutar con daphne (servidor ASGI)
    execute_from_command_line(['manage.py', 'runserver'])