import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async
from .models import ChatRoom, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['user'].id

        # Save message to the database
        await self.save_message(sender_id, self.room_name, message)
        
        # Broadcast message to the room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender_id': sender_id,
            }
        )
    
    async def chat_message(self, event):
        message = event['message']
        sender_id = event['sender_id']
        
        await self.send(text_data=json.dumps({
            'message': message,
            'sender_id': sender_id,
        }))
    
    @sync_to_async
    def save_message(self, sender_id, room_name, message):
        room = ChatRoom.objects.get(id=room_name)
        sender = User.objects.get(id=sender_id)
        ChatMessage.objects.create(room=room, sender=sender, message=message)
