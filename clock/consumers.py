import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from django.utils.timezone import localtime, now

from stafftracking.models import StaffTracking

User = get_user_model()


class ClockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]
        # self.room
        # self.room_group_name = "exam_5"
        # self.room_group_name = self.room_name

        # Join clock room
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "check_clock",
                "message": "hello",
            },
        )

    async def disconnect(self, close_code):
        # Leave clock room
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        # message = "Hello my friend"

        # Send message to clock room
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "check_clock",
                "message": message,
            },
        )

    def get_current_time(self):
        return str(localtime(now()))

    # Receive message from clock room
    async def check_clock(self, event):
        # message = event["message"]
        # print(message)

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    # "message": "fellow"
                    "cur_time": self.get_current_time()
                }
            )
        )

    async def get_exam(self, event):
        message = event["status"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"status": message, "cur_time": self.get_current_time()}
            )
        )

    async def get_session_status(self, event):
        message = event["is_published"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {"session_status": message, "cur_time": self.get_current_time()}
            )
        )


class StaffTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["room_name"]
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data=None):
        data = json.loads(text_data)
        await self.channel_layer.group_send(self.room_group_name, data)

    async def user_location(self, event):
        message = event["message"]
        await self.create_stafftracking_object(message)

    @database_sync_to_async
    def create_stafftracking_object(self, message):
        user_id = self.room_group_name.split("_")[1]
        user = User.objects.get(id=user_id)
        StaffTracking.objects.create(
            user=user, latitude=message["latitude"], longitude=message["longitude"]
        )

    async def send_request_user(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "user_location",
                }
            )
        )
