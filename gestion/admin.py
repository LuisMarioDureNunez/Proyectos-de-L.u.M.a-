from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import (
    UsuarioPersonalizado, Tienda, Categoria, Producto, Material, 
    Maquinaria, Herramienta, Obra, Presupuesto, ItemPresupuesto,
    Carrito, ItemCarrito, Pedido, ItemPedido, Notificacion,
    Contratista, Propietario, Propiedad, Empleado, Proveedor, 
    ProductoProveedor, EvaluacionProveedor, ContratoContratista
)

# Personalizar el sitio de administración
admin.site.site_header = "🇵🇾 SISTEMA GESTIÓN PARAGUAY - Administración"
admin.site.site_title = "Admin LUMAPY"
admin.site.index_title = "Panel de Administración Profesional"

# ===== USUARIO PERSONALIZADO =====
@admin.register(UsuarioPersonalizado)
class UsuarioPersonalizadoAdmin(UserAdmin):
    list_display = ('username', 'email', 'nombre_completo', 'rol_badge', 'telefono', 'is_staff', 'is_active', 'fecha_registro')
    list_filter = ('rol', 'is_staff', 'is_active', 'is_superuser', 'fecha_registro')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'telefono')
    ordering = ('-fecha_registro',)
    list_per_page = 20
    date_hierarchy = 'fecha_registro'
    
    fieldsets = UserAdmin.fieldsets + (
        ('🇵🇾 Información Paraguay', {
            'fields': ('rol', 'telefono', 'direccion', 'avatar', 'tienda', 'es_activo'),
            'classes': ('wide',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('🇵🇾 Información Paraguay', {
            'fields': ('rol', 'telefono', 'email', 'es_activo'),
            'classes': ('wide',)
        }),
    )
    
    def nombre_completo(self, obj):
        return obj.get_full_name() or obj.username
    nombre_completo.short_description = 'Nombre Completo'
    
    def rol_badge(self, obj):
        colors = {
            'admin': '#dc3545',
            'vendedor': '#28a745',
            'cliente': '#007bff',
            'constructor': '#ffc107'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 12px; border-radius: 15px; font-weight: bold;">{}</span>',
            colors.get(obj.rol, '#6c757d'),
            obj.get_rol_display()
        )
    rol_badge.short_description = 'Rol'

# ===== MATERIALES =====
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_guaranies', 'stock_badge', 'unidad_medida', 'creado_por', 'activo', 'fecha_creacion')
    list_filter = ('unidad_medida', 'activo', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_editable = ('activo',)
    list_per_page = 25
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'unidad_medida')
        }),
        ('💰 Precio y Stock', {
            'fields': ('precio', 'stock', 'activo'),
            'classes': ('wide',)
        }),
        ('Auditoría', {
            'fields': ('creado_por',),
            'classes': ('collapse',)
        }),
    )
    
    def precio_guaranies(self, obj):
        return format_html(
            '<strong style="color: #d52b1e;">₲ {}</strong>',
            '{:,.0f}'.format(float(obj.precio))
        )
    precio_guaranies.short_description = '💰 Precio (Gs.)'
    
    def stock_badge(self, obj):
        if obj.stock == 0:
            color = '#dc3545'
            icon = '❌'
        elif obj.stock < 10:
            color = '#ffc107'
            icon = '⚠️'
        else:
            color = '#28a745'
            icon = '✅'
        return format_html(
            '<span style="color: {}; font-weight: bold;">{} {}</span>',
            color, icon, obj.stock
        )
    stock_badge.short_description = '📦 Stock'

# ===== MAQUINARIAS =====
@admin.register(Maquinaria)
class MaquinariaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'modelo', 'marca', 'estado_badge', 'costo_alquiler_guaranies', 'creado_por', 'fecha_creacion')
    list_filter = ('estado', 'marca', 'fecha_creacion')
    search_fields = ('nombre', 'modelo', 'marca', 'descripcion')
    list_per_page = 20
    date_hierarchy = 'fecha_creacion'
    
    def estado_badge(self, obj):
        colors = {
            'disponible': '#28a745',
            'mantenimiento': '#ffc107',
            'alquilada': '#007bff',
            'reparacion': '#dc3545'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.estado, '#6c757d'),
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def costo_alquiler_guaranies(self, obj):
        return format_html(
            '<strong style="color: #0038a8;">₲ {}/día</strong>',
            '{:,.0f}'.format(float(obj.costo_alquiler_dia))
        )
    costo_alquiler_guaranies.short_description = '💵 Costo Alquiler'

