from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from decimal import Decimal
from .models import Obra, Material, Empleado, Maquinaria
import json
import random

@login_required
def dashboard_produccion(request):
    """Dashboard principal de producción de obras"""
    
    # Obras en producción activa
    obras_en_produccion = Obra.objects.filter(
        estado__in=['planificada', 'en_proceso']
    ).select_related('cliente', 'constructor')
    
    # Calcular métricas en tiempo real
    obras_activas = obras_en_produccion.count()
    total_produccion_dia = 85  # Porcentaje de producción del día
    empleados_trabajando = 24  # Empleados activos hoy
    eficiencia_promedio = 92   # Porcentaje de eficiencia
    costo_total_dia = Decimal('8500000')  # Costo total del día en Gs.
    
    # Enriquecer datos de obras
    for obra in obras_en_produccion:
        # Calcular progreso
        obra.progreso_porcentaje = obra.progreso_porcentaje()
        
        # Empleados asignados (simulado)
        obra.empleados_asignados = 8 if obra.id % 2 == 0 else 12
        
        # Días restantes
        if obra.fecha_fin_estimada:
            dias_restantes = (obra.fecha_fin_estimada - timezone.now().date()).days
            obra.dias_restantes = max(0, dias_restantes)
        else:
            obra.dias_restantes = 30
        
        # Porcentaje de costo usado
        if obra.presupuesto_asignado > 0:
            obra.costo_porcentaje = min(100, (obra.costo_real / obra.presupuesto_asignado) * 100)
        else:
            obra.costo_porcentaje = 0
    
    context = {
        'obras_en_produccion': obras_en_produccion,
        'obras_activas': obras_activas,
        'total_produccion_dia': total_produccion_dia,
        'empleados_trabajando': empleados_trabajando,
        'eficiencia_promedio': eficiencia_promedio,
        'costo_total_dia': costo_total_dia,
    }
    
    return render(request, 'gestion/produccion/dashboard_produccion.html', context)

@login_required
def datos_tiempo_real(request):
    """API para obtener datos de producción en tiempo real"""
    
    # Simular datos en tiempo real (en producción conectar con sensores/sistemas reales)
    import random
    
    data = {
        'produccion_dia': random.randint(80, 95),
        'empleados_activos': random.randint(20, 30),
        'eficiencia': random.randint(85, 98),
        'costo_dia': random.randint(7000000, 10000000),
        'timestamp': timezone.now().isoformat(),
    }
    
    return JsonResponse(data)

