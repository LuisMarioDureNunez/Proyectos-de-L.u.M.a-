from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'chat_general'
        self.room_group_name = f'chat_{self.room_name}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Enviar usuarios conectados
        await self.send_users_list()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'chat_message':
            message = data['message']
            username = data.get('username', 'Anónimo')
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                    'timestamp': data.get('timestamp')
                }
            )
        elif message_type == 'get_users':
            await self.send_users_list()

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'username': event['username'],
            'timestamp': event['timestamp']
        }))
    
    async def send_users_list(self):
        users = await self.get_active_users()
        await self.send(text_data=json.dumps({
            'type': 'users_list',
            'users': users
        }))
    
    @database_sync_to_async
    def get_active_users(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        return list(User.objects.filter(is_active=True).values('id', 'username', 'first_name', 'last_name')[:20])

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        pass

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': event.get('message', 'Nueva notificación')
        }))
