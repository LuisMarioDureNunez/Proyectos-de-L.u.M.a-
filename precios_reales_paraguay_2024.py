#!/usr/bin/env python
"""
Precios reales de materiales de construcción en Paraguay 2024
Fuente: Mercado paraguayo actualizado
"""

import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

from gestion.models import Material, Maquinaria, Empleado, Contratista

# PRECIOS REALES PARAGUAY 2024 (en Guaraníes)
MATERIALES_PRECIOS_PY = {
    # CEMENTO Y AGLOMERANTES
    'Cemento Portland': {'precio': 45000, 'unidad': 'bolsa', 'descripcion': 'Cemento Portland tipo I - 50kg'},
    'Cal Hidratada': {'precio': 28000, 'unidad': 'bolsa', 'descripcion': 'Cal hidratada para construcción - 25kg'},
    'Yeso': {'precio': 35000, 'unidad': 'bolsa', 'descripcion': 'Yeso para construcción - 40kg'},
    
    # AGREGADOS
    'Arena Fina': {'precio': 180000, 'unidad': 'm³', 'descripcion': 'Arena fina lavada para construcción'},
    'Arena Gruesa': {'precio': 170000, 'unidad': 'm³', 'descripcion': 'Arena gruesa para hormigón'},
    'Grava': {'precio': 220000, 'unidad': 'm³', 'descripcion': 'Grava triturada 12-25mm'},
    'Piedra Bruta': {'precio': 150000, 'unidad': 'm³', 'descripcion': 'Piedra bruta para cimientos'},
    'Ripio': {'precio': 190000, 'unidad': 'm³', 'descripcion': 'Ripio para hormigón'},
    
    # LADRILLOS Y BLOQUES
    'Ladrillos Comunes': {'precio': 1200, 'unidad': 'unidad', 'descripcion': 'Ladrillo común 6 huecos'},
    'Ladrillos Huecos': {'precio': 1800, 'unidad': 'unidad', 'descripcion': 'Ladrillo hueco 12cm'},
    'Bloques de Hormigón': {'precio': 8500, 'unidad': 'unidad', 'descripcion': 'Bloque de hormigón 20x20x40cm'},
    'Ladrillos Refractarios': {'precio': 4500, 'unidad': 'unidad', 'descripcion': 'Ladrillo refractario para hornos'},
    
    # HIERROS Y ACEROS
    'Hierro 6mm': {'precio': 18000, 'unidad': 'barra', 'descripcion': 'Hierro corrugado 6mm x 12m'},
    'Hierro 8mm': {'precio': 28000, 'unidad': 'barra', 'descripcion': 'Hierro corrugado 8mm x 12m'},
    'Hierro 10mm': {'precio': 42000, 'unidad': 'barra', 'descripcion': 'Hierro corrugado 10mm x 12m'},
    'Hierro 12mm': {'precio': 58000, 'unidad': 'barra', 'descripcion': 'Hierro corrugado 12mm x 12m'},
    'Hierro 16mm': {'precio': 95000, 'unidad': 'barra', 'descripcion': 'Hierro corrugado 16mm x 12m'},
    'Alambre Negro': {'precio': 12000, 'unidad': 'kg', 'descripcion': 'Alambre negro para atar hierros'},
    
    # MADERAS
    'Tabla Pino': {'precio': 25000, 'unidad': 'm²', 'descripcion': 'Tabla de pino 1" x 12"'},
    'Tirante Eucalipto': {'precio': 35000, 'unidad': 'unidad', 'descripcion': 'Tirante eucalipto 2" x 4" x 3m'},
    'Machimbre': {'precio': 45000, 'unidad': 'm²', 'descripcion': 'Machimbre de pino 1/2"'},
    'Contrachapado': {'precio': 85000, 'unidad': 'plancha', 'descripcion': 'Contrachapado 15mm 1.22x2.44m'},
    
    # REVESTIMIENTOS
    'Cerámica 30x30': {'precio': 35000, 'unidad': 'm²', 'descripcion': 'Cerámica esmaltada 30x30cm'},
    'Cerámica 45x45': {'precio': 55000, 'unidad': 'm²', 'descripcion': 'Cerámica esmaltada 45x45cm'},
    'Porcelanato 60x60': {'precio': 120000, 'unidad': 'm²', 'descripcion': 'Porcelanato pulido 60x60cm'},
    'Azulejos': {'precio': 28000, 'unidad': 'm²', 'descripcion': 'Azulejos blancos 20x30cm'},
    
    # PINTURAS
    'Pintura Látex': {'precio': 85000, 'unidad': 'lata', 'descripcion': 'Pintura látex interior 20L'},
    'Pintura Esmalte': {'precio': 95000, 'unidad': 'lata', 'descripcion': 'Pintura esmalte sintético 4L'},
    'Pintura Antióxido': {'precio': 75000, 'unidad': 'lata', 'descripcion': 'Pintura antióxido 4L'},
    'Sellador': {'precio': 65000, 'unidad': 'lata', 'descripcion': 'Sellador para paredes 20L'},
    
    # INSTALACIONES ELÉCTRICAS
    'Cable 2.5mm': {'precio': 8500, 'unidad': 'metro', 'descripcion': 'Cable unipolar 2.5mm²'},
    'Cable 4mm': {'precio': 12000, 'unidad': 'metro', 'descripcion': 'Cable unipolar 4mm²'},
    'Caño PVC 20mm': {'precio': 15000, 'unidad': 'barra', 'descripcion': 'Caño PVC eléctrico 20mm x 3m'},
    'Toma Corriente': {'precio': 25000, 'unidad': 'unidad', 'descripcion': 'Toma corriente con tierra'},
    
    # INSTALACIONES SANITARIAS
    'Caño PVC 110mm': {'precio': 45000, 'unidad': 'barra', 'descripcion': 'Caño PVC desagüe 110mm x 3m'},
    'Caño PVC 75mm': {'precio': 32000, 'unidad': 'barra', 'descripcion': 'Caño PVC desagüe 75mm x 3m'},
    'Inodoro': {'precio': 450000, 'unidad': 'unidad', 'descripcion': 'Inodoro completo con depósito'},
    'Lavatorio': {'precio': 280000, 'unidad': 'unidad', 'descripcion': 'Lavatorio con pedestal'},
    
    # TECHOS
    'Chapa Galvanizada': {'precio': 85000, 'unidad': 'm²', 'descripcion': 'Chapa galvanizada ondulada'},
    'Teja Francesa': {'precio': 2800, 'unidad': 'unidad', 'descripcion': 'Teja francesa de cerámica'},
    'Membrana Asfáltica': {'precio': 45000, 'unidad': 'm²', 'descripcion': 'Membrana asfáltica 4mm'},
}

