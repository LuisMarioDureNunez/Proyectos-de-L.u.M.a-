# models.py CORREGIDO Y MEJORADO
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.validators import MinValueValidator
from decimal import Decimal
from django.utils import timezone
from django.contrib.auth import get_user_model
import json

# =============================================
# MODELO DE USUARIO PERSONALIZADO CON ROLES
# =============================================

class UsuarioPersonalizado(AbstractUser):
    """Usuario personalizado con sistema de roles"""
    ROLES = (
        ('admin', '👑 Administrador'),
        ('vendedor', '💰 Vendedor'), 
        ('cliente', '👤 Cliente'),
        ('constructor', '👷 Constructor'),
    )
    
    rol = models.CharField(max_length=20, choices=ROLES, default='cliente')
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    es_activo = models.BooleanField(default=True)
    
    # AQUÍ ESTÁN LOS MÉTODOS CORRECTAMENTE INDENTADOS (4 espacios)
    def puede_gestionar_obras(self):
        """Determina si el usuario puede gestionar obras"""
        return self.rol in ['admin', 'vendedor']
    
    def puede_gestionar_productos(self):
        """Determina si el usuario puede gestionar productos"""
        return self.rol in ['admin', 'vendedor']
    
    def puede_gestionar_usuarios(self):
        """Determina si el usuario puede gestionar usuarios"""
        return self.rol == 'admin'
    
    def get_rol_display(self):
        """Retorna el nombre del rol"""
        return dict(self.ROLES).get(self.rol, self.rol)
    # Relación con tienda (para vendedores)
    tienda = models.ForeignKey('Tienda', on_delete=models.SET_NULL, blank=True, null=True, related_name='vendedores')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        permissions = [
            ("puede_ver_dashboard", "Puede ver dashboard"),
            ("puede_gestionar_productos", "Puede gestionar productos"),
            ("puede_ver_reportes", "Puede ver reportes"),
            ("puede_gestionar_usuarios", "Puede gestionar usuarios"),
            ("puede_gestionar_obras", "Puede gestionar obras"),  # NUEVO
            ("puede_gestionar_presupuestos", "Puede gestionar presupuestos"),  # NUEVO
        ]
    
    def __str__(self):
        return "{} ({})".format(self.username, self.get_rol_display())
    
    def es_administrador(self):
        return self.rol == 'admin' or self.is_superuser
    
    def es_vendedor(self):
        return self.rol == 'vendedor'
    
    def es_cliente(self):
        return self.rol == 'cliente'
    
    def es_constructor(self):
        return self.rol == 'constructor'
    
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return '/static/images/avatar-default.png'

# =============================================
# MODELOS PARA EL DIAGRAMA DE CASOS DE USO
# =============================================

class Material(models.Model):
    """Materiales de construcción"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    unidad_medida = models.CharField(max_length=20, default='unidad')
    creado_por = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='materiales_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return "{} - ${}".format(self.nombre, self.precio)

class Maquinaria(models.Model):
    """Maquinarias para construcción"""
    ESTADOS_MAQUINARIA = [
        ('disponible', '✅ Disponible'),
        ('mantenimiento', '🔧 En Mantenimiento'),
        ('alquilada', '🚚 Alquilada'),
        ('reparacion', '⚠️ En Reparación'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    modelo = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_MAQUINARIA, default='disponible')
    costo_alquiler_dia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    creado_por = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='maquinarias_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Maquinaria'
        verbose_name_plural = 'Maquinarias'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return "{} - {}".format(self.nombre, self.get_estado_display())

class Herramienta(models.Model):
    """Herramientas de construcción"""
    ESTADOS_HERRAMIENTA = [
        ('disponible', '✅ Disponible'),
        ('mantenimiento', '🔧 En Mantenimiento'),
        ('en_uso', '🛠️ En Uso'),
        ('perdida', '❌ Perdida'),
    ]
    
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS_HERRAMIENTA, default='disponible')
    cantidad_total = models.IntegerField(default=1)
    cantidad_disponible = models.IntegerField(default=1)
    creado_por = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='herramientas_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Herramienta'
        verbose_name_plural = 'Herramientas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return "{} - {}/{} disp.".format(self.nombre, self.cantidad_disponible, self.cantidad_total)

class Obra(models.Model):
    """Obras de construcción"""
    ESTADOS_OBRA = [
        ('planificada', '📋 Planificada'),
        ('en_proceso', '🚧 En Proceso'),
        ('suspendida', '⏸️ Suspendida'),
        ('finalizada', '✅ Finalizada'),
        ('cancelada', '❌ Cancelada'),
    ]
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    ubicacion = models.CharField(max_length=200, blank=True, null=True)
    cliente = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='obras_cliente', limit_choices_to={'rol': 'cliente'})
    constructor = models.ForeignKey(UsuarioPersonalizado, on_delete=models.SET_NULL, null=True, blank=True, related_name='obras_constructor', limit_choices_to={'rol': 'constructor'})
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField(null=True, blank=True)
    fecha_fin_real = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_OBRA, default='planificada')
    presupuesto_asignado = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    costo_real = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    creado_por = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='obras_creadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Obra'
        verbose_name_plural = 'Obras'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return "{} - {}".format(self.nombre, self.get_estado_display())
    
    def duracion_dias(self):
        """Calcula la duración de la obra en días"""
        if self.fecha_inicio and self.fecha_fin_real:
            return (self.fecha_fin_real - self.fecha_inicio).days
        elif self.fecha_inicio and self.fecha_fin_estimada:
            return (self.fecha_fin_estimada - self.fecha_inicio).days
        return 0
    
    def progreso_porcentaje(self):
        """Calcula el progreso de la obra"""
        if self.estado == 'finalizada':
            return 100
        elif self.estado == 'en_proceso':
            return 50
        elif self.estado == 'planificada':
            return 10
        return 0

class Presupuesto(models.Model):
    """Presupuestos para obras con cálculos automáticos en Guaraníes"""
    ESTADOS_PRESUPUESTO = [
        ('solicitado', '📨 Solicitado'),
        ('en_revision', '🔍 En Revisión'),
        ('aceptado', '✅ Aceptado'),
        ('rechazado', '❌ Rechazado'),
        ('replanteado', '🔄 Replanteado'),
    ]
    
    obra = models.ForeignKey('Obra', on_delete=models.CASCADE, related_name='presupuestos')
    cliente = models.ForeignKey('UsuarioPersonalizado', on_delete=models.CASCADE, related_name='presupuestos_cliente')
    constructor = models.ForeignKey('UsuarioPersonalizado', on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='presupuestos_constructor')
    
    # Campos de cálculo automático
    subtotal = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    iva_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=10, validators=[MinValueValidator(Decimal('0'))])
    iva_monto = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    total = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    
    # Campos de control
    codigo_presupuesto = models.CharField(max_length=20, unique=True, blank=True)
    descripcion_servicios = models.TextField()
    fecha_validez = models.DateField(null=True, blank=True)
    dias_validez = models.IntegerField(default=30)
    
    # Estado y seguimiento
    estado = models.CharField(max_length=20, choices=ESTADOS_PRESUPUESTO, default='solicitado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)
    
    # Métodos de cálculo automático
    def calcular_totales(self):
        """Calcula automáticamente subtotal, IVA y total"""
        items = self.items.all()
        self.subtotal = sum(item.total for item in items) if items else Decimal('0')
        self.iva_monto = (self.subtotal * self.iva_porcentaje) / Decimal('100')
        self.total = self.subtotal + self.iva_monto
        self.save()
    
    def generar_codigo(self):
        """Genera código único para el presupuesto"""
        if not self.codigo_presupuesto:
            from django.utils import timezone
            fecha = timezone.now().strftime('%Y%m%d')
            ultimo_presupuesto = Presupuesto.objects.filter(
                codigo_presupuesto__startswith=f'PY-{fecha}'
            ).order_by('-codigo_presupuesto').first()
            
            if ultimo_presupuesto:
                ultimo_numero = int(ultimo_presupuesto.codigo_presupuesto.split('-')[-1])
                nuevo_numero = ultimo_numero + 1
            else:
                nuevo_numero = 1
                
            self.codigo_presupuesto = f'PY-{fecha}-{nuevo_numero:04d}'
    
    def get_fecha_vencimiento(self):
        """Calcula fecha de vencimiento automáticamente"""
        from django.utils import timezone
        if self.fecha_creacion and self.dias_validez:
            return self.fecha_creacion + timezone.timedelta(days=self.dias_validez)
        return None
    
    def esta_vencido(self):
        """Verifica si el presupuesto está vencido"""
        fecha_vencimiento = self.get_fecha_vencimiento()
        if fecha_vencimiento:
            from django.utils import timezone
            return timezone.now().date() > fecha_vencimiento
        return False
    
    def puede_ser_aceptado(self):
        """Verifica si el presupuesto puede ser aceptado"""
        return self.estado in ['solicitado', 'en_revision'] and not self.esta_vencido()
    
    def save(self, *args, **kwargs):
        # Generar código automáticamente si no existe
        if not self.codigo_presupuesto:
            self.generar_codigo()
        
        # Si el presupuesto es aceptado, actualizar la obra
        if self.estado == 'aceptado' and not self.fecha_aprobacion:
            from django.utils import timezone
            self.fecha_aprobacion = timezone.now()
            self.obra.presupuesto_asignado = self.total
            self.obra.estado = 'en_proceso'
            self.obra.save()
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Presupuesto'
        verbose_name_plural = 'Presupuestos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return "{} - {} - {} Gs.".format(self.codigo_presupuesto, self.obra.nombre, self.total)

class ItemPresupuesto(models.Model):
    """Items detallados del presupuesto con cálculos automáticos"""
    TIPOS_ITEM = [
        ('material', '📦 Material'),
        ('mano_obra', '👷 Mano de Obra'),
        ('maquinaria', '🚜 Maquinaria'),
        ('herramienta', '🛠️ Herramienta'),
        ('servicio', '🔧 Servicio'),
        ('gastos_generales', '🏢 Gastos Generales'),
        ('utilidad', '💰 Utilidad'),
        ('otros', '📋 Otros'),
    ]
    
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE, related_name='items')
    tipo = models.CharField(max_length=20, choices=TIPOS_ITEM, default='material')
    descripcion = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=1, validators=[MinValueValidator(Decimal('0.01'))])
    unidad_medida = models.CharField(max_length=20, default='unidad')
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Relaciones opcionales para inventario
    material = models.ForeignKey('Material', on_delete=models.SET_NULL, null=True, blank=True)
    maquinaria = models.ForeignKey('Maquinaria', on_delete=models.SET_NULL, null=True, blank=True)
    herramienta = models.ForeignKey('Herramienta', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campos adicionales
    orden = models.IntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Item de Presupuesto'
        verbose_name_plural = 'Items de Presupuesto'
        ordering = ['orden', 'id']
    
    def __str__(self):
        return "{} - {} {} x {} Gs.".format(self.descripcion, self.cantidad, self.unidad_medida, self.precio_unitario)
    
    def calcular_total(self):
        """Calcula el total automáticamente"""
        return self.cantidad * self.precio_unitario
    
    def save(self, *args, **kwargs):
        # Calcular total automáticamente
        self.total = self.calcular_total()
        
        # Si está relacionado con un material, usar su precio
        if self.material and not self.precio_unitario:
            self.precio_unitario = self.material.precio
        
        super().save(*args, **kwargs)
        
        # Recalcular totales del presupuesto
        if self.presupuesto:
            self.presupuesto.calcular_totales()

# =============================================
# MODELOS EXISTENTES (MANTENER)
# =============================================

class Tienda(models.Model):
    """Tiendas para sistema multi-vendedor"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='logos_tiendas/', blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    propietario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='tiendas_propiedad')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tienda'
        verbose_name_plural = 'Tiendas'
    
    def __str__(self):
        return self.nombre

