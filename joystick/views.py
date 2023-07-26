from django.shortcuts import render,HttpResponse
from django.http import StreamingHttpResponse
from  joystick import camera
from django.views.decorators import gzip
# Create your views here.
@gzip.gzip_page
def livefe(request):
    try:
        cam = camera.VideoCamera()
        return StreamingHttpResponse(camera.gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad!
        pass


def index(request ,*args, **kwargs):
    return render(request,'index.html',{"room_name": 'joystick'})

def  motorcontrol(request):
     if request.method=='POST':
        x=int(request.POST.get('x'))
        y=int(request.POST.get('y'))
        s=int(request.POST.get('s'))
        a=int(request.POST.get('a'))
        if x==0 and y==0 and s==0 and a==0:
            return HttpResponse('motorstop')
        elif x in range(-50,50) and y in range(-205,-50):
            return HttpResponse('forward')
        elif x in range(-50,50) and y in range(50,205):
            return HttpResponse('backward') 
        elif y in range(-50,50) and x in range(-205,-50):
            return HttpResponse('left')
        elif y in range(-50,50) and x in range(50,205):
            return HttpResponse('right') 
        else:
            return HttpResponse('motorstop')
     
     return HttpResponse('hello')