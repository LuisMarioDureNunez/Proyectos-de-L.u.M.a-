#!/usr/bin/env python3
# test_panels.py - Script para verificar que los paneles funcionan

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

def test_urls():
    """Prueba las URLs principales"""
    base_url = "http://127.0.0.1:8000"
    
    urls_to_test = [
        "/dashboard/",
        "/presupuestos/",
        "/obras/",
        "/materiales/",
        "/reportes/estadisticas/",
        "/produccion/panel-obras/",
        "/produccion/panel-empleados/",
        "/proveedores/",
    ]
    
    print("Probando URLs principales...")
    
    for url in urls_to_test:
        try:
            print(f"Probando: {url}")
            # Solo verificamos que Django puede resolver la URL
            from django.urls import reverse, resolve
            from django.test import RequestFactory
            
            # Crear request de prueba
            factory = RequestFactory()
            request = factory.get(url)
            
            # Intentar resolver la URL
            try:
                resolved = resolve(url)
                print(f"  ✓ URL resuelta correctamente: {resolved.view_name}")
            except Exception as e:
                print(f"  ✗ Error resolviendo URL: {e}")
                
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print("\nPrueba completada. Ahora ejecuta: python manage.py runserver")

if __name__ == '__main__':
    test_urls()