class Categoria(models.Model):
    """Categorías de productos"""
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='categorias', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        unique_together = [['nombre', 'tienda']]
    
    def __str__(self):
        if self.tienda:
            return "{} - {}".format(self.nombre, self.tienda.nombre)
        return self.nombre

class Producto(models.Model):
    """Productos de la tienda"""
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    creado_por = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='productos_creados', null=True, blank=True)
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    activo = models.BooleanField(default=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    peso = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    dimensiones = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return "{} - ${}".format(self.nombre, self.precio)

class Carrito(models.Model):
    """Carrito de compras"""
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='carrito')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carrito'
        verbose_name_plural = 'Carritos'
    
    def __str__(self):
        return "Carrito de {}".format(self.usuario.username)

class ItemCarrito(models.Model):
    """Items del carrito de compras"""
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['carrito', 'producto']
        verbose_name = 'Item del Carrito'
        verbose_name_plural = 'Items del Carrito'
    
    def __str__(self):
        return "{} x {}".format(self.cantidad, self.producto.nombre)

class Pedido(models.Model):
    """Pedidos de clientes"""
    ESTADOS_PEDIDO = [
        ('pendiente', '🟡 Pendiente'),
        ('confirmado', '🔵 Confirmado'),
        ('preparando', '🟠 Preparando'),
        ('enviado', '🚚 Enviado'),
        ('entregado', '✅ Entregado'),
        ('cancelado', '❌ Cancelado'),
    ]
    
    METODOS_PAGO = [
        ('tarjeta', '💳 Tarjeta Crédito/Débito'),
        ('paypal', '📧 PayPal'),
        ('transferencia', '🏦 Transferencia Bancaria'),
        ('efectivo', '💰 Efectivo al recibir'),
    ]
    
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='pedidos')
    tienda = models.ForeignKey(Tienda, on_delete=models.CASCADE, related_name='pedidos', null=True, blank=True)
    numero_pedido = models.CharField(max_length=20, unique=True, blank=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO)
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    ciudad = models.CharField(max_length=50)
    codigo_postal = models.CharField(max_length=10)
    pais = models.CharField(max_length=50, default='Paraguay')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    impuesto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    envio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pago_id = models.CharField(max_length=100, blank=True, null=True)
    pago_estado = models.CharField(max_length=50, blank=True, null=True)
    notas = models.TextField(blank=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_entrega = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-fecha_pedido']
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
    
    def __str__(self):
        return "Pedido #{} - {}".format(self.numero_pedido, self.usuario.username)

class ItemPedido(models.Model):
    """Items de un pedido"""
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='items')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'Item de Pedido'
        verbose_name_plural = 'Items de Pedido'
    
    def __str__(self):
        return "{} x {}".format(self.cantidad, self.producto.nombre)

# =============================================
# SEÑALES
# =============================================

@receiver(post_save, sender=UsuarioPersonalizado)
def crear_carrito_usuario(sender, instance, created, **kwargs):
    """Crear carrito automáticamente cuando se crea un usuario"""
    if created:
        Carrito.objects.create(usuario=instance)

