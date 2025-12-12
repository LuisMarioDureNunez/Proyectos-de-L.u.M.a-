import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Notificacion, UsuarioPersonalizado

class NotificacionConsumer(AsyncWebsocketConsumer):
    """Consumer para notificaciones en tiempo real"""
    
    async def connect(self):
        """Conectar al WebSocket"""
        self.user = self.scope["user"]
        
        if self.user.is_anonymous:
            await self.close()
            return
        
        self.room_group_name = f"user_{self.user.id}"
        
        # Unirse al grupo del usuario
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Enviar notificaciones no leídas al conectar
        notificaciones = await self.get_notificaciones_no_leidas()
        await self.send(text_data=json.dumps({
            'type': 'notificaciones_iniciales',
            'notificaciones': notificaciones
        }))
    
    async def disconnect(self, close_code):
        """Desconectar del WebSocket"""
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Recibir mensaje del WebSocket"""
        try:
            data = json.loads(text_data)
            tipo = data.get('type')
            
            if tipo == 'marcar_como_leida':
                notificacion_id = data.get('notificacion_id')
                await self.marcar_notificacion_como_leida(notificacion_id)
                
            elif tipo == 'marcar_todas_leidas':
                await self.marcar_todas_como_leidas()
                
        except Exception as e:
            print(f"Error procesando mensaje WebSocket: {e}")
    
    async def enviar_notificacion(self, event):
        """Enviar notificación al cliente"""
        notificacion = event['notificacion']
        
        await self.send(text_data=json.dumps({
            'type': 'nueva_notificacion',
            'notificacion': notificacion
        }))
    
    @database_sync_to_async
    def get_notificaciones_no_leidas(self):
        """Obtener notificaciones no leídas"""
        if self.user.is_anonymous:
            return []
        
        notificaciones = Notificacion.objects.filter(
            usuario=self.user,
            leida=False
        ).order_by('-fecha_creacion')[:10]
        
        return [notif.to_dict() for notif in notificaciones]
    
    @database_sync_to_async
    def marcar_notificacion_como_leida(self, notificacion_id):
        """Marcar notificación como leída"""
        try:
            notificacion = Notificacion.objects.get(
                id=notificacion_id,
                usuario=self.user
            )
            notificacion.marcar_como_leida()
            return True
        except Notificacion.DoesNotExist:
            return False
    
    @database_sync_to_async
    def marcar_todas_como_leidas(self):
        """Marcar todas las notificaciones como leídas"""
        Notificacion.objects.filter(
            usuario=self.user,
            leida=False
        ).update(leida=True)
        return True