import cv2
import threading
import base64
class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        (self.grabbed, self.frame) = self.video.read()
        self.frame1=cv2.resize(self.frame,(224,244))
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame1
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            self.frame1=cv2.resize(self.frame,(224,244))

def gen(camera):
    # while True:
        frame = camera.get_frame()
        yield(base64.b64encode(frame).decode('utf-8'))