class Notificacion(models.Model):
    """Sistema de notificaciones en tiempo real"""
    TIPOS_NOTIFICACION = [
        ('presupuesto_creado', '📋 Presupuesto Creado'),
        ('presupuesto_aceptado', '✅ Presupuesto Aceptado'),
        ('presupuesto_rechazado', '❌ Presupuesto Rechazado'),
        ('obra_iniciada', '🏗️ Obra Iniciada'),
        ('obra_finalizada', '🎉 Obra Finalizada'),
        ('material_stock_bajo', '📦 Stock Bajo'),
        ('pago_realizado', '💰 Pago Realizado'),
        ('sistema', '🔔 Notificación del Sistema'),
        ('importante', '⚠️ Importante'),
    ]
    
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='notificaciones')
    tipo = models.CharField(max_length=25, choices=TIPOS_NOTIFICACION, default='sistema')
    titulo = models.CharField(max_length=250)
    mensaje = models.TextField()
    datos_extra = models.JSONField(default=dict, blank=True)  # Datos adicionales para la notificación
    
    # Estado de la notificación
    leida = models.BooleanField(default=False)
    enviada = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_leida = models.DateTimeField(null=True, blank=True)
    
    # Relaciones opcionales
    presupuesto = models.ForeignKey('Presupuesto', on_delete=models.CASCADE, null=True, blank=True)
    obra = models.ForeignKey('Obra', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_creacion']
        indexes = [
            models.Index(fields=['usuario', 'leida']),
            models.Index(fields=['fecha_creacion']),
        ]
    
    def __str__(self):
        return "{} - {}".format(self.get_tipo_display(), self.usuario.username)
    
    def marcar_como_leida(self):
        """Marcar notificación como leída"""
        if not self.leida:
            self.leida = True
            self.fecha_leida = timezone.now()
            self.save()
    
    def get_icono(self):
        """Obtener icono según el tipo de notificación"""
        iconos = {
            'presupuesto_creado': '📋',
            'presupuesto_aceptado': '✅',
            'presupuesto_rechazado': '❌',
            'obra_iniciada': '🏗️',
            'obra_finalizada': '🎉',
            'material_stock_bajo': '📦',
            'pago_realizado': '💰',
            'sistema': '🔔',
            'importante': '⚠️',
        }
        return iconos.get(self.tipo, '🔔')
    
    def get_color(self):
        """Obtener color CSS según el tipo"""
        colores = {
            'presupuesto_creado': 'var(--secondary-color)',
            'presupuesto_aceptado': 'var(--accent-color)',
            'presupuesto_rechazado': 'var(--danger-color)',
            'obra_iniciada': 'var(--warning-color)',
            'obra_finalizada': 'var(--success-color)',
            'material_stock_bajo': 'var(--danger-color)',
            'pago_realizado': 'var(--success-color)',
            'sistema': 'var(--primary-color)',
            'importante': 'var(--warning-color)',
        }
        return colores.get(self.tipo, 'var(--primary-color)')
    
    def to_dict(self):
        """Convertir notificación a diccionario para JSON"""
        return {
            'id': self.id,
            'tipo': self.tipo,
            'titulo': self.titulo,
            'mensaje': self.mensaje,
            'leida': self.leida,
            'fecha_creacion': self.fecha_creacion.isoformat(),
            'icono': self.get_icono(),
            'color': self.get_color(),
            'url': self.datos_extra.get('url', '#'),
        }

class ConfiguracionNotificacion(models.Model):
    """Configuración de notificaciones por usuario"""
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='configuracion_notificaciones')
    
    # Configuraciones de tipos de notificación
    email_presupuestos = models.BooleanField(default=True)
    email_obras = models.BooleanField(default=True)
    email_sistema = models.BooleanField(default=True)
    email_pagos = models.BooleanField(default=True)
    
    push_presupuestos = models.BooleanField(default=True)
    push_obras = models.BooleanField(default=True)
    push_sistema = models.BooleanField(default=True)
    
    # Configuraciones generales
    notificaciones_activas = models.BooleanField(default=True)
    silenciar_temporalmente = models.BooleanField(default=False)
    silenciar_hasta = models.DateTimeField(null=True, blank=True)
    
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Configuración de Notificación'
        verbose_name_plural = 'Configuraciones de Notificaciones'
    
    def __str__(self):
        return "Configuración de {}".format(self.usuario.username)
    
    def puede_recibir_notificacion(self, tipo_notificacion):
        """Verificar si el usuario puede recibir una notificación del tipo especificado"""
        if not self.notificaciones_activas or self.silenciar_temporalmente:
            return False
        
        if self.silenciar_hasta and timezone.now() < self.silenciar_hasta:
            return False
        
        # Mapear tipo de notificación a configuración
        config_map = {
            'presupuesto_creado': 'email_presupuestos',
            'presupuesto_aceptado': 'email_presupuestos',
            'presupuesto_rechazado': 'email_presupuestos',
            'obra_iniciada': 'email_obras',
            'obra_finalizada': 'email_obras',
            'material_stock_bajo': 'email_sistema',
            'pago_realizado': 'email_pagos',
            'sistema': 'email_sistema',
            'importante': 'email_sistema',
        }
        
        config_field = config_map.get(tipo_notificacion)
        return getattr(self, config_field, True) if config_field else True

# =============================================
# MODELOS DE CHAT EN TIEMPO REAL
# =============================================

class Conversacion(models.Model):
    """Conversación entre usuarios"""
    participantes = models.ManyToManyField(UsuarioPersonalizado, related_name='conversaciones')
    nombre = models.CharField(max_length=200, blank=True)
    es_grupal = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-actualizado_en']
    
    def __str__(self):
        if self.nombre:
            return self.nombre
        return "Chat {}".format(self.id)
    
    def ultimo_mensaje(self):
        return self.mensajes.last()

class Mensaje(models.Model):
    """Mensaje en una conversación"""
    conversacion = models.ForeignKey(Conversacion, on_delete=models.CASCADE, related_name='mensajes')
    remitente = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='mensajes_enviados')
    contenido = models.TextField()
    archivo = models.FileField(upload_to='chat_archivos/', blank=True, null=True)
    imagen = models.ImageField(upload_to='chat_imagenes/', blank=True, null=True)
    leido = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['creado_en']
    
    def __str__(self):
        return "{}: {}".format(self.remitente.username, self.contenido[:50])

class MensajeLeido(models.Model):
    """Registro de mensajes leídos por usuario"""
    mensaje = models.ForeignKey(Mensaje, on_delete=models.CASCADE)
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    leido_en = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['mensaje', 'usuario']

# =============================================
# NUEVOS MODELOS SUPER AVANZADOS PARA PARAGUAY
# =============================================

