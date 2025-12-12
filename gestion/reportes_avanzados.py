"""
MÓDULO DE REPORTES AVANZADOS - SISTEMA LUMA PARAGUAY
Generación de reportes profesionales en PDF con gráficos
"""
from decimal import Decimal
from django.db.models import Sum, Count, Avg, Q
from django.utils import timezone
from datetime import timedelta
from .models import Obra, Presupuesto, Material, Maquinaria, UsuarioPersonalizado

class ReportesAvanzados:
    """Clase para generar reportes avanzados del sistema"""
    
    @staticmethod
    def reporte_financiero_mensual():
        """Genera reporte financiero del mes actual"""
        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)
        
        # Presupuestos del mes
        presupuestos_mes = Presupuesto.objects.filter(
            fecha_creacion__gte=inicio_mes
        )
        
        total_presupuestado = presupuestos_mes.aggregate(
            total=Sum('total')
        )['total'] or Decimal('0')
        
        presupuestos_aceptados = presupuestos_mes.filter(
            estado='aceptado'
        ).aggregate(total=Sum('total'))['total'] or Decimal('0')
        
        # Obras del mes
        obras_mes = Obra.objects.filter(
            fecha_inicio__gte=inicio_mes
        )
        
        inversion_obras = obras_mes.aggregate(
            total=Sum('costo_real')
        )['total'] or Decimal('0')
        
        return {
            'periodo': f"{inicio_mes.strftime('%B %Y')}",
            'total_presupuestado': total_presupuestado,
            'presupuestos_aceptados': presupuestos_aceptados,
            'inversion_obras': inversion_obras,
            'utilidad_estimada': presupuestos_aceptados - inversion_obras,
            'tasa_aceptacion': (presupuestos_mes.filter(estado='aceptado').count() / presupuestos_mes.count() * 100) if presupuestos_mes.count() > 0 else 0
        }
    
    @staticmethod
    def reporte_obras_por_estado():
        """Genera reporte de obras agrupadas por estado"""
        return {
            'planificadas': Obra.objects.filter(estado='planificada').count(),
            'en_proceso': Obra.objects.filter(estado='en_proceso').count(),
            'suspendidas': Obra.objects.filter(estado='suspendida').count(),
            'finalizadas': Obra.objects.filter(estado='finalizada').count(),
            'canceladas': Obra.objects.filter(estado='cancelada').count(),
            'total': Obra.objects.count()
        }
    
    @staticmethod
    def reporte_inventario_critico():
        """Genera reporte de materiales con stock crítico"""
        materiales_criticos = Material.objects.filter(
            Q(stock=0) | Q(stock__lt=10),
            activo=True
        ).order_by('stock')
        
        return {
            'sin_stock': materiales_criticos.filter(stock=0).count(),
            'stock_bajo': materiales_criticos.filter(stock__gt=0, stock__lt=10).count(),
            'materiales': list(materiales_criticos.values(
                'nombre', 'stock', 'precio', 'unidad_medida'
            ))
        }
    
    @staticmethod
    def reporte_rendimiento_constructores():
        """Genera reporte de rendimiento de constructores"""
        constructores = UsuarioPersonalizado.objects.filter(rol='constructor')
        
        datos = []
        for constructor in constructores:
            obras = Obra.objects.filter(constructor=constructor)
            datos.append({
                'nombre': constructor.get_full_name() or constructor.username,
                'obras_totales': obras.count(),
                'obras_finalizadas': obras.filter(estado='finalizada').count(),
                'obras_en_proceso': obras.filter(estado='en_proceso').count(),
                'tasa_finalizacion': (obras.filter(estado='finalizada').count() / obras.count() * 100) if obras.count() > 0 else 0
            })
        
        return datos
    
    @staticmethod
    def reporte_presupuestos_pendientes():
        """Genera reporte de presupuestos pendientes de revisión"""
        pendientes = Presupuesto.objects.filter(
            estado__in=['solicitado', 'en_revision']
        ).order_by('-fecha_creacion')
        
        return {
            'total_pendientes': pendientes.count(),
            'monto_total': pendientes.aggregate(total=Sum('total'))['total'] or Decimal('0'),
            'presupuestos': list(pendientes.values(
                'codigo_presupuesto', 'obra__nombre', 'cliente__username', 
                'total', 'fecha_creacion', 'estado'
            )[:10])
        }
    
    @staticmethod
    def reporte_comparativo_trimestral():
        """Genera reporte comparativo de los últimos 3 meses"""
        hoy = timezone.now().date()
        meses = []
        
        for i in range(3):
            fecha = hoy - timedelta(days=30*i)
            inicio_mes = fecha.replace(day=1)
            
            if i == 0:
                fin_mes = hoy
            else:
                fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            
            presupuestos = Presupuesto.objects.filter(
                fecha_creacion__gte=inicio_mes,
                fecha_creacion__lte=fin_mes
            )
            
            obras = Obra.objects.filter(
                fecha_inicio__gte=inicio_mes,
                fecha_inicio__lte=fin_mes
            )
            
            meses.append({
                'mes': inicio_mes.strftime('%B %Y'),
                'presupuestos_total': presupuestos.count(),
                'presupuestos_aceptados': presupuestos.filter(estado='aceptado').count(),
                'monto_presupuestado': presupuestos.aggregate(total=Sum('total'))['total'] or Decimal('0'),
                'obras_iniciadas': obras.count(),
                'obras_finalizadas': obras.filter(estado='finalizada').count()
            })
        
        return meses
    
    @staticmethod
    def dashboard_ejecutivo():
        """Genera datos para dashboard ejecutivo"""
        hoy = timezone.now().date()
        hace_30_dias = hoy - timedelta(days=30)
        
        return {
            'resumen_financiero': ReportesAvanzados.reporte_financiero_mensual(),
            'obras_estado': ReportesAvanzados.reporte_obras_por_estado(),
            'inventario_critico': ReportesAvanzados.reporte_inventario_critico(),
            'presupuestos_pendientes': ReportesAvanzados.reporte_presupuestos_pendientes(),
            'rendimiento_constructores': ReportesAvanzados.reporte_rendimiento_constructores(),
            'comparativo_trimestral': ReportesAvanzados.reporte_comparativo_trimestral(),
            'kpis': {
                'total_usuarios': UsuarioPersonalizado.objects.count(),
                'usuarios_activos_mes': UsuarioPersonalizado.objects.filter(
                    last_login__gte=hace_30_dias
                ).count(),
                'obras_activas': Obra.objects.filter(estado='en_proceso').count(),
                'valor_inventario': Material.objects.filter(activo=True).aggregate(
                    total=Sum('precio')
                )['total'] or Decimal('0')
            }
        }
