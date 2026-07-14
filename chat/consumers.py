import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer


# ws://localhost:8000/ws/chat/123/ → room_id = 123
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat{self.room_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room_id = data['room_id']

        # these are user defined
        user = await self.get_user(username)
        room =  await  self.get_room(room_id)

        await self.save_message(room, user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    @staticmethod
    @database_sync_to_async
    def save_message(room, user, message):
        #lazy import
        from .models import Message
        Message.objects.create(chatroom=room, sender=user, content=message)

    @staticmethod
    @database_sync_to_async
    def get_room(room_id):
        from .models import ChatRoom
        return ChatRoom.objects.get(id=room_id)

    @staticmethod
    @database_sync_to_async
    def get_user(username):
        from django.contrib.auth.models import User
        return User.objects.get(username=username)
    