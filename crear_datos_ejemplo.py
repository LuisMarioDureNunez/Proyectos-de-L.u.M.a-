#!/usr/bin/env python
"""
Crear datos de ejemplo para el dashboard
"""
import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import *

def crear_datos_ejemplo():
    """Crear datos de ejemplo para mostrar en el dashboard"""
    print("Creando datos de ejemplo...")
    
    try:
        # 1. Crear materiales adicionales
        materiales_ejemplo = [
            {'nombre': 'Cemento Portland', 'precio': 45000, 'stock': 50, 'unidad_medida': 'bolsa'},
            {'nombre': 'Arena Fina', 'precio': 25000, 'stock': 100, 'unidad_medida': 'm³'},
            {'nombre': 'Grava', 'precio': 30000, 'stock': 80, 'unidad_medida': 'm³'},
            {'nombre': 'Ladrillos Comunes', 'precio': 800, 'stock': 5000, 'unidad_medida': 'unidad'},
            {'nombre': 'Hierro 12mm', 'precio': 8500, 'stock': 200, 'unidad_medida': 'barra'},
        ]
        
        admin_user = UsuarioPersonalizado.objects.filter(username='admin').first()
        if not admin_user:
            print("Usuario admin no encontrado")
            return
        
        for mat_data in materiales_ejemplo:
            material, created = Material.objects.get_or_create(
                nombre=mat_data['nombre'],
                defaults={
                    'descripcion': f'Material de construcción: {mat_data["nombre"]}',
                    'precio': Decimal(str(mat_data['precio'])),
                    'stock': mat_data['stock'],
                    'unidad_medida': mat_data['unidad_medida'],
                    'creado_por': admin_user
                }
            )
            if created:
                print(f"Material creado: {material.nombre}")
        
        # 2. Crear obras adicionales
        cliente = UsuarioPersonalizado.objects.filter(rol='cliente').first()
        constructor = UsuarioPersonalizado.objects.filter(rol='constructor').first()
        
        if cliente and constructor:
            obras_ejemplo = [
                {
                    'nombre': 'Edificio Comercial Centro',
                    'descripcion': 'Construcción de edificio comercial de 3 plantas',
                    'ubicacion': 'Asunción, Central, Paraguay',
                    'estado': 'en_proceso',
                    'presupuesto_asignado': 850000000,
                    'costo_real': 650000000
                },
                {
                    'nombre': 'Casa Familiar San Lorenzo',
                    'descripcion': 'Casa unifamiliar de 120m²',
                    'ubicacion': 'San Lorenzo, Central, Paraguay',
                    'estado': 'finalizada',
                    'presupuesto_asignado': 280000000,
                    'costo_real': 275000000
                },
                {
                    'nombre': 'Complejo Residencial Luque',
                    'descripcion': 'Complejo de 5 casas residenciales',
                    'ubicacion': 'Luque, Central, Paraguay',
                    'estado': 'planificada',
                    'presupuesto_asignado': 1200000000,
                    'costo_real': 0
                }
            ]
            
            for obra_data in obras_ejemplo:
                obra, created = Obra.objects.get_or_create(
                    nombre=obra_data['nombre'],
                    defaults={
                        'descripcion': obra_data['descripcion'],
                        'ubicacion': obra_data['ubicacion'],
                        'cliente': cliente,
                        'constructor': constructor,
                        'fecha_inicio': date.today() - timedelta(days=30),
                        'fecha_fin_estimada': date.today() + timedelta(days=90),
                        'estado': obra_data['estado'],
                        'presupuesto_asignado': Decimal(str(obra_data['presupuesto_asignado'])),
                        'costo_real': Decimal(str(obra_data['costo_real'])),
                        'creado_por': admin_user
                    }
                )
                if created:
                    print(f"Obra creada: {obra.nombre}")
        
        # 3. Crear presupuestos de ejemplo
        obras = Obra.objects.all()[:3]
        for i, obra in enumerate(obras):
            presupuesto, created = Presupuesto.objects.get_or_create(
                obra=obra,
                cliente=obra.cliente,
                defaults={
                    'constructor': constructor,
                    'descripcion_servicios': f'Presupuesto completo para {obra.nombre}',
                    'subtotal': obra.presupuesto_asignado * Decimal('0.9'),
                    'iva_porcentaje': Decimal('10'),
                    'iva_monto': obra.presupuesto_asignado * Decimal('0.1'),
                    'total': obra.presupuesto_asignado,
                    'estado': ['aceptado', 'en_revision', 'solicitado'][i % 3],
                    'dias_validez': 30
                }
            )
            if created:
                print(f"Presupuesto creado para: {obra.nombre}")
        
        # 4. Crear maquinarias
        maquinarias_ejemplo = [
            {'nombre': 'Excavadora CAT 320', 'estado': 'disponible', 'costo_alquiler_dia': 450000},
            {'nombre': 'Mixer de Concreto', 'estado': 'en_uso', 'costo_alquiler_dia': 280000},
            {'nombre': 'Grúa Torre', 'estado': 'mantenimiento', 'costo_alquiler_dia': 650000},
        ]
        
        for maq_data in maquinarias_ejemplo:
            maquinaria, created = Maquinaria.objects.get_or_create(
                nombre=maq_data['nombre'],
                defaults={
                    'descripcion': f'Maquinaria para construcción: {maq_data["nombre"]}',
                    'modelo': 'Modelo 2023',
                    'marca': 'Industrial',
                    'estado': maq_data['estado'],
                    'costo_alquiler_dia': Decimal(str(maq_data['costo_alquiler_dia'])),
                    'creado_por': admin_user
                }
            )
            if created:
                print(f"Maquinaria creada: {maquinaria.nombre}")
        
        # 5. Crear herramientas
        herramientas_ejemplo = [
            {'nombre': 'Taladro Industrial', 'cantidad_total': 15, 'estado': 'disponible'},
            {'nombre': 'Sierra Circular', 'cantidad_total': 8, 'estado': 'disponible'},
            {'nombre': 'Nivel Láser', 'cantidad_total': 5, 'estado': 'en_uso'},
        ]
        
        for herr_data in herramientas_ejemplo:
            herramienta, created = Herramienta.objects.get_or_create(
                nombre=herr_data['nombre'],
                defaults={
                    'descripcion': f'Herramienta: {herr_data["nombre"]}',
                    'estado': herr_data['estado'],
                    'cantidad_total': herr_data['cantidad_total'],
                    'cantidad_disponible': herr_data['cantidad_total'] - 2,
                    'creado_por': admin_user
                }
            )
            if created:
                print(f"Herramienta creada: {herramienta.nombre}")
        
        print("\n¡Datos de ejemplo creados exitosamente!")
        print("Ahora el dashboard se verá mucho más completo.")
        
    except Exception as e:
        print(f"Error creando datos: {e}")

if __name__ == '__main__':
    crear_datos_ejemplo()