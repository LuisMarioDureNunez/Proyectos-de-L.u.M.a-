#!/usr/bin/env python
"""
Script para convertir todos los precios de dólares a guaraníes
Ejecutar: python manage.py shell < convertir_precios_guaranies.py
"""

import os
import django
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import Material, Producto, ItemPresupuesto, Presupuesto, Maquinaria, ContratoContratista

# Tasa de cambio USD a PYG (Guaraníes paraguayos)
# Actualizar esta tasa según el tipo de cambio actual
TASA_CAMBIO_USD_PYG = Decimal('7300.00')  # 1 USD = 7,300 PYG aproximadamente

def convertir_precios_materiales():
    """Convierte precios de materiales de USD a PYG"""
    print("🔄 Convirtiendo precios de materiales...")
    materiales = Material.objects.all()
    
    for material in materiales:
        precio_original = material.precio
        precio_guaranies = precio_original * TASA_CAMBIO_USD_PYG
        material.precio = precio_guaranies
        material.save()
        print(f"✅ {material.nombre}: ${precio_original} → {precio_guaranies:,.0f} Gs.")
    
    print(f"📦 Total materiales convertidos: {materiales.count()}")

def convertir_precios_productos():
    """Convierte precios de productos de USD a PYG"""
    print("\n🔄 Convirtiendo precios de productos...")
    productos = Producto.objects.all()
    
    for producto in productos:
        precio_original = producto.precio
        precio_guaranies = precio_original * TASA_CAMBIO_USD_PYG
        producto.precio = precio_guaranies
        producto.save()
        print(f"✅ {producto.nombre}: ${precio_original} → {precio_guaranies:,.0f} Gs.")
    
    print(f"🛍️ Total productos convertidos: {productos.count()}")

def convertir_precios_maquinaria():
    """Convierte precios de alquiler de maquinaria de USD a PYG"""
    print("\n🔄 Convirtiendo precios de maquinaria...")
    maquinarias = Maquinaria.objects.all()
    
    for maquinaria in maquinarias:
        if maquinaria.costo_alquiler_dia > 0:
            costo_original = maquinaria.costo_alquiler_dia
            costo_guaranies = costo_original * TASA_CAMBIO_USD_PYG
            maquinaria.costo_alquiler_dia = costo_guaranies
            maquinaria.save()
            print(f"✅ {maquinaria.nombre}: ${costo_original}/día → {costo_guaranies:,.0f} Gs./día")
    
    print(f"🚜 Total maquinarias convertidas: {maquinarias.count()}")

def convertir_precios_presupuestos():
    """Convierte precios en presupuestos de USD a PYG"""
    print("\n🔄 Convirtiendo precios de presupuestos...")
    
    # Convertir items de presupuesto
    items = ItemPresupuesto.objects.all()
    for item in items:
        precio_original = item.precio_unitario
        precio_guaranies = precio_original * TASA_CAMBIO_USD_PYG
        item.precio_unitario = precio_guaranies
        item.save()  # Esto recalculará automáticamente el total
        print(f"✅ Item: {item.descripcion}: ${precio_original} → {precio_guaranies:,.0f} Gs.")
    
    # Recalcular totales de presupuestos
    presupuestos = Presupuesto.objects.all()
    for presupuesto in presupuestos:
        presupuesto.calcular_totales()
        print(f"📋 Presupuesto {presupuesto.codigo_presupuesto}: Total actualizado a {presupuesto.total:,.0f} Gs.")
    
    print(f"📋 Total items convertidos: {items.count()}")
    print(f"📋 Total presupuestos recalculados: {presupuestos.count()}")

def convertir_precios_contratos():
    """Convierte montos de contratos de USD a PYG"""
    print("\n🔄 Convirtiendo montos de contratos...")
    contratos = ContratoContratista.objects.all()
    
    for contrato in contratos:
        monto_original = contrato.monto_total
        monto_guaranies = monto_original * TASA_CAMBIO_USD_PYG
        contrato.monto_total = monto_guaranies
        
        # Convertir anticipo si existe
        if contrato.anticipo_monto > 0:
            anticipo_original = contrato.anticipo_monto
            anticipo_guaranies = anticipo_original * TASA_CAMBIO_USD_PYG
            contrato.anticipo_monto = anticipo_guaranies
        
        contrato.save()
        print(f"✅ Contrato {contrato.numero_contrato}: ${monto_original} → {monto_guaranies:,.0f} Gs.")
    
    print(f"📄 Total contratos convertidos: {contratos.count()}")

def mostrar_resumen():
    """Muestra un resumen de la conversión"""
    print("\n" + "="*60)
    print("🎉 CONVERSIÓN COMPLETADA - RESUMEN")
    print("="*60)
    print(f"💱 Tasa de cambio utilizada: 1 USD = {TASA_CAMBIO_USD_PYG:,.0f} PYG")
    print(f"📦 Materiales: {Material.objects.count()}")
    print(f"🛍️ Productos: {Producto.objects.count()}")
    print(f"🚜 Maquinarias: {Maquinaria.objects.count()}")
    print(f"📋 Items de presupuesto: {ItemPresupuesto.objects.count()}")
    print(f"📋 Presupuestos: {Presupuesto.objects.count()}")
    print(f"📄 Contratos: {ContratoContratista.objects.count()}")
    print("="*60)
    print("✅ Todos los precios han sido convertidos a Guaraníes (PYG)")
    print("💡 Tip: Actualiza tus templates para mostrar 'Gs.' en lugar de '$'")

if __name__ == "__main__":
    print("🇵🇾 CONVERSIÓN DE PRECIOS A GUARANÍES PARAGUAYOS")
    print("="*60)
    print(f"💱 Tasa de cambio: 1 USD = {TASA_CAMBIO_USD_PYG:,.0f} PYG")
    print("⚠️  IMPORTANTE: Este proceso modificará TODOS los precios en la base de datos")
    
    respuesta = input("\n¿Deseas continuar? (s/n): ").lower().strip()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        print("\n🚀 Iniciando conversión...")
        
        try:
            convertir_precios_materiales()
            convertir_precios_productos()
            convertir_precios_maquinaria()
            convertir_precios_presupuestos()
            convertir_precios_contratos()
            mostrar_resumen()
            
        except Exception as e:
            print(f"\n❌ Error durante la conversión: {e}")
            print("💡 Revisa la base de datos y ejecuta nuevamente si es necesario")
    else:
        print("\n❌ Conversión cancelada por el usuario")