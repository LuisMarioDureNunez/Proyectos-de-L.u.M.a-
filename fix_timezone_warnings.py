#!/usr/bin/env python3
# fix_timezone_warnings.py - Script para corregir warnings de timezone

import os
import sys
import django
from datetime import datetime
from django.utils import timezone

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_tienda.settings')
django.setup()

def fix_naive_datetimes():
    """Corrige fechas naive en la base de datos"""
    from gestion.models import Obra, Presupuesto
    
    print("Corrigiendo fechas naive en la base de datos...")
    
    # Corregir fechas en Obra
    obras_actualizadas = 0
    for obra in Obra.objects.all():
        updated = False
        
        if obra.fecha_creacion and timezone.is_naive(obra.fecha_creacion):
            obra.fecha_creacion = timezone.make_aware(obra.fecha_creacion)
            updated = True
            
        if obra.fecha_actualizacion and timezone.is_naive(obra.fecha_actualizacion):
            obra.fecha_actualizacion = timezone.make_aware(obra.fecha_actualizacion)
            updated = True
            
        if updated:
            obra.save()
            obras_actualizadas += 1
    
    # Corregir fechas en Presupuesto
    presupuestos_actualizados = 0
    for presupuesto in Presupuesto.objects.all():
        updated = False
        
        if presupuesto.fecha_creacion and timezone.is_naive(presupuesto.fecha_creacion):
            presupuesto.fecha_creacion = timezone.make_aware(presupuesto.fecha_creacion)
            updated = True
            
        if presupuesto.fecha_actualizacion and timezone.is_naive(presupuesto.fecha_actualizacion):
            presupuesto.fecha_actualizacion = timezone.make_aware(presupuesto.fecha_actualizacion)
            updated = True
            
        if updated:
            presupuesto.save()
            presupuestos_actualizados += 1
    
    print(f"Obras actualizadas: {obras_actualizadas}")
    print(f"Presupuestos actualizados: {presupuestos_actualizados}")
    print("Correccion de fechas completada!")

if __name__ == '__main__':
    fix_naive_datetimes()