class Contratista(models.Model):
    """Contratistas especializados para obras civiles en Paraguay"""
    ESPECIALIDADES = [
        ('construccion_civil', '🏗️ Construcción Civil'),
        ('arquitectura', '🏛️ Arquitectura'),
        ('ingenieria_civil', '⚙️ Ingeniería Civil'),
        ('electricidad', '⚡ Instalaciones Eléctricas'),
        ('plomeria', '🚰 Plomería y Sanitarios'),
        ('pintura', '🎨 Pintura y Acabados'),
        ('carpinteria', '🪚 Carpintería'),
        ('albañileria', '🧱 Albañilería'),
        ('techado', '🏠 Techado y Cubiertas'),
        ('paisajismo', '🌳 Paisajismo'),
        ('demolicion', '🔨 Demolición'),
        ('excavacion', '🚜 Excavación y Movimiento de Tierra'),
    ]
    
    ESTADOS = [
        ('disponible', '✅ Disponible'),
        ('ocupado', '🚧 Ocupado'),
        ('vacaciones', '🏖️ En Vacaciones'),
        ('suspendido', '⚠️ Suspendido'),
        ('inactivo', '❌ Inactivo'),
    ]
    
    DEPARTAMENTOS_PARAGUAY = [
        ('asuncion', '🏛️ Asunción'),
        ('central', '🌆 Central'),
        ('alto_parana', '🌊 Alto Paraná'),
        ('itapua', '🌾 Itapúa'),
        ('caaguazu', '🌲 Caaguazú'),
        ('caazapa', '🏞️ Caazapá'),
        ('canindeyú', '🌿 Canindeyú'),
        ('concepcion', '🏔️ Concepción'),
        ('cordillera', '⛰️ Cordillera'),
        ('guaira', '🌄 Guairá'),
        ('paraguari', '🏘️ Paraguarí'),
        ('presidente_hayes', '🐄 Presidente Hayes'),
        ('san_pedro', '🌱 San Pedro'),
        ('amambay', '💎 Amambay'),
        ('boqueron', '🌵 Boquerón'),
        ('alto_paraguay', '🦎 Alto Paraguay'),
        ('misiones', '⛪ Misiones'),
        ('ñeembucu', '🐟 Ñeembucú'),
    ]
    
    # Información básica
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='perfil_contratista')
    nombre_empresa = models.CharField(max_length=200, blank=True, null=True)
    ruc = models.CharField(max_length=20, unique=True, help_text="RUC del contratista")
    especialidad = models.CharField(max_length=30, choices=ESPECIALIDADES)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')
    
    # Ubicación y contacto
    departamento = models.CharField(max_length=30, choices=DEPARTAMENTOS_PARAGUAY)
    ciudad = models.CharField(max_length=100)
    direccion_completa = models.TextField()
    telefono_principal = models.CharField(max_length=20)
    telefono_secundario = models.CharField(max_length=20, blank=True, null=True)
    email_empresa = models.EmailField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    
    # Información profesional
    años_experiencia = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    licencia_profesional = models.CharField(max_length=50, blank=True, null=True)
    registro_profesional = models.CharField(max_length=50, blank=True, null=True)
    
    # Calificaciones y ratings
    calificacion_promedio = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    total_trabajos_completados = models.IntegerField(default=0)
    total_clientes_satisfechos = models.IntegerField(default=0)
    
    # Información financiera
    tarifa_por_hora = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Tarifa en Guaraníes")
    tarifa_por_dia = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Tarifa en Guaraníes")
    tarifa_por_proyecto = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Tarifa en Guaraníes")
    
    # Disponibilidad
    disponible_lunes_viernes = models.BooleanField(default=True)
    disponible_sabados = models.BooleanField(default=True)
    disponible_domingos = models.BooleanField(default=False)
    disponible_feriados = models.BooleanField(default=False)
    
    # Documentos y certificaciones
    cedula_identidad = models.FileField(upload_to='contratistas/documentos/', blank=True, null=True)
    certificado_antecedentes = models.FileField(upload_to='contratistas/documentos/', blank=True, null=True)
    seguro_responsabilidad = models.FileField(upload_to='contratistas/documentos/', blank=True, null=True)
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Contratista'
        verbose_name_plural = 'Contratistas'
        ordering = ['-calificacion_promedio', '-total_trabajos_completados']
        indexes = [
            models.Index(fields=['especialidad', 'departamento']),
            models.Index(fields=['estado', 'activo']),
            models.Index(fields=['calificacion_promedio']),
        ]
    
    def __str__(self):
        return "{} - {}".format(self.usuario.get_full_name() or self.usuario.username, self.get_especialidad_display())
    
    def get_calificacion_estrellas(self):
        """Retorna las estrellas de calificación"""
        estrellas = int(self.calificacion_promedio)
        return '⭐' * estrellas + '☆' * (5 - estrellas)
    
    def esta_disponible(self):
        """Verifica si el contratista está disponible"""
        return self.estado == 'disponible' and self.activo
    
    def calcular_costo_estimado(self, horas=None, dias=None):
        """Calcula el costo estimado según horas o días"""
        if horas and self.tarifa_por_hora:
            return self.tarifa_por_hora * horas
        elif dias and self.tarifa_por_dia:
            return self.tarifa_por_dia * dias
        return self.tarifa_por_proyecto

class Propietario(models.Model):
    """Propietarios de inmuebles y terrenos en Paraguay"""
    TIPOS_PROPIETARIO = [
        ('persona_fisica', '👤 Persona Física'),
        ('persona_juridica', '🏢 Persona Jurídica'),
        ('cooperativa', '🤝 Cooperativa'),
        ('gobierno', '🏛️ Entidad Gubernamental'),
        ('ong', '🌍 ONG'),
    ]
    
    # Información básica
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='perfil_propietario')
    tipo_propietario = models.CharField(max_length=20, choices=TIPOS_PROPIETARIO, default='persona_fisica')
    
    # Datos personales/empresariales
    nombre_completo = models.CharField(max_length=200)
    cedula_ruc = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    nacionalidad = models.CharField(max_length=50, default='Paraguaya')
    
    # Contacto
    telefono_principal = models.CharField(max_length=20)
    telefono_alternativo = models.CharField(max_length=20, blank=True, null=True)
    email_alternativo = models.EmailField(blank=True, null=True)
    
    # Dirección principal
    departamento = models.CharField(max_length=30, choices=Contratista.DEPARTAMENTOS_PARAGUAY)
    ciudad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    direccion_completa = models.TextField()
    codigo_postal = models.CharField(max_length=10, blank=True, null=True)
    
    # Información financiera
    ingresos_mensuales = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Ingresos en Guaraníes")
    patrimonio_estimado = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, help_text="Patrimonio en Guaraníes")
    
    # Preferencias de construcción
    presupuesto_maximo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Presupuesto máximo en Guaraníes")
    tipo_construccion_preferida = models.CharField(max_length=100, blank=True, null=True)
    
    # Documentos
    cedula_identidad = models.FileField(upload_to='propietarios/documentos/', blank=True, null=True)
    comprobante_ingresos = models.FileField(upload_to='propietarios/documentos/', blank=True, null=True)
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Propietario'
        verbose_name_plural = 'Propietarios'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return "{} - {}".format(self.nombre_completo, self.get_tipo_propietario_display())
    
    def get_propiedades_count(self):
        """Cuenta las propiedades del propietario"""
        return self.propiedades.count()
    
    def get_obras_activas_count(self):
        """Cuenta las obras activas del propietario"""
        return Obra.objects.filter(cliente=self.usuario, estado__in=['planificada', 'en_proceso']).count()

