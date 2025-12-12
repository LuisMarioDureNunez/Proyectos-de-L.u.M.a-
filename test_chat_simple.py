#!/usr/bin/env python3
"""
Test simple para el chat L.u.N.a AI
"""

import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
import json

def test_luna_chat():
    """Probar el chat L.u.N.a AI"""
    
    client = Client()
    User = get_user_model()
    
    # Crear usuario de prueba si no existe
    try:
        user = User.objects.get(username='admin')
        print(f"Usuario admin encontrado: {user.username}")
    except User.DoesNotExist:
        print("Usuario admin no encontrado")
        return
    
    # Login
    client.force_login(user)
    print("Login exitoso")
    
    # Probar endpoint de chat
    response = client.post('/luna-ai/chat/', 
        data=json.dumps({
            'question': 'hola',
            'user_id': 'admin'
        }),
        content_type='application/json'
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Respuesta exitosa: {data.get('success', False)}")
        if data.get('response'):
            print(f"Respuesta: {data['response'][:100]}...")
        else:
            print("No hay respuesta en los datos")
            print(f"Datos completos: {data}")
    else:
        print(f"Error en la respuesta: {response.content}")
    
    print("Test completado!")

if __name__ == "__main__":
    test_luna_chat()