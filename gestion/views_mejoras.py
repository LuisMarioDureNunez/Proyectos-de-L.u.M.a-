# views_mejoras.py - Vistas para las nuevas funcionalidades increíbles
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg, Q
from decimal import Decimal
from datetime import datetime, timedelta
from django.utils import timezone

from .models import *

# =============================================
# DASHBOARD INTERACTIVO
# =============================================

@login_required
def dashboard_interactivo(request):
    """Dashboard interactivo con gráficos en tiempo real"""
    
    # Estadísticas generales
    stats = {
        'total_obras': Obra.objects.count(),
        'obras_en_proceso': Obra.objects.filter(estado='en_proceso').count(),
        'obras_planificadas': Obra.objects.filter(estado='planificada').count(),
        'obras_finalizadas': Obra.objects.filter(estado='finalizada').count(),
        'obras_suspendidas': Obra.objects.filter(estado='suspendida').count(),
        'total_materiales': Material.objects.count(),
        'stock_bajo': Material.objects.filter(stock__lt=10, stock__gt=0).count(),
        'total_presupuestos_aceptados': Presupuesto.objects.filter(
            estado='aceptado'
        ).aggregate(total=Sum('total'))['total'] or Decimal('0'),
    }
    
    context = {
        'stats': stats,
    }
    
    return render(request, 'gestion/dashboard/dashboard_interactivo.html', context)


# =============================================
# GALERÍA DE OBRAS
# =============================================

@login_required
def galeria_obras(request):
    """Galería de obras con filtros y slider"""
    
    obras = Obra.objects.all().order_by('-fecha_creacion')
    
    # Filtros
    estado = request.GET.get('estado')
    if estado:
        obras = obras.filter(estado=estado)
    
    context = {
        'obras': obras,
    }
    
    return render(request, 'gestion/obras/galeria.html', context)


# =============================================
# CALENDARIO DE OBRAS
# =============================================

@login_required
def calendario_obras(request):
    """Calendario interactivo de obras"""
    
    if request.user.es_administrador() or request.user.rol == 'constructor':
        obras = Obra.objects.all()
    else:
        obras = Obra.objects.filter(cliente=request.user)
    
    context = {
        'obras': obras,
    }
    
    return render(request, 'gestion/obras/calendario.html', context)


# =============================================
# API PARA NOTIFICACIONES EN TIEMPO REAL
# =============================================

@login_required
def api_notificaciones(request):
    """API para obtener notificaciones del usuario"""
    
    notificaciones = Notificacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha_creacion')[:10]
    
    data = []
    for notif in notificaciones:
        data.append({
            'id': notif.id,
            'tipo': notif.tipo,
            'titulo': notif.titulo,
            'mensaje': notif.mensaje,
            'leida': notif.leida,
            'fecha': notif.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S'),
            'icono': notif.get_icono(),
        })
    
    return JsonResponse({
        'success': True,
        'notificaciones': data,
        'no_leidas': notificaciones.filter(leida=False).count()
    })


@login_required
def marcar_notificacion_leida(request, notificacion_id):
    """Marcar notificación como leída"""
    
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    notificacion.marcar_como_leida()
    
    return JsonResponse({'success': True})


@login_required
def lista_notificaciones(request):
    """Lista completa de notificaciones"""
    
    notificaciones = Notificacion.objects.filter(
        usuario=request.user
    ).order_by('-fecha_creacion')
    
    context = {
        'notificaciones': notificaciones,
    }
    
    return render(request, 'gestion/notificaciones/lista.html', context)


# =============================================
# ESTADÍSTICAS AVANZADAS PARA GRÁFICOS
# =============================================

@login_required
def api_estadisticas_dashboard(request):
    """API para obtener estadísticas para gráficos"""
    
    # Ingresos vs Gastos últimos 6 meses
    hoy = timezone.now().date()
    meses = []
    ingresos = []
    gastos = []
    
    for i in range(5, -1, -1):
        mes = hoy - timedelta(days=30*i)
        mes_inicio = mes.replace(day=1)
        mes_fin = (mes_inicio + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        ingreso_mes = Presupuesto.objects.filter(
            estado='aceptado',
            fecha_creacion__gte=mes_inicio,
            fecha_creacion__lte=mes_fin
        ).aggregate(total=Sum('total'))['total'] or 0
        
        gasto_mes = Obra.objects.filter(
            fecha_creacion__gte=mes_inicio,
            fecha_creacion__lte=mes_fin
        ).aggregate(total=Sum('costo_real'))['total'] or 0
        
        meses.append(mes.strftime('%B'))
        ingresos.append(float(ingreso_mes))
        gastos.append(float(gasto_mes))
    
    # Materiales más usados
    materiales_top = Material.objects.annotate(
        veces_usado=Count('itempresupuesto')
    ).order_by('-veces_usado')[:5]
    
    materiales_nombres = [m.nombre for m in materiales_top]
    materiales_cantidades = [m.veces_usado for m in materiales_top]
    
    return JsonResponse({
        'success': True,
        'ingresos_gastos': {
            'meses': meses,
            'ingresos': ingresos,
            'gastos': gastos
        },
        'materiales': {
            'nombres': materiales_nombres,
            'cantidades': materiales_cantidades
        }
    })


# =============================================
# BÚSQUEDA GLOBAL AVANZADA
# =============================================

@login_required
def busqueda_global(request):
    """Búsqueda avanzada en todo el sistema"""
    
    query = request.GET.get('q', '')
    
    if not query:
        return JsonResponse({'resultados': []})
    
    resultados = []
    
    # Buscar en Obras
    obras = Obra.objects.filter(
        Q(nombre__icontains=query) |
        Q(descripcion__icontains=query) |
        Q(ubicacion__icontains=query)
    )[:5]
    
    for obra in obras:
        resultados.append({
            'tipo': 'obra',
            'icono': '🏗️',
            'titulo': obra.nombre,
            'subtitulo': obra.ubicacion,
            'url': f'/obras/{obra.id}/'
        })
    
    # Buscar en Materiales
    materiales = Material.objects.filter(
        Q(nombre__icontains=query) |
        Q(descripcion__icontains=query)
    )[:5]
    
    for material in materiales:
        resultados.append({
            'tipo': 'material',
            'icono': '📦',
            'titulo': material.nombre,
            'subtitulo': f'Stock: {material.stock}',
            'url': f'/materiales/{material.id}/'
        })
    
    # Buscar en Presupuestos
    presupuestos = Presupuesto.objects.filter(
        Q(codigo_presupuesto__icontains=query) |
        Q(obra__nombre__icontains=query)
    )[:5]
    
    for presupuesto in presupuestos:
        resultados.append({
            'tipo': 'presupuesto',
            'icono': '💰',
            'titulo': presupuesto.codigo_presupuesto,
            'subtitulo': presupuesto.obra.nombre,
            'url': f'/presupuestos/{presupuesto.id}/'
        })
    
    return JsonResponse({
        'success': True,
        'resultados': resultados,
        'total': len(resultados)
    })