class Propiedad(models.Model):
    """Propiedades inmobiliarias de los propietarios"""
    TIPOS_PROPIEDAD = [
        ('casa', '🏠 Casa'),
        ('apartamento', '🏢 Apartamento'),
        ('terreno', '🌾 Terreno'),
        ('local_comercial', '🏪 Local Comercial'),
        ('oficina', '🏢 Oficina'),
        ('deposito', '🏭 Depósito'),
        ('quinta', '🏡 Quinta'),
        ('chacra', '🚜 Chacra'),
        ('estancia', '🐄 Estancia'),
    ]
    
    ESTADOS_PROPIEDAD = [
        ('excelente', '⭐ Excelente'),
        ('muy_bueno', '👍 Muy Bueno'),
        ('bueno', '✅ Bueno'),
        ('regular', '⚠️ Regular'),
        ('malo', '❌ Malo'),
        ('en_construccion', '🚧 En Construcción'),
        ('abandonado', '🏚️ Abandonado'),
    ]
    
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE, related_name='propiedades')
    tipo_propiedad = models.CharField(max_length=20, choices=TIPOS_PROPIEDAD)
    nombre_propiedad = models.CharField(max_length=200)
    
    # Ubicación
    departamento = models.CharField(max_length=30, choices=Contratista.DEPARTAMENTOS_PARAGUAY)
    ciudad = models.CharField(max_length=100)
    barrio = models.CharField(max_length=100, blank=True, null=True)
    direccion_completa = models.TextField()
    
    # Características
    superficie_total = models.DecimalField(max_digits=10, decimal_places=2, help_text="Superficie en m²")
    superficie_construida = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Superficie construida en m²")
    habitaciones = models.IntegerField(blank=True, null=True)
    baños = models.IntegerField(blank=True, null=True)
    cocheras = models.IntegerField(default=0)
    
    # Estado y valuación
    estado_propiedad = models.CharField(max_length=20, choices=ESTADOS_PROPIEDAD, default='bueno')
    valor_fiscal = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Valor fiscal en Guaraníes")
    valor_comercial = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Valor comercial en Guaraníes")
    
    # Servicios
    tiene_agua_corriente = models.BooleanField(default=True)
    tiene_energia_electrica = models.BooleanField(default=True)
    tiene_cloacas = models.BooleanField(default=False)
    tiene_gas = models.BooleanField(default=False)
    tiene_internet = models.BooleanField(default=False)
    
    # Documentos
    titulo_propiedad = models.FileField(upload_to='propiedades/documentos/', blank=True, null=True)
    plano_catastral = models.FileField(upload_to='propiedades/documentos/', blank=True, null=True)
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activa = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        ordering = ['-fecha_registro']
    
    def __str__(self):
        return "{} - {}".format(self.nombre_propiedad, self.propietario.nombre_completo)
    
    def get_obras_realizadas(self):
        """Obtiene las obras realizadas en esta propiedad"""
        return Obra.objects.filter(
            cliente=self.propietario.usuario,
            ubicacion__icontains=self.direccion_completa
        )

class Empleado(models.Model):
    """Empleados de la empresa constructora"""
    CARGOS = [
        ('gerente_general', '👔 Gerente General'),
        ('gerente_obras', '🏗️ Gerente de Obras'),
        ('ingeniero_civil', '⚙️ Ingeniero Civil'),
        ('arquitecto', '🏛️ Arquitecto'),
        ('maestro_obras', '👷 Maestro de Obras'),
        ('capataz', '🔨 Capataz'),
        ('albañil', '🧱 Albañil'),
        ('electricista', '⚡ Electricista'),
        ('plomero', '🚰 Plomero'),
        ('pintor', '🎨 Pintor'),
        ('carpintero', '🪚 Carpintero'),
        ('soldador', '🔥 Soldador'),
        ('operador_maquinaria', '🚜 Operador de Maquinaria'),
        ('ayudante', '🤝 Ayudante'),
        ('administrativo', '📋 Administrativo'),
        ('contador', '💰 Contador'),
        ('vendedor', '💼 Vendedor'),
        ('seguridad', '🛡️ Seguridad'),
        ('limpieza', '🧹 Limpieza'),
    ]
    
    ESTADOS_EMPLEADO = [
        ('activo', '✅ Activo'),
        ('vacaciones', '🏖️ En Vacaciones'),
        ('licencia_medica', '🏥 Licencia Médica'),
        ('licencia_personal', '👤 Licencia Personal'),
        ('suspendido', '⚠️ Suspendido'),
        ('despedido', '❌ Despedido'),
        ('renunciado', '👋 Renunciado'),
    ]
    
    TURNOS = [
        ('mañana', '🌅 Mañana (06:00-14:00)'),
        ('tarde', '🌇 Tarde (14:00-22:00)'),
        ('noche', '🌙 Noche (22:00-06:00)'),
        ('completo', '⏰ Tiempo Completo (08:00-17:00)'),
        ('medio_tiempo', '⏳ Medio Tiempo'),
        ('por_horas', '🕐 Por Horas'),
    ]
    
    # Información básica
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='perfil_empleado')
    codigo_empleado = models.CharField(max_length=20, unique=True)
    cargo = models.CharField(max_length=30, choices=CARGOS)
    estado = models.CharField(max_length=20, choices=ESTADOS_EMPLEADO, default='activo')
    
    # Información personal
    cedula_identidad = models.CharField(max_length=20, unique=True)
    fecha_nacimiento = models.DateField()
    lugar_nacimiento = models.CharField(max_length=100)
    estado_civil = models.CharField(max_length=20, choices=[
        ('soltero', 'Soltero/a'),
        ('casado', 'Casado/a'),
        ('divorciado', 'Divorciado/a'),
        ('viudo', 'Viudo/a'),
        ('union_libre', 'Unión Libre'),
    ], default='soltero')
    
    # Contacto
    telefono_principal = models.CharField(max_length=20)
    telefono_emergencia = models.CharField(max_length=20)
    contacto_emergencia = models.CharField(max_length=200, help_text="Nombre del contacto de emergencia")
    
    # Dirección
    departamento = models.CharField(max_length=30, choices=Contratista.DEPARTAMENTOS_PARAGUAY)
    ciudad = models.CharField(max_length=100)
    direccion_completa = models.TextField()
    
    # Información laboral
    fecha_ingreso = models.DateField()
    fecha_salida = models.DateField(blank=True, null=True)
    turno = models.CharField(max_length=20, choices=TURNOS, default='completo')
    salario_base = models.DecimalField(max_digits=10, decimal_places=2, help_text="Salario base en Guaraníes")
    bonificaciones = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Bonificaciones en Guaraníes")
    
    # Capacitación y experiencia
    nivel_educacion = models.CharField(max_length=100, blank=True, null=True)
    certificaciones = models.TextField(blank=True, null=True, help_text="Certificaciones y cursos")
    años_experiencia = models.IntegerField(default=0)
    
    # Evaluación de desempeño
    calificacion_desempeño = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    observaciones = models.TextField(blank=True, null=True)
    
    # Documentos
    foto_empleado = models.ImageField(upload_to='empleados/fotos/', blank=True, null=True)
    cv_empleado = models.FileField(upload_to='empleados/documentos/', blank=True, null=True)
    certificado_antecedentes = models.FileField(upload_to='empleados/documentos/', blank=True, null=True)
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Empleado'
        verbose_name_plural = 'Empleados'
        ordering = ['-fecha_ingreso']
        indexes = [
            models.Index(fields=['cargo', 'estado']),
            models.Index(fields=['fecha_ingreso']),
        ]
    
    def __str__(self):
        return "{} - {}".format(self.usuario.get_full_name() or self.usuario.username, self.get_cargo_display())
    
    def get_antiguedad_años(self):
        """Calcula los años de antigüedad"""
        from datetime import date
        if self.fecha_salida:
            return (self.fecha_salida - self.fecha_ingreso).days // 365
        return (date.today() - self.fecha_ingreso).days // 365
    
    def get_salario_total(self):
        """Calcula el salario total incluyendo bonificaciones"""
        return self.salario_base + self.bonificaciones
    
    def esta_activo(self):
        """Verifica si el empleado está activo"""
        return self.estado == 'activo' and self.activo

