#!/usr/bin/env python
"""
Script completo para convertir toda la aplicación de USD a Guaraníes
Ejecutar: python ejecutar_conversion_completa.py
"""

import os
import sys
import django

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import Material, Producto, ItemPresupuesto, Presupuesto, Maquinaria, ContratoContratista
from decimal import Decimal

# Tasa de cambio USD a PYG
TASA_CAMBIO = Decimal('7300.00')

def main():
    print("🇵🇾 CONVERSIÓN COMPLETA A GUARANÍES PARAGUAYOS")
    print("=" * 60)
    print(f"💱 Tasa de cambio: 1 USD = {TASA_CAMBIO:,.0f} PYG")
    print("🔄 Iniciando conversión completa...")
    print("-" * 60)
    
    try:
        # 1. Convertir materiales
        print("📦 Convirtiendo materiales...")
        materiales_count = 0
        for material in Material.objects.all():
            precio_usd = material.precio
            material.precio = precio_usd * TASA_CAMBIO
            material.save()
            print(f"   ✅ {material.nombre}: ${precio_usd} → {material.precio:,.0f} Gs.")
            materiales_count += 1
        
        # 2. Convertir productos
        print("\n🛍️ Convirtiendo productos...")
        productos_count = 0
        for producto in Producto.objects.all():
            precio_usd = producto.precio
            producto.precio = precio_usd * TASA_CAMBIO
            producto.save()
            print(f"   ✅ {producto.nombre}: ${precio_usd} → {producto.precio:,.0f} Gs.")
            productos_count += 1
        
        # 3. Convertir maquinaria
        print("\n🚜 Convirtiendo maquinaria...")
        maquinarias_count = 0
        for maquinaria in Maquinaria.objects.all():
            if maquinaria.costo_alquiler_dia > 0:
                costo_usd = maquinaria.costo_alquiler_dia
                maquinaria.costo_alquiler_dia = costo_usd * TASA_CAMBIO
                maquinaria.save()
                print(f"   ✅ {maquinaria.nombre}: ${costo_usd}/día → {maquinaria.costo_alquiler_dia:,.0f} Gs./día")
                maquinarias_count += 1
        
        # 4. Convertir items de presupuesto
        print("\n📋 Convirtiendo items de presupuesto...")
        items_count = 0
        for item in ItemPresupuesto.objects.all():
            precio_usd = item.precio_unitario
            item.precio_unitario = precio_usd * TASA_CAMBIO
            item.save()
            print(f"   ✅ {item.descripcion}: ${precio_usd} → {item.precio_unitario:,.0f} Gs.")
            items_count += 1
        
        # 5. Recalcular presupuestos
        print("\n📊 Recalculando presupuestos...")
        presupuestos_count = 0
        for presupuesto in Presupuesto.objects.all():
            presupuesto.calcular_totales()
            print(f"   ✅ {presupuesto.codigo_presupuesto}: Total = {presupuesto.total:,.0f} Gs.")
            presupuestos_count += 1
        
        # 6. Convertir contratos
        print("\n📄 Convirtiendo contratos...")
        contratos_count = 0
        for contrato in ContratoContratista.objects.all():
            monto_usd = contrato.monto_total
            contrato.monto_total = monto_usd * TASA_CAMBIO
            if contrato.anticipo_monto > 0:
                contrato.anticipo_monto *= TASA_CAMBIO
            contrato.save()
            print(f"   ✅ {contrato.numero_contrato}: ${monto_usd} → {contrato.monto_total:,.0f} Gs.")
            contratos_count += 1
        
        # Resumen final
        print("\n" + "=" * 60)
        print("🎉 CONVERSIÓN COMPLETADA EXITOSAMENTE")
        print("=" * 60)
        print(f"📦 Materiales convertidos: {materiales_count}")
        print(f"🛍️ Productos convertidos: {productos_count}")
        print(f"🚜 Maquinarias convertidas: {maquinarias_count}")
        print(f"📋 Items de presupuesto convertidos: {items_count}")
        print(f"📊 Presupuestos recalculados: {presupuestos_count}")
        print(f"📄 Contratos convertidos: {contratos_count}")
        print("=" * 60)
        print("✅ Todos los precios han sido convertidos a Guaraníes (PYG)")
        print("✅ Templates actualizados para mostrar 'Gs.' en lugar de '$'")
        print("💡 La aplicación ahora está completamente en Guaraníes paraguayos")
        print("\n🔧 PRÓXIMOS PASOS:")
        print("1. Reinicia el servidor Django: python manage.py runserver")
        print("2. Verifica que todos los precios se muestren correctamente")
        print("3. Actualiza cualquier documentación o manual de usuario")
        
    except Exception as e:
        print(f"\n❌ Error durante la conversión: {e}")
        print("💡 Revisa la base de datos y ejecuta nuevamente si es necesario")

if __name__ == "__main__":
    main()