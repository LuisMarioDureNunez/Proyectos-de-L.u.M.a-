
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, Avg
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import datetime, timedelta
import csv
from django.db.models.functions import TruncWeek, TruncMonth

# Importaciones específicas
from gestion.models import Obra, Presupuesto, Material, UsuarioPersonalizado

def es_administrador(user):
    return user.is_authenticated and user.es_administrador()

@login_required
@user_passes_test(es_administrador)
def reportes_avanzados(request):
    """Reportes avanzados del sistema"""
    
    # Filtros de fecha
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if fecha_inicio and fecha_fin:
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        except ValueError:
            fecha_fin = timezone.now()
            fecha_inicio = fecha_fin - timedelta(days=30)
    else:
        # Últimos 30 días por defecto
        fecha_fin = timezone.now()
        fecha_inicio = fecha_fin - timedelta(days=30)
    
    # Estadísticas generales
    stats = {
        'periodo': {
            'inicio': fecha_inicio,
            'fin': fecha_fin
        },
        'obras': {
            'total': Obra.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin]).count(),
            'por_estado': list(Obra.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
                          .values('estado').annotate(total=Count('id'))),
            'nuevas_por_semana': obtener_obras_por_semana(fecha_inicio, fecha_fin),
        },
        'presupuestos': {
            'total': Presupuesto.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin]).count(),
            'por_estado': list(Presupuesto.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
                            .values('estado').annotate(total=Count('id'))),
            'total_monto': Presupuesto.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
                          .aggregate(total=Sum('total'))['total'] or 0,
            'monto_promedio': Presupuesto.objects.filter(fecha_creacion__range=[fecha_inicio, fecha_fin])
                            .aggregate(promedio=Avg('total'))['promedio'] or 0,
        },
        'materiales': {
            'total': Material.objects.count(),
            'stock_bajo': Material.objects.filter(stock__lt=10).count(),
            'sin_stock': Material.objects.filter(stock=0).count(),
            'valor_total_inventario': Material.objects.aggregate(
                total=Sum('precio') * Sum('stock')
            )['total'] or 0,
        },
        'usuarios': {
            'total': UsuarioPersonalizado.objects.count(),
            'por_rol': list(UsuarioPersonalizado.objects.values('rol').annotate(total=Count('id'))),
            'nuevos_por_mes': obtener_usuarios_por_mes(fecha_inicio, fecha_fin),
        }
    }
    
    # Obras más grandes por presupuesto
    obras_mas_grandes = Obra.objects.filter(
        fecha_creacion__range=[fecha_inicio, fecha_fin]
    ).order_by('-presupuesto_asignado')[:10]
    
    # Clientes más activos
    clientes_activos = UsuarioPersonalizado.objects.filter(
        rol='cliente',
        obras_cliente__fecha_creacion__range=[fecha_inicio, fecha_fin]
    ).annotate(
        total_obras=Count('obras_cliente'),
        total_presupuestos=Count('presupuestos_cliente')
    ).order_by('-total_obras')[:10]
    
    context = {
        'stats': stats,
        'obras_mas_grandes': obras_mas_grandes,
        'clientes_activos': clientes_activos,
        'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d'),
        'fecha_fin': fecha_fin.strftime('%Y-%m-%d'),
    }
    
    return render(request, 'gestion/reportes/avanzados.html', context)

@login_required
def reporte_obras_json(request):
    """API JSON para gráficos de obras"""
    datos = Obra.objects.values('estado').annotate(total=Count('id'))
    
    data = {
        'labels': [item['estado'] for item in datos],
        'datasets': [{
            'data': [item['total'] for item in datos],
            'backgroundColor': ['#28a745', '#ffc107', '#17a2b8', '#dc3545']
        }]
    }
    
    return JsonResponse(data)

@login_required
def reporte_presupuestos_json(request):
    """API JSON para gráficos de presupuestos"""
    datos = Presupuesto.objects.values('estado').annotate(
        total=Count('id'),
        monto_total=Sum('total')
    )
    
    data = {
        'labels': [item['estado'] for item in datos],
        'datasets': [{
            'label': 'Cantidad',
            'data': [item['total'] for item in datos],
            'backgroundColor': '#17a2b8'
        }, {
            'label': 'Monto Total',
            'data': [float(item['monto_total'] or 0) for item in datos],
            'backgroundColor': '#28a745',
            'type': 'bar'
        }]
    }
    
    return JsonResponse(data)

@login_required
@user_passes_test(es_administrador)
def exportar_reporte(request, tipo):
    """Exportar reportes en diferentes formatos"""
    if tipo == 'obras':
        datos = Obra.objects.all().values(
            'nombre', 'ubicacion', 'estado', 'fecha_inicio', 
            'fecha_fin_estimada', 'presupuesto_asignado'
        )
        filename = 'reporte_obras.csv'
        
    elif tipo == 'presupuestos':
        datos = Presupuesto.objects.all().values(
            'obra__nombre', 'cliente__username', 'total', 
            'estado', 'fecha_creacion'
        )
        filename = 'reporte_presupuestos.csv'
        
    else:
        return HttpResponse('Tipo de reporte no válido')
    
    # Convertir a CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    if datos:
        writer = csv.writer(response)
        # Escribir headers
        writer.writerow(datos[0].keys())
        # Escribir datos
        for item in datos:
            writer.writerow(item.values())
    
    return response

# Funciones auxiliares
def obtener_obras_por_semana(fecha_inicio, fecha_fin):
    """Obtener cantidad de obras creadas por semana"""
    obras_por_semana = Obra.objects.filter(
        fecha_creacion__range=[fecha_inicio, fecha_fin]
    ).annotate(
        semana=TruncWeek('fecha_creacion')
    ).values('semana').annotate(
        total=Count('id')
    ).order_by('semana')
    
    return list(obras_por_semana)

def obtener_usuarios_por_mes(fecha_inicio, fecha_fin):
    """Obtener cantidad de usuarios registrados por mes"""
    usuarios_por_mes = UsuarioPersonalizado.objects.filter(
        date_joined__range=[fecha_inicio, fecha_fin]
    ).annotate(
        mes=TruncMonth('date_joined')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')
    
    return list(usuarios_por_mes)