# ===== HERRAMIENTAS =====
@admin.register(Herramienta)
class HerramientaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado_badge', 'disponibilidad', 'creado_por', 'fecha_creacion')
    list_filter = ('estado', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion')
    list_per_page = 25
    
    def estado_badge(self, obj):
        colors = {
            'disponible': '#28a745',
            'mantenimiento': '#ffc107',
            'en_uso': '#007bff',
            'perdida': '#dc3545'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.estado, '#6c757d'),
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def disponibilidad(self, obj):
        return format_html(
            '<strong>{}/{}</strong> disponibles',
            obj.cantidad_disponible,
            obj.cantidad_total
        )
    disponibilidad.short_description = '🛠️ Disponibilidad'

# ===== OBRAS =====
@admin.register(Obra)
class ObraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cliente', 'constructor', 'estado_badge', 'ubicacion', 'presupuesto_guaranies', 'costo_real_guaranies', 'progreso', 'fecha_inicio')
    list_filter = ('estado', 'fecha_inicio', 'fecha_creacion')
    search_fields = ('nombre', 'ubicacion', 'descripcion', 'cliente__username')
    list_per_page = 20
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información General', {
            'fields': ('nombre', 'descripcion', 'ubicacion')
        }),
        ('👥 Participantes', {
            'fields': ('cliente', 'constructor', 'creado_por')
        }),
        ('📅 Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin_estimada', 'fecha_fin_real')
        }),
        ('💰 Financiero', {
            'fields': ('presupuesto_asignado', 'costo_real', 'estado'),
            'classes': ('wide',)
        }),
    )
    
    def estado_badge(self, obj):
        colors = {
            'planificada': '#007bff',
            'en_proceso': '#ffc107',
            'suspendida': '#6c757d',
            'finalizada': '#28a745',
            'cancelada': '#dc3545'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 10px; font-weight: bold;">{}</span>',
            colors.get(obj.estado, '#6c757d'),
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def presupuesto_guaranies(self, obj):
        return format_html(
            '<strong style="color: #28a745;">₲ {}</strong>',
            '{:,.0f}'.format(float(obj.presupuesto_asignado))
        )
    presupuesto_guaranies.short_description = '💰 Presupuesto'
    
    def costo_real_guaranies(self, obj):
        return format_html(
            '<strong style="color: #dc3545;">₲ {}</strong>',
            '{:,.0f}'.format(float(obj.costo_real))
        )
    costo_real_guaranies.short_description = '💸 Costo Real'
    
    def progreso(self, obj):
        porcentaje = obj.progreso_porcentaje()
        if porcentaje >= 75:
            color = '#28a745'
        elif porcentaje >= 50:
            color = '#ffc107'
        else:
            color = '#007bff'
        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 10px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; color: white; text-align: center; padding: 2px; font-size: 11px; font-weight: bold;">{}%</div>'
            '</div>',
            porcentaje, color, porcentaje
        )
    progreso.short_description = '📊 Progreso'

# ===== PRESUPUESTOS =====
class ItemPresupuestoInline(admin.TabularInline):
    model = ItemPresupuesto
    extra = 1
    fields = ('tipo', 'descripcion', 'cantidad', 'unidad_medida', 'precio_unitario', 'total')
    readonly_fields = ('total',)