class Proveedor(models.Model):
    """Proveedores de materiales y servicios"""
    TIPOS_PROVEEDOR = [
        ('materiales_construccion', '🧱 Materiales de Construcción'),
        ('herramientas', '🛠️ Herramientas'),
        ('maquinaria', '🚜 Maquinaria'),
        ('servicios_especializados', '⚙️ Servicios Especializados'),
        ('transporte', '🚚 Transporte'),
        ('equipos_seguridad', '🦺 Equipos de Seguridad'),
        ('pinturas_acabados', '🎨 Pinturas y Acabados'),
        ('electricidad', '⚡ Materiales Eléctricos'),
        ('plomeria', '🚰 Plomería y Sanitarios'),
        ('ferreteria', '🔧 Ferretería General'),
        ('maderas', '🪵 Maderas'),
        ('metales', '⚒️ Metales y Soldadura'),
        ('vidrios', '🪟 Vidrios y Cristales'),
        ('ceramicas', '🏺 Cerámicas y Revestimientos'),
    ]
    
    ESTADOS_PROVEEDOR = [
        ('activo', '✅ Activo'),
        ('inactivo', '❌ Inactivo'),
        ('suspendido', '⚠️ Suspendido'),
        ('evaluacion', '🔍 En Evaluación'),
        ('preferido', '⭐ Proveedor Preferido'),
    ]
    
    # Información básica
    nombre_empresa = models.CharField(max_length=200)
    ruc = models.CharField(max_length=20, unique=True)
    tipo_proveedor = models.CharField(max_length=30, choices=TIPOS_PROVEEDOR)
    estado = models.CharField(max_length=20, choices=ESTADOS_PROVEEDOR, default='activo')
    
    # Contacto principal
    persona_contacto = models.CharField(max_length=200)
    cargo_contacto = models.CharField(max_length=100, blank=True, null=True)
    telefono_principal = models.CharField(max_length=20)
    telefono_secundario = models.CharField(max_length=20, blank=True, null=True)
    email_principal = models.EmailField()
    email_secundario = models.EmailField(blank=True, null=True)
    sitio_web = models.URLField(blank=True, null=True)
    
    # Ubicación
    departamento = models.CharField(max_length=30, choices=Contratista.DEPARTAMENTOS_PARAGUAY)
    ciudad = models.CharField(max_length=100)
    direccion_completa = models.TextField()
    
    # Información comercial
    años_mercado = models.IntegerField(default=0, help_text="Años en el mercado")
    capacidad_suministro = models.CharField(max_length=200, blank=True, null=True, help_text="Descripción de capacidad")
    tiempo_entrega_promedio = models.IntegerField(default=0, help_text="Días promedio de entrega")
    
    # Condiciones comerciales
    forma_pago_preferida = models.CharField(max_length=100, blank=True, null=True)
    descuento_volumen = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Descuento por volumen (%)")
    credito_maximo = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Crédito máximo en Guaraníes")
    
    # Evaluación y calificación
    calificacion_calidad = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    calificacion_precio = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    calificacion_entrega = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    calificacion_servicio = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(Decimal('0'))])
    
    # Certificaciones y documentos
    certificaciones = models.TextField(blank=True, null=True, help_text="Certificaciones de calidad")
    licencias = models.TextField(blank=True, null=True, help_text="Licencias y permisos")
    
    # Documentos
    logo_empresa = models.ImageField(upload_to='proveedores/logos/', blank=True, null=True)
    catalogo_productos = models.FileField(upload_to='proveedores/catalogos/', blank=True, null=True)
    certificado_calidad = models.FileField(upload_to='proveedores/documentos/', blank=True, null=True)
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-calificacion_calidad', 'nombre_empresa']
        indexes = [
            models.Index(fields=['tipo_proveedor', 'estado']),
            models.Index(fields=['departamento', 'ciudad']),
        ]
    
    def __str__(self):
        return "{} - {}".format(self.nombre_empresa, self.get_tipo_proveedor_display())
    
    def get_calificacion_promedio(self):
        """Calcula la calificación promedio general"""
        total = self.calificacion_calidad + self.calificacion_precio + self.calificacion_entrega + self.calificacion_servicio
        return total / 4 if total > 0 else 0
    
    def get_calificacion_estrellas(self):
        """Retorna las estrellas de calificación promedio"""
        promedio = self.get_calificacion_promedio()
        estrellas = int(promedio)
        return '⭐' * estrellas + '☆' * (5 - estrellas)
    
    def esta_activo(self):
        """Verifica si el proveedor está activo"""
        return self.estado == 'activo' and self.activo

class ProductoProveedor(models.Model):
    """Productos ofrecidos por proveedores"""
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='productos')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='proveedores', blank=True, null=True)
    
    # Información del producto
    nombre_producto = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    codigo_producto = models.CharField(max_length=50, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    modelo = models.CharField(max_length=100, blank=True, null=True)
    
    # Precios y disponibilidad
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, help_text="Precio en Guaraníes")
    precio_mayorista = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Precio mayorista en Guaraníes")
    stock_disponible = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=0)
    
    # Especificaciones
    unidad_medida = models.CharField(max_length=20, default='unidad')
    peso = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, help_text="Peso en kg")
    dimensiones = models.CharField(max_length=200, blank=True, null=True)
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Producto de Proveedor'
        verbose_name_plural = 'Productos de Proveedores'
        ordering = ['nombre_producto']
        unique_together = ['proveedor', 'codigo_producto']
    
    def __str__(self):
        return "{} - {}".format(self.nombre_producto, self.proveedor.nombre_empresa)
    
    def get_precio_con_descuento(self, cantidad=1):
        """Calcula el precio con descuento por volumen"""
        precio_base = self.precio_mayorista if cantidad >= 10 and self.precio_mayorista else self.precio_unitario
        descuento = self.proveedor.descuento_volumen / 100 if cantidad >= 50 else 0
        return precio_base * (1 - descuento)

class EvaluacionProveedor(models.Model):
    """Evaluaciones de proveedores por parte de la empresa"""
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='evaluaciones')
    evaluador = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, blank=True, null=True)
    
    # Calificaciones específicas
    calidad_productos = models.IntegerField(choices=[(i, f'{i} ⭐') for i in range(1, 6)])
    puntualidad_entrega = models.IntegerField(choices=[(i, f'{i} ⭐') for i in range(1, 6)])
    precio_competitivo = models.IntegerField(choices=[(i, f'{i} ⭐') for i in range(1, 6)])
    atencion_cliente = models.IntegerField(choices=[(i, f'{i} ⭐') for i in range(1, 6)])
    
    # Comentarios
    comentarios = models.TextField(blank=True, null=True)
    recomendaria = models.BooleanField(default=True)
    
    # Metadatos
    fecha_evaluacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Evaluación de Proveedor'
        verbose_name_plural = 'Evaluaciones de Proveedores'
        ordering = ['-fecha_evaluacion']
        unique_together = ['proveedor', 'evaluador', 'obra']
    
    def __str__(self):
        return "Evaluación de {} - {}".format(self.proveedor.nombre_empresa, self.fecha_evaluacion.strftime('%d/%m/%Y'))
    
    def get_calificacion_promedio(self):
        """Calcula la calificación promedio de esta evaluación"""
        return (self.calidad_productos + self.puntualidad_entrega + self.precio_competitivo + self.atencion_cliente) / 4

