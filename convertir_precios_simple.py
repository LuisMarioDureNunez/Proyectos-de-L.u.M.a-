#!/usr/bin/env python
"""
Script simple para convertir precios de USD a Guaraníes
Ejecutar: python convertir_precios_simple.py
"""

import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import Material, Producto
from decimal import Decimal

# Tasa de cambio USD a PYG
TASA_CAMBIO = Decimal('7300.00')  # 1 USD = 7,300 PYG

def main():
    print("🇵🇾 Convirtiendo precios a Guaraníes...")
    print(f"💱 Tasa de cambio: 1 USD = {TASA_CAMBIO:,.0f} PYG")
    print("-" * 50)
    
    # Convertir materiales
    materiales_convertidos = 0
    for material in Material.objects.all():
        precio_usd = material.precio
        precio_pyg = precio_usd * TASA_CAMBIO
        material.precio = precio_pyg
        material.save()
        print(f"✅ {material.nombre}: ${precio_usd} → {precio_pyg:,.0f} Gs.")
        materiales_convertidos += 1
    
    # Convertir productos
    productos_convertidos = 0
    for producto in Producto.objects.all():
        precio_usd = producto.precio
        precio_pyg = precio_usd * TASA_CAMBIO
        producto.precio = precio_pyg
        producto.save()
        print(f"✅ {producto.nombre}: ${precio_usd} → {precio_pyg:,.0f} Gs.")
        productos_convertidos += 1
    
    print("-" * 50)
    print(f"🎉 Conversión completada!")
    print(f"📦 Materiales convertidos: {materiales_convertidos}")
    print(f"🛍️ Productos convertidos: {productos_convertidos}")
    print("💡 Todos los precios ahora están en Guaraníes (Gs.)")

if __name__ == "__main__":
    main()