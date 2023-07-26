from django.urls import re_path

from joystick import consumers

#r"ws/sc/(?P<room_name>\w+)/$"
websocket_urlpatterns = [
    re_path(r"ws/sc/sc/", consumers.NewConsumer.as_asgi()),

]