class ContratoContratista(models.Model):
    """Contratos con contratistas para obras específicas"""
    ESTADOS_CONTRATO = [
        ('borrador', '📝 Borrador'),
        ('enviado', '📤 Enviado'),
        ('negociacion', '🤝 En Negociación'),
        ('firmado', '✅ Firmado'),
        ('en_ejecucion', '🚧 En Ejecución'),
        ('completado', '🎉 Completado'),
        ('cancelado', '❌ Cancelado'),
        ('suspendido', '⏸️ Suspendido'),
    ]
    
    # Partes del contrato
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, related_name='contratos')
    contratista = models.ForeignKey(Contratista, on_delete=models.CASCADE, related_name='contratos')
    creado_por = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    
    # Información del contrato
    numero_contrato = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CONTRATO, default='borrador')
    
    # Fechas importantes
    fecha_inicio_prevista = models.DateField()
    fecha_fin_prevista = models.DateField()
    fecha_firma = models.DateTimeField(blank=True, null=True)
    fecha_inicio_real = models.DateField(blank=True, null=True)
    fecha_fin_real = models.DateField(blank=True, null=True)
    
    # Términos financieros
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, help_text="Monto total en Guaraníes")
    anticipo_porcentaje = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    anticipo_monto = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Términos y condiciones
    descripcion_trabajo = models.TextField()
    materiales_incluidos = models.BooleanField(default=False)
    mano_obra_incluida = models.BooleanField(default=True)
    garantia_meses = models.IntegerField(default=12)
    
    # Penalizaciones y bonificaciones
    penalizacion_retraso = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Penalización por día de retraso")
    bonificacion_adelanto = models.DecimalField(max_digits=10, decimal_places=2, default=0, help_text="Bonificación por adelanto")
    
    # Documentos
    contrato_firmado = models.FileField(upload_to='contratos/', blank=True, null=True)
    anexos = models.FileField(upload_to='contratos/anexos/', blank=True, null=True)
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Contrato de Contratista'
        verbose_name_plural = 'Contratos de Contratistas'
        ordering = ['-fecha_creacion']
    
    def __str__(self):
        return "Contrato {} - {}".format(self.numero_contrato, self.obra.nombre)
    
    def get_duracion_dias(self):
        """Calcula la duración del contrato en días"""
        return (self.fecha_fin_prevista - self.fecha_inicio_prevista).days
    
    def get_progreso_porcentaje(self):
        """Calcula el progreso del contrato"""
        if self.estado == 'completado':
            return 100
        elif self.estado == 'en_ejecucion':
            if self.fecha_inicio_real:
                from datetime import date
                dias_transcurridos = (date.today() - self.fecha_inicio_real).days
                duracion_total = self.get_duracion_dias()
                return min(int((dias_transcurridos / duracion_total) * 100), 100) if duracion_total > 0 else 0
        return 0

# =============================================
# MODELOS PARA REPOSITORIOS GITHUB
# =============================================

class RepositorioGitHub(models.Model):
    """Repositorios de GitHub para mostrar trabajos y proyectos"""
    TIPOS_PROYECTO = [
        ('web_app', '🌐 Aplicación Web'),
        ('mobile_app', '📱 Aplicación Móvil'),
        ('desktop_app', '💻 Aplicación de Escritorio'),
        ('api_backend', '⚙️ API/Backend'),
        ('frontend', '🎨 Frontend'),
        ('fullstack', '🔄 Full Stack'),
        ('machine_learning', '🤖 Machine Learning'),
        ('data_science', '📊 Data Science'),
        ('game', '🎮 Juego'),
        ('library', '📚 Librería/Framework'),
        ('tool', '🛠️ Herramienta'),
        ('script', '📜 Script/Automatización'),
        ('website', '🌍 Sitio Web'),
        ('portfolio', '💼 Portfolio'),
        ('educational', '🎓 Educativo'),
        ('experimental', '🧪 Experimental'),
        ('construction', '🏗️ Construcción/Obras'),
        ('business', '💼 Empresarial'),
        ('ecommerce', '🛒 E-commerce'),
        ('cms', '📝 CMS'),
    ]
    
    ESTADOS_PROYECTO = [
        ('activo', '✅ Activo'),
        ('en_desarrollo', '🚧 En Desarrollo'),
        ('completado', '🎉 Completado'),
        ('mantenimiento', '🔧 En Mantenimiento'),
        ('archivado', '📦 Archivado'),
        ('pausado', '⏸️ Pausado'),
        ('descontinuado', '❌ Descontinuado'),
    ]
    
    TECNOLOGIAS_PRINCIPALES = [
        ('python', '🐍 Python'),
        ('django', '🎯 Django'),
        ('javascript', '💛 JavaScript'),
        ('react', '⚛️ React'),
        ('vue', '💚 Vue.js'),
        ('angular', '🔴 Angular'),
        ('nodejs', '💚 Node.js'),
        ('php', '🐘 PHP'),
        ('laravel', '🔴 Laravel'),
        ('java', '☕ Java'),
        ('spring', '🍃 Spring'),
        ('csharp', '💙 C#'),
        ('dotnet', '🔵 .NET'),
        ('flutter', '💙 Flutter'),
        ('react_native', '📱 React Native'),
        ('swift', '🍎 Swift'),
        ('kotlin', '🟠 Kotlin'),
        ('go', '🔵 Go'),
        ('rust', '🦀 Rust'),
        ('typescript', '💙 TypeScript'),
        ('html_css', '🎨 HTML/CSS'),
        ('bootstrap', '🟣 Bootstrap'),
        ('tailwind', '💨 Tailwind CSS'),
        ('mysql', '🐬 MySQL'),
        ('postgresql', '🐘 PostgreSQL'),
        ('mongodb', '🍃 MongoDB'),
        ('redis', '🔴 Redis'),
        ('docker', '🐳 Docker'),
        ('kubernetes', '☸️ Kubernetes'),
        ('aws', '☁️ AWS'),
        ('firebase', '🔥 Firebase'),
        ('other', '🔧 Otro'),
    ]
    
    # Información básica del repositorio
    nombre = models.CharField(max_length=200, help_text="Nombre del repositorio")
    descripcion = models.TextField(help_text="Descripción detallada del proyecto")
    url_repositorio = models.URLField(help_text="URL del repositorio en GitHub")
    url_demo = models.URLField(blank=True, null=True, help_text="URL de demo en vivo")
    url_documentacion = models.URLField(blank=True, null=True, help_text="URL de documentación")
    
    # Clasificación del proyecto
    tipo_proyecto = models.CharField(max_length=30, choices=TIPOS_PROYECTO, default='web_app')
    tecnologia_principal = models.CharField(max_length=30, choices=TECNOLOGIAS_PRINCIPALES, default='python')
    tecnologias_adicionales = models.JSONField(default=list, blank=True, help_text="Lista de tecnologías adicionales")
    
    # Estado y progreso
    estado = models.CharField(max_length=20, choices=ESTADOS_PROYECTO, default='activo')
    progreso_porcentaje = models.IntegerField(default=0, validators=[MinValueValidator(0)], help_text="Progreso del proyecto (0-100)")
    
    # Información del repositorio GitHub
    github_id = models.CharField(max_length=50, blank=True, null=True, help_text="ID del repositorio en GitHub")
    estrellas = models.IntegerField(default=0, help_text="Número de estrellas en GitHub")
    forks = models.IntegerField(default=0, help_text="Número de forks")
    watchers = models.IntegerField(default=0, help_text="Número de watchers")
    issues_abiertas = models.IntegerField(default=0, help_text="Issues abiertas")
    lenguaje_principal = models.CharField(max_length=50, blank=True, null=True)
    tamaño_kb = models.IntegerField(default=0, help_text="Tamaño del repositorio en KB")
    
    # Fechas importantes
    fecha_creacion_github = models.DateTimeField(blank=True, null=True)
    fecha_ultimo_commit = models.DateTimeField(blank=True, null=True)
    fecha_ultimo_release = models.DateTimeField(blank=True, null=True)
    
    # Información adicional
    es_privado = models.BooleanField(default=False)
    es_fork = models.BooleanField(default=False)
    tiene_wiki = models.BooleanField(default=False)
    tiene_pages = models.BooleanField(default=False)
    licencia = models.CharField(max_length=100, blank=True, null=True)
    
    # Características del proyecto
    es_destacado = models.BooleanField(default=False, help_text="Marcar como proyecto destacado")
    es_comercial = models.BooleanField(default=False, help_text="Proyecto comercial/empresarial")
    es_open_source = models.BooleanField(default=True, help_text="Proyecto de código abierto")
    
    # Métricas y evaluación
    dificultad = models.IntegerField(choices=[
        (1, '⭐ Básico'),
        (2, '⭐⭐ Intermedio'),
        (3, '⭐⭐⭐ Avanzado'),
        (4, '⭐⭐⭐⭐ Experto'),
        (5, '⭐⭐⭐⭐⭐ Maestro'),
    ], default=2)
    
    calidad_codigo = models.IntegerField(choices=[
        (1, '⭐ Básica'),
        (2, '⭐⭐ Buena'),
        (3, '⭐⭐⭐ Muy Buena'),
        (4, '⭐⭐⭐⭐ Excelente'),
        (5, '⭐⭐⭐⭐⭐ Excepcional'),
    ], default=3)
    
    # Imágenes y multimedia
    imagen_preview = models.ImageField(upload_to='repositorios/previews/', blank=True, null=True, help_text="Imagen de vista previa")
    capturas_pantalla = models.JSONField(default=list, blank=True, help_text="URLs de capturas de pantalla")
    video_demo = models.URLField(blank=True, null=True, help_text="URL de video demo")
    
    # Información del desarrollador
    desarrollador = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE, related_name='repositorios')
    colaboradores = models.ManyToManyField(UsuarioPersonalizado, blank=True, related_name='repositorios_colaborados')
    
    # Información empresarial (para proyectos de L.u.M.a)
    cliente_proyecto = models.CharField(max_length=200, blank=True, null=True, help_text="Cliente para quien se desarrolló")
    costo_desarrollo = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Costo de desarrollo en Guaraníes")
    tiempo_desarrollo_horas = models.IntegerField(blank=True, null=True, help_text="Tiempo de desarrollo en horas")
    
    # Metadatos
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    fecha_actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    sincronizado_github = models.BooleanField(default=False)
    ultima_sincronizacion = models.DateTimeField(blank=True, null=True)
    
    # Estadísticas de visualización
    vistas = models.IntegerField(default=0)
    descargas = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Repositorio GitHub'
        verbose_name_plural = 'Repositorios GitHub'
        ordering = ['-es_destacado', '-fecha_ultimo_commit', '-estrellas']
        indexes = [
            models.Index(fields=['tipo_proyecto', 'tecnologia_principal']),
            models.Index(fields=['estado', 'es_destacado']),
            models.Index(fields=['desarrollador', 'activo']),
        ]
    
    def __str__(self):
        return f"{self.nombre} - {self.get_tipo_proyecto_display()}"
    
    def get_url_github_api(self):
        """Obtiene la URL de la API de GitHub para este repositorio"""
        if '/github.com/' in self.url_repositorio:
            parts = self.url_repositorio.replace('https://github.com/', '').split('/')
            if len(parts) >= 2:
                return f"https://api.github.com/repos/{parts[0]}/{parts[1]}"
        return None
    
    def get_tecnologias_display(self):
        """Retorna las tecnologías como lista legible"""
        tecnologias = [self.get_tecnologia_principal_display()]
        if self.tecnologias_adicionales:
            for tech in self.tecnologias_adicionales:
                tech_display = dict(self.TECNOLOGIAS_PRINCIPALES).get(tech, tech)
                if tech_display not in tecnologias:
                    tecnologias.append(tech_display)
        return tecnologias
    
    def get_color_estado(self):
        """Retorna el color CSS según el estado"""
        colores = {
            'activo': '#28a745',
            'en_desarrollo': '#ffc107',
            'completado': '#17a2b8',
            'mantenimiento': '#fd7e14',
            'archivado': '#6c757d',
            'pausado': '#dc3545',
            'descontinuado': '#343a40',
        }
        return colores.get(self.estado, '#6c757d')
    
    def get_icono_tipo(self):
        """Retorna el icono según el tipo de proyecto"""
        iconos = {
            'web_app': '🌐',
            'mobile_app': '📱',
            'desktop_app': '💻',
            'api_backend': '⚙️',
            'frontend': '🎨',
            'fullstack': '🔄',
            'machine_learning': '🤖',
            'data_science': '📊',
            'game': '🎮',
            'library': '📚',
            'tool': '🛠️',
            'script': '📜',
            'website': '🌍',
            'portfolio': '💼',
            'educational': '🎓',
            'experimental': '🧪',
            'construction': '🏗️',
            'business': '💼',
            'ecommerce': '🛒',
            'cms': '📝',
        }
        return iconos.get(self.tipo_proyecto, '📁')
    
    def incrementar_vistas(self):
        """Incrementa el contador de vistas"""
        self.vistas += 1
        self.save(update_fields=['vistas'])
    
    def get_popularidad_score(self):
        """Calcula un score de popularidad basado en métricas"""
        score = 0
        score += self.estrellas * 10
        score += self.forks * 5
        score += self.watchers * 2
        score += self.vistas
        if self.es_destacado:
            score += 100
        if self.url_demo:
            score += 50
        return score
    
    def esta_actualizado(self):
        """Verifica si el repositorio está actualizado (último commit < 30 días)"""
        if self.fecha_ultimo_commit:
            from datetime import timedelta
            return (timezone.now() - self.fecha_ultimo_commit).days <= 30
        return False