# MAQUINARIAS - COSTOS DE ALQUILER POR DÍA
MAQUINARIAS_ALQUILER_PY = {
    'Retroexcavadora': {'costo_dia': 850000, 'descripcion': 'Retroexcavadora CAT 320D'},
    'Motoniveladora': {'costo_dia': 1200000, 'descripcion': 'Motoniveladora CAT 140M'},
    'Compactadora': {'costo_dia': 450000, 'descripcion': 'Compactadora vibradora 10 ton'},
    'Mixer Hormigón': {'costo_dia': 380000, 'descripcion': 'Mixer para hormigón 8m³'},
    'Grúa Torre': {'costo_dia': 1800000, 'descripcion': 'Grúa torre 50m alcance'},
    'Bulldozer': {'costo_dia': 950000, 'descripcion': 'Bulldozer CAT D6T'},
    'Excavadora': {'costo_dia': 750000, 'descripcion': 'Excavadora hidráulica 20 ton'},
    'Cargadora Frontal': {'costo_dia': 680000, 'descripcion': 'Cargadora frontal 3m³'},
    'Vibrador Hormigón': {'costo_dia': 85000, 'descripcion': 'Vibrador para hormigón'},
    'Soldadora': {'costo_dia': 120000, 'descripcion': 'Soldadora eléctrica 300A'},
}

# SALARIOS EMPLEADOS CONSTRUCCIÓN PARAGUAY 2024
SALARIOS_EMPLEADOS_PY = {
    'Peón': {'hora': 12000, 'dia': 96000, 'mes': 2500000},
    'Oficial Albañil': {'hora': 18000, 'dia': 144000, 'mes': 3800000},
    'Maestro Obras': {'hora': 25000, 'dia': 200000, 'mes': 5200000},
    'Electricista': {'hora': 22000, 'dia': 176000, 'mes': 4600000},
    'Plomero': {'hora': 20000, 'dia': 160000, 'mes': 4200000},
    'Carpintero': {'hora': 19000, 'dia': 152000, 'mes': 4000000},
    'Pintor': {'hora': 16000, 'dia': 128000, 'mes': 3400000},
    'Soldador': {'hora': 24000, 'dia': 192000, 'mes': 5000000},
    'Operador Maquinaria': {'hora': 28000, 'dia': 224000, 'mes': 5800000},
    'Ingeniero Civil': {'hora': 45000, 'dia': 360000, 'mes': 9500000},
    'Arquitecto': {'hora': 42000, 'dia': 336000, 'mes': 8800000},
    'Capataz': {'hora': 30000, 'dia': 240000, 'mes': 6200000},
}

def actualizar_precios_reales():
    print("🇵🇾 ACTUALIZANDO PRECIOS REALES DE PARAGUAY 2024")
    print("=" * 60)
    
    # Actualizar materiales
    print("📦 Actualizando materiales...")
    for nombre, datos in MATERIALES_PRECIOS_PY.items():
        material, created = Material.objects.get_or_create(
            nombre=nombre,
            defaults={
                'descripcion': datos['descripcion'],
                'precio': Decimal(str(datos['precio'])),
                'unidad_medida': datos['unidad'],
                'stock': 100,  # Stock inicial
                'creado_por_id': 1,  # Asume que existe un usuario admin
                'activo': True
            }
        )
        if not created:
            material.precio = Decimal(str(datos['precio']))
            material.descripcion = datos['descripcion']
            material.unidad_medida = datos['unidad']
            material.save()
        
        print(f"   ✅ {nombre}: {datos['precio']:,} Gs./{datos['unidad']}")
    
    # Actualizar maquinarias
    print("\n🚜 Actualizando maquinarias...")
    for nombre, datos in MAQUINARIAS_ALQUILER_PY.items():
        maquinaria, created = Maquinaria.objects.get_or_create(
            nombre=nombre,
            defaults={
                'descripcion': datos['descripcion'],
                'costo_alquiler_dia': Decimal(str(datos['costo_dia'])),
                'estado': 'disponible',
                'creado_por_id': 1,
            }
        )
        if not created:
            maquinaria.costo_alquiler_dia = Decimal(str(datos['costo_dia']))
            maquinaria.descripcion = datos['descripcion']
            maquinaria.save()
        
        print(f"   ✅ {nombre}: {datos['costo_dia']:,} Gs./día")
    
    print("\n" + "=" * 60)
    print("🎉 PRECIOS REALES ACTUALIZADOS CORRECTAMENTE")
    print(f"📦 Materiales: {len(MATERIALES_PRECIOS_PY)}")
    print(f"🚜 Maquinarias: {len(MAQUINARIAS_ALQUILER_PY)}")
    print("💡 Todos los precios están basados en el mercado paraguayo 2024")

if __name__ == "__main__":
    actualizar_precios_reales()