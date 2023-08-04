from functools import reduce
import json
import  asyncio
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from django.db.models import Q
from  joystick import camera
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
        await self.accept()
       
        
        
        
    async def disconnect(self, close_code):
         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
       
        
       

    async def receive(self, text_data):
       
        text_data_json = json.loads(text_data)
        message = text_data_json

        x=int(message.get('x'))
        y=int(message.get('y'))
        s=int(message.get('s'))
        a=int(message.get('a'))
        if x==0 and y==0 and s==0 and a==0:
           await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'motorstop'})
        elif x in range(-50,50) and y in range(-205,-50):
            await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'forward'})
        elif x in range(-50,50) and y in range(50,205):
                        await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'backward'}) 
        elif y in range(-50,50) and x in range(-205,-50):
                        await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'left'})
        elif y in range(-50,50) and x in range(50,205):
            await self. channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'right'}) 
        else:
            await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'motorstop'})
            
        # print(message)
        # if message!="":
        #     await self.channel_layer.group_send(
        #                                     self.room_group_name, {"type": "live_message", "message": message}
        #                                     )
        # if  data!="":

    async def live_message(self, event,type='live_message'):
        
     
        message = event['message']

        await self.send(text_data=json.dumps(message))
cam = camera.VideoCamera()        
class CameraConsumer(AsyncWebsocketConsumer):
        async def connect(self):
        
            # self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
            self.room_name=self.scope['user']
            print(self.room_name)
            
            
            self.room_group_name = "rc_%s" % "joystick"
            
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            print(self.scope['user'])
            await self.accept()
            # await self.channel_layer.group_send(
            #                                         self.room_group_name, {"type": "cam_message", "message":"2"}
            #                                         )
            
            
            
        async def disconnect(self, close_code):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
            self.state= False

        
            
        

        async def receive(self, text_data):
            # print(text_data)
            text_data_json = text_data
            message = text_data_json

                
            try:
                
                # for i in camera.gen(cam):
                #     #  print(type(i))
                #      await asyncio.sleep(2)
                await self.channel_layer.group_send(
                                                    self.room_group_name, {"type": "cam_message", "message":str(next(camera.gen(cam)))}
                                                    )
                
            except:  # This is bad!
                pass

        async def cam_message(self, event,type='cam_message'):
            
        
            message = event['message']
            # print(message)
            await self.send(text_data=json.dumps(message))
        