class TagRepositorio(models.Model):
    """Tags/etiquetas para categorizar repositorios"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#007bff', help_text="Color hexadecimal para el tag")
    icono = models.CharField(max_length=50, blank=True, null=True, help_text="Clase de icono (ej: fas fa-code)")
    
    # Metadatos
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Tag de Repositorio'
        verbose_name_plural = 'Tags de Repositorios'
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre
    
    def get_repositorios_count(self):
        """Cuenta los repositorios que usan este tag"""
        return self.repositorios.filter(activo=True).count()

# Relación many-to-many entre repositorios y tags
RepositorioGitHub.add_to_class('tags', models.ManyToManyField(TagRepositorio, blank=True, related_name='repositorios'))

class ComentarioRepositorio(models.Model):
    """Comentarios y reseñas de repositorios"""
    repositorio = models.ForeignKey(RepositorioGitHub, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(UsuarioPersonalizado, on_delete=models.CASCADE)
    
    # Contenido del comentario
    comentario = models.TextField()
    calificacion = models.IntegerField(choices=[
        (1, '⭐ 1 Estrella'),
        (2, '⭐⭐ 2 Estrellas'),
        (3, '⭐⭐⭐ 3 Estrellas'),
        (4, '⭐⭐⭐⭐ 4 Estrellas'),
        (5, '⭐⭐⭐⭐⭐ 5 Estrellas'),
    ], blank=True, null=True)
    
    # Metadatos
    fecha_comentario = models.DateTimeField(auto_now_add=True)
    fecha_actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Comentario de Repositorio'
        verbose_name_plural = 'Comentarios de Repositorios'
        ordering = ['-fecha_comentario']
        unique_together = ['repositorio', 'usuario']
    
    def __str__(self):
        return f"Comentario de {self.usuario.username} en {self.repositorio.nombre}"

class EstadisticaRepositorio(models.Model):
    """Estadísticas históricas de repositorios"""
    repositorio = models.ForeignKey(RepositorioGitHub, on_delete=models.CASCADE, related_name='estadisticas')
    
    # Métricas del día
    fecha = models.DateField()
    estrellas = models.IntegerField(default=0)
    forks = models.IntegerField(default=0)
    watchers = models.IntegerField(default=0)
    issues_abiertas = models.IntegerField(default=0)
    commits_dia = models.IntegerField(default=0)
    vistas_dia = models.IntegerField(default=0)
    
    # Metadatos
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Estadística de Repositorio'
        verbose_name_plural = 'Estadísticas de Repositorios'
        ordering = ['-fecha']
        unique_together = ['repositorio', 'fecha']
    
    def __str__(self):
        return f"Stats {self.repositorio.nombre} - {self.fecha}"