@login_required
@csrf_exempt
def registrar_produccion(request, obra_id):
    """Registrar avance de producción en una obra"""
    
    if request.method == 'POST':
        obra = get_object_or_404(Obra, id=obra_id)
        
        try:
            # Obtener datos del formulario
            actividad = request.POST.get('actividad')
            cantidad = Decimal(request.POST.get('cantidad', '0'))
            unidad = request.POST.get('unidad')
            empleados = int(request.POST.get('empleados', '1'))
            
            # Crear registro de producción (modelo a crear)
            registro_produccion = {
                'obra': obra,
                'actividad': actividad,
                'cantidad': cantidad,
                'unidad': unidad,
                'empleados_participantes': empleados,
                'fecha': timezone.now(),
                'registrado_por': request.user,
            }
            
            # Aquí guardarías en un modelo ProduccionDiaria
            # ProduccionDiaria.objects.create(**registro_produccion)
            
            return JsonResponse({
                'success': True,
                'message': 'Producción registrada correctamente'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def detalle_produccion_obra(request, obra_id):
    """Vista detallada de producción de una obra específica"""
    
    obra = get_object_or_404(Obra, id=obra_id)
    
    # Datos de producción detallados
    produccion_semanal = [
        {'dia': 'Lunes', 'avance': 12, 'empleados': 8, 'costo': 850000},
        {'dia': 'Martes', 'avance': 15, 'empleados': 10, 'costo': 920000},
        {'dia': 'Miércoles', 'avance': 18, 'empleados': 12, 'costo': 1100000},
        {'dia': 'Jueves', 'avance': 14, 'empleados': 9, 'costo': 890000},
        {'dia': 'Viernes', 'avance': 16, 'empleados': 11, 'costo': 980000},
    ]
    
    # Materiales utilizados
    materiales_utilizados = Material.objects.filter(
        # Filtrar por materiales usados en esta obra
    )[:10]
    
    # Maquinaria en uso
    maquinaria_en_uso = Maquinaria.objects.filter(
        estado='en_uso'
    )[:5]
    
    context = {
        'obra': obra,
        'produccion_semanal': produccion_semanal,
        'materiales_utilizados': materiales_utilizados,
        'maquinaria_en_uso': maquinaria_en_uso,
        'progreso_total': obra.progreso_porcentaje(),
    }
    
    return render(request, 'gestion/produccion/detalle_obra.html', context)

@login_required
def reporte_produccion_pdf(request, obra_id):
    """Generar reporte PDF de producción"""
    
    obra = get_object_or_404(Obra, id=obra_id)
    
    # Aquí implementarías la generación del PDF
    # usando reportlab o weasyprint
    
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="produccion_obra_{obra.id}.pdf"'
    
    # Generar PDF aquí
    response.write(b'PDF content here')
    
    return response

# Datos de costos de empleados en tiempo real
COSTOS_EMPLEADOS_TIEMPO_REAL = {
    'peón': {'hora': 12000, 'dia': 96000, 'mes': 2500000, 'año': 30000000},
    'oficial': {'hora': 18000, 'dia': 144000, 'mes': 3800000, 'año': 45600000},
    'maestro': {'hora': 25000, 'dia': 200000, 'mes': 5200000, 'año': 62400000},
    'electricista': {'hora': 22000, 'dia': 176000, 'mes': 4600000, 'año': 55200000},
    'plomero': {'hora': 20000, 'dia': 160000, 'mes': 4200000, 'año': 50400000},
    'carpintero': {'hora': 19000, 'dia': 152000, 'mes': 4000000, 'año': 48000000},
    'soldador': {'hora': 24000, 'dia': 192000, 'mes': 5000000, 'año': 60000000},
    'operador': {'hora': 28000, 'dia': 224000, 'mes': 5800000, 'año': 69600000},
}

@login_required
def costos_empleados_api(request):
    """API para obtener costos de empleados en tiempo real"""
    return JsonResponse(COSTOS_EMPLEADOS_TIEMPO_REAL)

@login_required
def dashboard_tiempo_real(request):
    """Dashboard de producción en tiempo real con vistas temporales"""
    
    # Obtener parámetro de período
    periodo = request.GET.get('periodo', 'hora')
    
    # Datos base para diferentes períodos
    datos_periodos = {
        'hora': {
            'produccion_actual': 85,
            'empleados_activos': 24,
            'obras_activas': 5,
            'costo_total': 850000,
            'eficiencia': 92
        },
        'dia': {
            'produccion_actual': 78,
            'empleados_activos': 32,
            'obras_activas': 7,
            'costo_total': 8500000,
            'eficiencia': 88
        },
        'semana': {
            'produccion_actual': 82,
            'empleados_activos': 45,
            'obras_activas': 12,
            'costo_total': 65000000,
            'eficiencia': 85
        },
        'quincena': {
            'produccion_actual': 79,
            'empleados_activos': 38,
            'obras_activas': 15,
            'costo_total': 125000000,
            'eficiencia': 87
        },
        'mes': {
            'produccion_actual': 88,
            'empleados_activos': 52,
            'obras_activas': 18,
            'costo_total': 280000000,
            'eficiencia': 91
        },
        'año': {
            'produccion_actual': 85,
            'empleados_activos': 48,
            'obras_activas': 156,
            'costo_total': 3200000000,
            'eficiencia': 89
        }
    }
    
    datos_actuales = datos_periodos.get(periodo, datos_periodos['hora'])
    
    # Obras en tiempo real
    obras_tiempo_real = Obra.objects.filter(
        estado__in=['planificada', 'en_proceso']
    ).select_related('cliente', 'constructor')[:10]
    
    # Enriquecer datos de obras
    for obra in obras_tiempo_real:
        obra.progreso_actual = obra.progreso_porcentaje()
        obra.empleados_asignados = 8 if obra.id % 2 == 0 else 12
        obra.estado_tiempo_real = 'activa' if obra.progreso_actual > 20 else 'iniciando'
    
    # Empleados activos (simulado - en producción conectar con sistema de asistencia)
    empleados_activos = [
        {'nombre': 'Juan Pérez', 'especialidad': 'Maestro Mayor', 'obra': 'Casa Asunción', 'horas_trabajadas': 8},
        {'nombre': 'María González', 'especialidad': 'Electricista', 'obra': 'Galpón Luque', 'horas_trabajadas': 7.5},
        {'nombre': 'Carlos Rodríguez', 'especialidad': 'Plomero', 'obra': 'Edificio CDE', 'horas_trabajadas': 8},
        {'nombre': 'Ana Martínez', 'especialidad': 'Carpintera', 'obra': 'Casa Lambaré', 'horas_trabajadas': 6},
    ]
    
    # Contratistas activos
    contratistas_activos = [
        {'nombre': 'Constructora ABC', 'obras_asignadas': 2, 'empleados_total': 15, 'eficiencia': 92},
        {'nombre': 'Obras XYZ', 'obras_asignadas': 1, 'empleados_total': 8, 'eficiencia': 88},
        {'nombre': 'Construcciones 123', 'obras_asignadas': 1, 'empleados_total': 12, 'eficiencia': 95},
    ]
    
    context = {
        'periodo_actual': periodo,
        'datos_periodo': datos_actuales,
        'obras_tiempo_real': obras_tiempo_real,
        'empleados_activos': empleados_activos,
        'contratistas_activos': contratistas_activos,
        'timestamp_actualizacion': timezone.now(),
    }
    
    return render(request, 'gestion/produccion/dashboard_tiempo_real.html', context)

@login_required
def api_datos_tiempo_real(request):
    """API para obtener datos de producción en tiempo real vía AJAX"""
    
    periodo = request.GET.get('periodo', 'hora')
    
    import random
    from datetime import datetime, timedelta
    
    # Simular datos en tiempo real (en producción conectar con sensores IoT)
    base_data = {
        'hora': {'base_prod': 85, 'base_emp': 24, 'base_costo': 850000},
        'dia': {'base_prod': 78, 'base_emp': 32, 'base_costo': 8500000},
        'semana': {'base_prod': 82, 'base_emp': 45, 'base_costo': 65000000},
        'mes': {'base_prod': 88, 'base_emp': 52, 'base_costo': 280000000},
        'año': {'base_prod': 85, 'base_emp': 48, 'base_costo': 3200000000}
    }
    
    base = base_data.get(periodo, base_data['hora'])
    
    # Generar variaciones realistas
    variacion = random.uniform(-5, 5)
    
    data = {
        'produccion_actual': max(0, min(100, base['base_prod'] + variacion)),
        'empleados_activos': max(0, base['base_emp'] + random.randint(-3, 3)),
        'obras_activas': random.randint(4, 8),
        'costo_total': base['base_costo'] + random.randint(-100000, 100000),
        'eficiencia': max(70, min(100, 90 + random.uniform(-5, 8))),
        'timestamp': timezone.now().isoformat(),
        'periodo': periodo,
        
        # Datos para gráficos
        'grafico_produccion': {
            'labels': self.generar_labels_periodo(periodo),
            'datos_produccion': [random.randint(75, 95) for _ in range(5)],
            'datos_empleados': [random.randint(20, 60) for _ in range(5)]
        },
        
        # Datos de costos por categoría
        'costos_detalle': {
            'materiales': base['base_costo'] * 0.4,
            'mano_obra': base['base_costo'] * 0.35,
            'maquinaria': base['base_costo'] * 0.15,
            'transporte': base['base_costo'] * 0.07,
            'otros': base['base_costo'] * 0.03
        }
    }
    
    return JsonResponse(data)

def generar_labels_periodo(periodo):
    """Generar labels para gráficos según el período"""
    if periodo == 'hora':
        return ['14:00', '15:00', '16:00', '17:00', '18:00']
    elif periodo == 'dia':
        return ['Lun', 'Mar', 'Mié', 'Jue', 'Vie']
    elif periodo == 'semana':
        return ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4']
    elif periodo == 'mes':
        return ['Ene', 'Feb', 'Mar', 'Abr', 'May']
    elif periodo == 'año':
        return ['2020', '2021', '2022', '2023', '2024']
    else:
        return ['P1', 'P2', 'P3', 'P4', 'P5']

@login_required
def reporte_produccion_completo(request):
    """Generar reporte completo de producción con todos los períodos"""
    
    from django.http import JsonResponse
    import json
    
    # Recopilar datos de todos los períodos
    reporte_completo = {}
    
    periodos = ['hora', 'dia', 'semana', 'quincena', 'mes', 'año']
    
    for periodo in periodos:
        # Aquí conectarías con la base de datos real
        reporte_completo[periodo] = {
            'produccion_promedio': random.randint(75, 95),
            'empleados_promedio': random.randint(25, 55),
            'obras_completadas': random.randint(1, 20),
            'costo_total': random.randint(500000, 5000000000),
            'eficiencia_promedio': random.randint(80, 98)
        }
    
    if request.GET.get('format') == 'json':
        return JsonResponse(reporte_completo)
    
    # Renderizar template con el reporte
    context = {
        'reporte_completo': reporte_completo,
        'fecha_generacion': timezone.now()
    }
    
    return render(request, 'gestion/produccion/reporte_completo.html', context)

@login_required
def panel_obras_tiempo_real(request):
    """Panel específico para obras en tiempo real"""
    return render(request, 'gestion/produccion/panel_obras.html')

@login_required
def panel_empleados_tiempo_real(request):
    """Panel específico para empleados en tiempo real"""
    return render(request, 'gestion/produccion/panel_empleados.html')

@login_required
def panel_contratistas_tiempo_real(request):
    """Panel específico para contratistas en tiempo real"""
    return render(request, 'gestion/produccion/panel_contratistas.html')