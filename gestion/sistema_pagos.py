"""
SISTEMA DE PAGOS - LUMA PARAGUAY
Procesamiento de pagos con múltiples métodos
"""
from django.db import models
from decimal import Decimal
from django.utils import timezone
from .models import UsuarioPersonalizado, Presupuesto, Obra

class MetodoPago(models.Model):
    """Métodos de pago disponibles"""
    TIPOS = [
        ('tarjeta', '💳 Tarjeta'),
        ('transferencia', '🏦 Transferencia'),
        ('efectivo', '💵 Efectivo'),
        ('cheque', '📝 Cheque'),
        ('crypto', '₿ Criptomonedas')
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    activo = models.BooleanField(default=True)
    comision_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.nombre}"

class Pago(models.Model):
    """Registro de pagos"""
    ESTADOS = [
        ('pendiente', '⏳ Pendiente'),
        ('procesando', '🔄 Procesando'),
        ('completado', '✅ Completado'),
        ('fallido', '❌ Fallido'),
        ('reembolsado', '↩️ Reembolsado')
    ]
    
    codigo = models.CharField(max_length=50, unique=True)
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='pagos')
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.PROTECT)
    
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    comision = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    monto_total = models.DecimalField(max_digits=15, decimal_places=2)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    referencia_externa = models.CharField(max_length=200, blank=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_procesado = models.DateTimeField(null=True, blank=True)
    fecha_completado = models.DateTimeField(null=True, blank=True)
    
    notas = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return f"Pago {self.codigo} - ₲{self.monto_total}"
    
    def procesar_pago(self):
        """Procesa el pago"""
        self.estado = 'procesando'
        self.fecha_procesado = timezone.now()
        self.save()
        
        # Simular procesamiento
        import time
        time.sleep(2)
        
        self.estado = 'completado'
        self.fecha_completado = timezone.now()
        self.save()
        
        # Actualizar presupuesto
        self.presupuesto.estado = 'aceptado'
        self.presupuesto.save()
        
        return True

class CuotaPago(models.Model):
    """Cuotas de pago para pagos en cuotas"""
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name='cuotas')
    numero_cuota = models.IntegerField()
    monto = models.DecimalField(max_digits=15, decimal_places=2)
    fecha_vencimiento = models.DateField()
    fecha_pago = models.DateTimeField(null=True, blank=True)
    pagada = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['numero_cuota']
    
    def __str__(self):
        return f"Cuota {self.numero_cuota} - ₲{self.monto}"

class HistorialPago(models.Model):
    """Historial de cambios en pagos"""
    pago = models.ForeignKey(Pago, on_delete=models.CASCADE, related_name='historial')
    estado_anterior = models.CharField(max_length=20)
    estado_nuevo = models.CharField(max_length=20)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-fecha']
