from functools import reduce
import json

from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from django.db.models import Q
import operator
# from django_q.tasks import async_task
from asgiref.sync import async_to_sync


from urllib import request

class NewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
       
        # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_name=self.scope['user']
        print(self.room_name)
        
        
        self.room_group_name = "sc_%s" % "joystick"
        
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        print(self.scope['user'])
        self.accept()
       
        
        
        
    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
       
        
       

    async def receive(self, text_data):
       
        text_data_json = json.loads(text_data)
        message = text_data_json
        
        print(message)
        if message!="":
            await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": message}
                                            )
        # if  data!="":

    async def live_message(self, event,type='live_message'):
        
     
        message = event['message']

        await self.send(text_data=json.dumps(message))
    
