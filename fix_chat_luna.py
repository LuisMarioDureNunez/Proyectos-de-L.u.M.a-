#!/usr/bin/env python3
"""
Fix rápido para el chat L.u.N.a AI
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
        print(f"✅ Usuario admin encontrado: {user.username}")
    except User.DoesNotExist:
        print("❌ Usuario admin no encontrado")
        return
    
    # Login
    client.force_login(user)
    print("✅ Login exitoso")
    
    # Probar endpoint de chat
    response = client.post('/luna-ai/chat/', 
        data=json.dumps({
            'question': 'hola',
            'user_id': 'admin'
        }),
        content_type='application/json'
    )
    
    print(f"📡 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Respuesta exitosa: {data.get('success', False)}")
        if data.get('response'):
            print(f"💬 Respuesta: {data['response'][:100]}...")
        else:
            print("❌ No hay respuesta en los datos")
    else:
        print(f"❌ Error en la respuesta: {response.content}")
    
    # Probar endpoint de conocimiento
    response = client.get('/luna-ai/knowledge/')
    print(f"🧠 Knowledge API Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"📊 Stats: {data.get('stats', {})}")
        print(f"📦 Materiales: {len(data.get('materiales', {}))}")
    
    print("\n🎉 Test completado!")

if __name__ == "__main__":
    test_luna_chat()