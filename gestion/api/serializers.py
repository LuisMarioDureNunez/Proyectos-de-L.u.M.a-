from rest_framework import serializers
from django.contrib.auth import authenticate
from ..models import (
    UsuarioPersonalizado, Obra, Presupuesto, ItemPresupuesto,
    Material, Maquinaria, Herramienta, Notificacion
)

class UserLoginSerializer(serializers.Serializer):
    """Serializer para login de usuario"""
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('Cuenta desactivada.')
            else:
                raise serializers.ValidationError('Credenciales inválidas.')
        else:
            raise serializers.ValidationError('Debe proporcionar username y password.')
        
        return data

class UserSerializer(serializers.ModelSerializer):
    """Serializer para usuario"""
    class Meta:
        model = UsuarioPersonalizado
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 
                 'rol', 'telefono', 'date_joined', 'last_login')
        read_only_fields = ('id', 'date_joined', 'last_login')

class MaterialSerializer(serializers.ModelSerializer):
    """Serializer para materiales"""
    precio_formateado = serializers.SerializerMethodField()
    
    class Meta:
        model = Material
        fields = ('id', 'nombre', 'descripcion', 'precio', 'precio_formateado',
                 'stock', 'unidad_medida', 'fecha_creacion')
    
    def get_precio_formateado(self, obj):
        return f"Gs. {obj.precio:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

class ObraSerializer(serializers.ModelSerializer):
    """Serializer para obras"""
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    presupuesto_asignado_formateado = serializers.SerializerMethodField()
    
    class Meta:
        model = Obra
        fields = ('id', 'nombre', 'descripcion', 'ubicacion', 'cliente', 'cliente_nombre',
                 'constructor', 'fecha_inicio', 'fecha_fin_estimada', 'fecha_fin_real',
                 'estado', 'estado_display', 'presupuesto_asignado', 'presupuesto_asignado_formateado',
                 'costo_real', 'fecha_creacion')
    
    def get_presupuesto_asignado_formateado(self, obj):
        if obj.presupuesto_asignado:
            return f"Gs. {obj.presupuesto_asignado:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return "Gs. 0"

class ItemPresupuestoSerializer(serializers.ModelSerializer):
    """Serializer para items de presupuesto"""
    total_formateado = serializers.SerializerMethodField()
    precio_unitario_formateado = serializers.SerializerMethodField()
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = ItemPresupuesto
        fields = ('id', 'tipo', 'tipo_display', 'descripcion', 'cantidad', 
                 'unidad_medida', 'precio_unitario', 'precio_unitario_formateado',
                 'total', 'total_formateado', 'material', 'maquinaria', 'herramienta')
    
    def get_total_formateado(self, obj):
        return f"Gs. {obj.total:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def get_precio_unitario_formateado(self, obj):
        return f"Gs. {obj.precio_unitario:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")

class PresupuestoSerializer(serializers.ModelSerializer):
    """Serializer para presupuestos"""
    items = ItemPresupuestoSerializer(many=True, read_only=True)
    cliente_nombre = serializers.CharField(source='cliente.get_full_name', read_only=True)
    obra_nombre = serializers.CharField(source='obra.nombre', read_only=True)
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    total_formateado = serializers.SerializerMethodField()
    subtotal_formateado = serializers.SerializerMethodField()
    iva_formateado = serializers.SerializerMethodField()
    fecha_vencimiento = serializers.SerializerMethodField()
    
    class Meta:
        model = Presupuesto
        fields = ('id', 'codigo_presupuesto', 'obra', 'obra_nombre', 'cliente', 'cliente_nombre',
                 'constructor', 'descripcion_servicios', 'subtotal', 'subtotal_formateado',
                 'iva_porcentaje', 'iva_monto', 'iva_formateado', 'total', 'total_formateado',
                 'estado', 'estado_display', 'fecha_creacion', 'fecha_vencimiento',
                 'fecha_aprobacion', 'items')
    
    def get_total_formateado(self, obj):
        return f"Gs. {obj.total:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def get_subtotal_formateado(self, obj):
        return f"Gs. {obj.subtotal:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def get_iva_formateado(self, obj):
        return f"Gs. {obj.iva_monto:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def get_fecha_vencimiento(self, obj):
        vencimiento = obj.get_fecha_vencimiento()
        return vencimiento.strftime("%d/%m/%Y") if vencimiento else None

class NotificacionSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones"""
    icono = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    tiempo_transcurrido = serializers.SerializerMethodField()
    
    class Meta:
        model = Notificacion
        fields = ('id', 'tipo', 'titulo', 'mensaje', 'leida', 'fecha_creacion',
                 'icono', 'color', 'tiempo_transcurrido', 'datos_extra')
    
    def get_icono(self, obj):
        return obj.get_icono()
    
    def get_color(self, obj):
        return obj.get_color()
    
    def get_tiempo_transcurrido(self, obj):
        from django.utils import timezone
        from django.utils.timesince import timesince
        
        return timesince(obj.fecha_creacion, timezone.now())

class DashboardStatsSerializer(serializers.Serializer):
    """Serializer para estadísticas del dashboard"""
    total_obras = serializers.IntegerField()
    total_presupuestos = serializers.IntegerField()
    presupuestos_aceptados = serializers.IntegerField()
    presupuestos_rechazados = serializers.IntegerField()
    total_materiales = serializers.IntegerField()
    monto_total_presupuestado = serializers.DecimalField(max_digits=15, decimal_places=2)
    monto_total_aceptado = serializers.DecimalField(max_digits=15, decimal_places=2)
    obras_en_proceso = serializers.IntegerField()
    obras_finalizadas = serializers.IntegerField()

class PresupuestoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear presupuestos"""
    class Meta:
        model = Presupuesto
        fields = ('obra', 'constructor', 'descripcion_servicios', 'iva_porcentaje', 'dias_validez')

class ItemPresupuestoCreateSerializer(serializers.ModelSerializer):
    """Serializer para crear items de presupuesto"""
    class Meta:
        model = ItemPresupuesto
        fields = ('tipo', 'descripcion', 'cantidad', 'unidad_medida', 'precio_unitario',
                 'material', 'maquinaria', 'herramienta')