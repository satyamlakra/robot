from functools import reduce
import json
import  asyncio
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from django.db.models import Q
from  joystick import camera
import operator
# from django_q.tasks import async_task
from asgiref.sync import async_to_sync
import RPi.GPIO as GPIO

from urllib import request
ledpin = 23 	
ledpin1 = 24							
GPIO.setwarnings(False)			
GPIO.setmode(GPIO.BCM)		
GPIO.setup(ledpin,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.LOW)
GPIO.setup(16,GPIO.OUT)
GPIO.output(16,GPIO.LOW)
GPIO.setup(20,GPIO.OUT)
GPIO.output(20,GPIO.LOW)
GPIO.setup(21,GPIO.OUT)
GPIO.output(21,GPIO.LOW)
pi_pwm = GPIO.PWM(ledpin,900)		
pi_pwm.start(0)	
pi_pwm1 = GPIO.PWM(ledpin1,900)		
pi_pwm1.start(0)
def cdu(x):
    pi_pwm.ChangeDutyCycle(x)
    pi_pwm1.ChangeDutyCycle(x)
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
            cdu(s)
            GPIO.output(26,GPIO.LOW)
            GPIO.output(16,GPIO.LOW)
            GPIO.output(20,GPIO.LOW)
            GPIO.output(21,GPIO.LOW)
           await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'motorstop'})
        elif x in range(-50,50) and y in range(-205,-50):
            cdu(s)
            GPIO.output(16,GPIO.LOW)
            GPIO.output(21,GPIO.LOW)
            GPIO.output(20,GPIO.HIGH)
            GPIO.output(26,GPIO.HIGH)
            
           
            await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'forward'})
        elif x in range(-50,50) and y in range(50,205):
                        cdu(s)
                        GPIO.output(26,GPIO.LOW)
                        GPIO.output(20,GPIO.LOW)
                        GPIO.output(16,GPIO.HIGH)
                        GPIO.output(21,GPIO.HIGH) 
                        await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'backward'}) 
        elif y in range(-50,50) and x in range(-205,-50):
                        cdu(s)
                        
                        GPIO.output(16,GPIO.LOW)
                        GPIO.output(20,GPIO.LOW)
                        GPIO.output(26,GPIO.HIGH)
                        GPIO.output(21,GPIO.HIGH)
                        await self.channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'left'})
        elif y in range(-50,50) and x in range(50,205):
            cdu(s)
            GPIO.output(26,GPIO.LOW)
            GPIO.output(16,GPIO.HIGH)
            GPIO.output(20,GPIO.LOW)
            GPIO.output(21,GPIO.HIGH)
            await self. channel_layer.group_send(
                                            self.room_group_name, {"type": "live_message", "message": 'right'}) 
        else:
            cdu(s)
            GPIO.output(26,GPIO.LOW)
            GPIO.output(16,GPIO.HIGH)
            GPIO.output(20,GPIO.HIGH)
            GPIO.output(21,GPIO.LOW)
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
        