@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('codigo_presupuesto', 'obra', 'cliente', 'estado_badge', 'subtotal_guaranies', 'iva_guaranies', 'total_guaranies', 'fecha_creacion', 'vencimiento')
    list_filter = ('estado', 'fecha_creacion', 'fecha_aprobacion')
    search_fields = ('codigo_presupuesto', 'obra__nombre', 'cliente__username')
    list_per_page = 20
    date_hierarchy = 'fecha_creacion'
    inlines = [ItemPresupuestoInline]
    
    fieldsets = (
        ('Información General', {
            'fields': ('codigo_presupuesto', 'obra', 'cliente', 'constructor', 'descripcion_servicios')
        }),
        ('💰 Cálculos Financieros', {
            'fields': ('subtotal', 'iva_porcentaje', 'iva_monto', 'total'),
            'classes': ('wide',)
        }),
        ('📅 Fechas y Estado', {
            'fields': ('estado', 'dias_validez', 'fecha_validez', 'fecha_aprobacion')
        }),
    )
    
    readonly_fields = ('codigo_presupuesto', 'subtotal', 'iva_monto', 'total')
    
    def estado_badge(self, obj):
        colors = {
            'solicitado': '#6c757d',
            'en_revision': '#007bff',
            'aceptado': '#28a745',
            'rechazado': '#dc3545',
            'replanteado': '#ffc107'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 10px; font-weight: bold;">{}</span>',
            colors.get(obj.estado, '#6c757d'),
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def subtotal_guaranies(self, obj):
        return format_html('<strong style="color: #007bff;">₲ {}</strong>', '{:,.0f}'.format(float(obj.subtotal)))
    subtotal_guaranies.short_description = '💵 Subtotal'
    
    def iva_guaranies(self, obj):
        return format_html('<strong style="color: #ffc107;">₲ {}</strong>', '{:,.0f}'.format(float(obj.iva_monto)))
    iva_guaranies.short_description = '📊 IVA (10%)'
    
    def total_guaranies(self, obj):
        return format_html('<strong style="color: #28a745; font-size: 16px;">₲ {}</strong>', '{:,.0f}'.format(float(obj.total)))
    total_guaranies.short_description = '💰 TOTAL'
    
    def vencimiento(self, obj):
        fecha = obj.get_fecha_vencimiento()
        if fecha:
            vencido = obj.esta_vencido()
            color = '#dc3545' if vencido else '#28a745'
            icon = '❌' if vencido else '✅'
            return format_html(
                '<span style="color: {};">{} {}</span>',
                color, icon, fecha.strftime('%d/%m/%Y')
            )
        return '-'
    vencimiento.short_description = '⏰ Vencimiento'

# ===== PRODUCTOS =====
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_guaranies', 'stock_badge', 'tienda', 'activo', 'fecha_creacion')
    list_filter = ('categoria', 'activo', 'tienda', 'fecha_creacion')
    search_fields = ('nombre', 'descripcion', 'sku')
    list_editable = ('activo',)
    list_per_page = 25
    date_hierarchy = 'fecha_creacion'
    
    def precio_guaranies(self, obj):
        return format_html('<strong style="color: #d52b1e;">₲ {}</strong>', '{:,.0f}'.format(float(obj.precio)))
    precio_guaranies.short_description = '💰 Precio'
    
    def stock_badge(self, obj):
        if obj.stock == 0:
            color = '#dc3545'
            icon = '❌'
        elif obj.stock < 5:
            color = '#ffc107'
            icon = '⚠️'
        else:
            color = '#28a745'
            icon = '✅'
        return format_html('<span style="color: {}; font-weight: bold;">{} {}</span>', color, icon, obj.stock)
    stock_badge.short_description = '📦 Stock'

# ===== PEDIDOS =====
@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('numero_pedido', 'usuario', 'estado_badge', 'total_guaranies', 'metodo_pago', 'fecha_pedido')
    list_filter = ('estado', 'metodo_pago', 'fecha_pedido')
    search_fields = ('numero_pedido', 'usuario__username', 'email')
    list_per_page = 20
    date_hierarchy = 'fecha_pedido'
    
    def estado_badge(self, obj):
        colors = {
            'pendiente': '#ffc107',
            'confirmado': '#007bff',
            'preparando': '#17a2b8',
            'enviado': '#6f42c1',
            'entregado': '#28a745',
            'cancelado': '#dc3545'
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 10px; border-radius: 10px;">{}</span>',
            colors.get(obj.estado, '#6c757d'),
            obj.get_estado_display()
        )
    estado_badge.short_description = 'Estado'
    
    def total_guaranies(self, obj):
        return format_html('<strong style="color: #28a745; font-size: 15px;">₲ {}</strong>', '{:,.0f}'.format(float(obj.total)))
    total_guaranies.short_description = '💰 Total'

# ===== NOTIFICACIONES =====
@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo_badge', 'leida_badge', 'fecha_creacion')
    list_filter = ('tipo', 'leida', 'fecha_creacion')
    search_fields = ('titulo', 'mensaje', 'usuario__username')
    list_per_page = 30
    date_hierarchy = 'fecha_creacion'
    
    def tipo_badge(self, obj):
        return format_html('<span>{} {}</span>', obj.get_icono(), obj.get_tipo_display())
    tipo_badge.short_description = 'Tipo'
    
    def leida_badge(self, obj):
        if obj.leida:
            return format_html('<span style="color: #28a745;">✅ Leída</span>')
        return format_html('<span style="color: #ffc107;">⏳ Pendiente</span>')
    leida_badge.short_description = 'Estado'

# Registrar modelos simples
admin.site.register(Tienda)
admin.site.register(Categoria)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(ItemPedido)

# =============================================
# ADMIN PARA NUEVOS MODELOS SUPER AVANZADOS
# =============================================

@admin.register(Contratista)
class ContratistaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'nombre_empresa', 'especialidad', 'departamento', 'estado', 'calificacion_promedio', 'verificado']
    list_filter = ['especialidad', 'departamento', 'estado', 'verificado', 'activo']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'nombre_empresa', 'ruc']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion', 'calificacion_promedio', 'total_trabajos_completados']
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'nombre_empresa', 'ruc', 'especialidad', 'estado')
        }),
        ('Ubicación', {
            'fields': ('departamento', 'ciudad', 'direccion_completa')
        }),
        ('Contacto', {
            'fields': ('telefono_principal', 'telefono_secundario', 'email_empresa', 'sitio_web')
        }),
        ('Información Profesional', {
            'fields': ('años_experiencia', 'licencia_profesional', 'registro_profesional')
        }),
        ('Tarifas', {
            'fields': ('tarifa_por_hora', 'tarifa_por_dia', 'tarifa_por_proyecto')
        }),
        ('Calificaciones', {
            'fields': ('calificacion_promedio', 'total_trabajos_completados', 'total_clientes_satisfechos')
        }),
        ('Estado', {
            'fields': ('activo', 'verificado', 'fecha_registro', 'fecha_actualizacion')
        })
    )

