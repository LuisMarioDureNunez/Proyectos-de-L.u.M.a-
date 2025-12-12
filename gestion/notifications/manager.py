from django.db import models
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
from ..models import Notificacion, ConfiguracionNotificacion

class NotificationManager:
    """Gestor profesional de notificaciones"""
    
    @staticmethod
    def crear_notificacion(usuario, tipo, titulo, mensaje, datos_extra=None, presupuesto=None, obra=None):
        """Crear una nueva notificación"""
        try:
            # Verificar configuración del usuario
            config, created = ConfiguracionNotificacion.objects.get_or_create(usuario=usuario)
            if not config.puede_recibir_notificacion(tipo):
                return None
            
            # Crear notificación
            notificacion = Notificacion.objects.create(
                usuario=usuario,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                datos_extra=datos_extra or {},
                presupuesto=presupuesto,
                obra=obra
            )
            
            # Enviar notificación en tiempo real
            NotificationManager.enviar_notificacion_tiempo_real(notificacion)
            
            # Enviar email si está configurado
            if getattr(config, f'email_{tipo.split("_")[0]}', True):
                NotificationManager.enviar_email_notificacion(notificacion)
            
            return notificacion
            
        except Exception as e:
            print(f"Error creando notificación: {e}")
            return None
    
    @staticmethod
    def enviar_notificacion_tiempo_real(notificacion):
        """Enviar notificación a través de WebSockets"""
        try:
            channel_layer = get_channel_layer()
            group_name = f"user_{notificacion.usuario.id}"
            
            async_to_sync(channel_layer.group_send)(
                group_name,
                {
                    'type': 'enviar_notificacion',
                    'notificacion': notificacion.to_dict()
                }
            )
            
            notificacion.enviada = True
            notificacion.save(update_fields=['enviada'])
            
        except Exception as e:
            print(f"Error enviando notificación en tiempo real: {e}")
    
    @staticmethod
    def enviar_email_notificacion(notificacion):
        """Enviar notificación por email"""
        try:
            from django.core.mail import send_mail
            from django.conf import settings
            
            subject = f"🔔 {notificacion.titulo} - Sistema de Gestión Paraguay"
            message = f"""
            {notificacion.get_icono()} {notificacion.titulo}
            
            {notificacion.mensaje}
            
            Fecha: {notificacion.fecha_creacion.strftime('%d/%m/%Y %H:%M')}
            
            ---
            Sistema de Gestión de Presupuestos para Obras Civiles
            Paraguay
            """
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [notificacion.usuario.email],
                fail_silently=True,
            )
            
        except Exception as e:
            print(f"Error enviando email de notificación: {e}")
    
    @staticmethod
    def notificar_presupuesto_creado(presupuesto):
        """Notificar creación de presupuesto"""
        titulo = "Nuevo Presupuesto Creado"
        mensaje = f"Se ha creado un nuevo presupuesto #{presupuesto.codigo_presupuesto} para la obra '{presupuesto.obra.nombre}'"
        
        datos_extra = {
            'url': f"/presupuestos/{presupuesto.id}/",
            'presupuesto_id': presupuesto.id,
            'obra_id': presupuesto.obra.id,
        }
        
        # Notificar al cliente
        NotificationManager.crear_notificacion(
            usuario=presupuesto.cliente,
            tipo='presupuesto_creado',
            titulo=titulo,
            mensaje=mensaje,
            datos_extra=datos_extra,
            presupuesto=presupuesto
        )
        
        # Notificar al constructor si está asignado
        if presupuesto.constructor:
            NotificationManager.crear_notificacion(
                usuario=presupuesto.constructor,
                tipo='presupuesto_creado',
                titulo=titulo,
                mensaje=mensaje,
                datos_extra=datos_extra,
                presupuesto=presupuesto
            )
    
    @staticmethod
    def notificar_presupuesto_aceptado(presupuesto):
        """Notificar aceptación de presupuesto"""
        titulo = "Presupuesto Aceptado ✅"
        mensaje = f"El presupuesto #{presupuesto.codigo_presupuesto} ha sido aceptado por el cliente"
        
        datos_extra = {
            'url': f"/presupuestos/{presupuesto.id}/",
            'presupuesto_id': presupuesto.id,
        }
        
        # Notificar al constructor
        if presupuesto.constructor:
            NotificationManager.crear_notificacion(
                usuario=presupuesto.constructor,
                tipo='presupuesto_aceptado',
                titulo=titulo,
                mensaje=mensaje,
                datos_extra=datos_extra,
                presupuesto=presupuesto
            )
    
    @staticmethod
    def notificar_stock_bajo(material):
        """Notificar stock bajo de material"""
        titulo = "Stock Bajo de Material ⚠️"
        mensaje = f"El material '{material.nombre}' tiene stock bajo ({material.stock} unidades)"
        
        datos_extra = {
            'url': f"/materiales/{material.id}/",
            'material_id': material.id,
        }
        
        # Notificar a todos los administradores
        from ..models import UsuarioPersonalizado
        administradores = UsuarioPersonalizado.objects.filter(rol='admin', is_active=True)
        
        for admin in administradores:
            NotificationManager.crear_notificacion(
                usuario=admin,
                tipo='material_stock_bajo',
                titulo=titulo,
                mensaje=mensaje,
                datos_extra=datos_extra
            )
    
    @staticmethod
    def obtener_notificaciones_no_leidas(usuario, limite=10):
        """Obtener notificaciones no leídas del usuario"""
        return Notificacion.objects.filter(
            usuario=usuario,
            leida=False
        ).order_by('-fecha_creacion')[:limite]
    
    @staticmethod
    def marcar_todas_como_leidas(usuario):
        """Marcar todas las notificaciones como leídas"""
        Notificacion.objects.filter(
            usuario=usuario,
            leida=False
        ).update(
            leida=True,
            fecha_leida=timezone.now()
        )