@admin.register(Propietario)
class PropietarioAdmin(admin.ModelAdmin):
    list_display = ['nombre_completo', 'tipo_propietario', 'cedula_ruc', 'departamento', 'verificado']
    list_filter = ['tipo_propietario', 'departamento', 'verificado', 'activo']
    search_fields = ['nombre_completo', 'cedula_ruc', 'usuario__username']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

@admin.register(Propiedad)
class PropiedadAdmin(admin.ModelAdmin):
    list_display = ['nombre_propiedad', 'propietario', 'tipo_propiedad', 'departamento', 'estado_propiedad']
    list_filter = ['tipo_propiedad', 'departamento', 'estado_propiedad', 'activa']
    search_fields = ['nombre_propiedad', 'propietario__nombre_completo', 'direccion_completa']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'codigo_empleado', 'cargo', 'estado', 'salario_base', 'fecha_ingreso']
    list_filter = ['cargo', 'estado', 'turno', 'departamento']
    search_fields = ['usuario__username', 'codigo_empleado', 'cedula_identidad']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('usuario', 'codigo_empleado', 'cargo', 'estado')
        }),
        ('Información Personal', {
            'fields': ('cedula_identidad', 'fecha_nacimiento', 'lugar_nacimiento', 'estado_civil')
        }),
        ('Contacto', {
            'fields': ('telefono_principal', 'telefono_emergencia', 'contacto_emergencia')
        }),
        ('Ubicación', {
            'fields': ('departamento', 'ciudad', 'direccion_completa')
        }),
        ('Información Laboral', {
            'fields': ('fecha_ingreso', 'fecha_salida', 'turno', 'salario_base', 'bonificaciones')
        }),
        ('Capacitación', {
            'fields': ('nivel_educacion', 'certificaciones', 'años_experiencia')
        }),
        ('Evaluación', {
            'fields': ('calificacion_desempeño', 'observaciones')
        })
    )

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'tipo_proveedor', 'departamento', 'estado', 'calificacion_calidad', 'verificado']
    list_filter = ['tipo_proveedor', 'departamento', 'estado', 'verificado', 'activo']
    search_fields = ['nombre_empresa', 'ruc', 'persona_contacto']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre_empresa', 'ruc', 'tipo_proveedor', 'estado')
        }),
        ('Contacto', {
            'fields': ('persona_contacto', 'cargo_contacto', 'telefono_principal', 'telefono_secundario', 'email_principal', 'email_secundario', 'sitio_web')
        }),
        ('Ubicación', {
            'fields': ('departamento', 'ciudad', 'direccion_completa')
        }),
        ('Información Comercial', {
            'fields': ('años_mercado', 'capacidad_suministro', 'tiempo_entrega_promedio')
        }),
        ('Condiciones Comerciales', {
            'fields': ('forma_pago_preferida', 'descuento_volumen', 'credito_maximo')
        }),
        ('Calificaciones', {
            'fields': ('calificacion_calidad', 'calificacion_precio', 'calificacion_entrega', 'calificacion_servicio')
        }),
        ('Estado', {
            'fields': ('activo', 'verificado', 'fecha_registro', 'fecha_actualizacion')
        })
    )

@admin.register(ProductoProveedor)
class ProductoProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre_producto', 'proveedor', 'precio_unitario', 'stock_disponible', 'activo']
    list_filter = ['proveedor', 'activo']
    search_fields = ['nombre_producto', 'codigo_producto', 'marca']
    readonly_fields = ['fecha_registro', 'fecha_actualizacion']

@admin.register(EvaluacionProveedor)
class EvaluacionProveedorAdmin(admin.ModelAdmin):
    list_display = ['proveedor', 'evaluador', 'calidad_productos', 'puntualidad_entrega', 'fecha_evaluacion']
    list_filter = ['calidad_productos', 'puntualidad_entrega', 'precio_competitivo', 'atencion_cliente', 'recomendaria']
    search_fields = ['proveedor__nombre_empresa', 'evaluador__username']
    readonly_fields = ['fecha_evaluacion']

@admin.register(ContratoContratista)
class ContratoContratistaAdmin(admin.ModelAdmin):
    list_display = ['numero_contrato', 'obra', 'contratista', 'estado', 'monto_total', 'fecha_creacion']
    list_filter = ['estado', 'fecha_creacion']
    search_fields = ['numero_contrato', 'obra__nombre', 'contratista__nombre_empresa']
    readonly_fields = ['numero_contrato', 'fecha_creacion', 'fecha_actualizacion', 'anticipo_monto']
    fieldsets = (
        ('Información Básica', {
            'fields': ('numero_contrato', 'obra', 'contratista', 'creado_por', 'estado')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio_prevista', 'fecha_fin_prevista', 'fecha_firma', 'fecha_inicio_real', 'fecha_fin_real')
        }),
        ('Términos Financieros', {
            'fields': ('monto_total', 'anticipo_porcentaje', 'anticipo_monto')
        }),
        ('Términos y Condiciones', {
            'fields': ('descripcion_trabajo', 'materiales_incluidos', 'mano_obra_incluida', 'garantia_meses')
        }),
        ('Penalizaciones y Bonificaciones', {
            'fields': ('penalizacion_retraso', 'bonificacion_adelanto')
        }),
        ('Estado', {
            'fields': ('activo', 'fecha_creacion', 'fecha_actualizacion')
        })
    )
