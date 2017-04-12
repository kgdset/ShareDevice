import os
import threading

import time
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.web
from Android.AndroidDevice import _AndroidDevice
from MiniTouch.MiniTouchStream import _MiniTouchStream
from Minicap.MinicapStream import _MinicapStream
mini=''
ad=''
phone=''
Scale=2
screen_size=[360,580]
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Main/default.html')
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    is_control=False
    screen_sizeX=0
    screen_sizeY=0
    def check_origin(self, origin):
        print(origin)
        return True

    def open(self):
        self.write_message(str(screen_size))
        self.start_server()
        #print(self.num1)

    def on_message(self, message):
        if len(message)>1:
            if(message=='control'):
                self.is_control=True
            else:
                if self.is_control:
                    self.TouchEvent(message)
                else:
                    pass

    def start_server(self):

        t3 = threading.Thread(target=self.senddata, name='thread2', args=())
        t3.start()

    def senddata(self):
        while True:
            time.sleep(0.001)
            try:
                if mini.update:
                    sends = mini.bytequeue
                    mini.update = False
                    self.write_message(sends,True)
            except:
                print('断开一个连接！')
                return

    def on_close(self):
        pass

    def create_screen_size(self):
        self.screen_sizeX=(phone.device.width/phone.device.virtualscale)/screen_size[0]
        self.screen_sizeY = (phone.device.height / phone.device.virtualscale) /screen_size[1]

    def TouchEvent(self,buffer):
        self.create_screen_size()
        str = buffer;
        strArry = str.split(':');

        if len(strArry) < 2:
            return;
        type=strArry[0]
        xy=strArry[1]
        if type == '3':
            pnt = xy.split(',');
            X = int(float(pnt[0]))*self.screen_sizeX
            Y = int(float(pnt[1]))*self.screen_sizeY
            ad.TouchMove(X, Y);

        elif type == '1':
            pnt = xy.split(',');
            X = int(float(pnt[0]))*self.screen_sizeX
            Y = int(float(pnt[1]))*self.screen_sizeY
            ad.TouchDown(X, Y);

        elif type == "2":
            ad.TouchUp();
        elif type == "4":
            ad.ClickKeycode(xy);

    def on_close(self):
        pass

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/ws', WebSocketHandler)
        ]
        settings = {"template_path": ".",
                    "static_path": os.path.join(os.path.dirname(__file__), "static")}
        tornado.web.Application.__init__(self, handlers, **settings)

class PhoneConfig():
    device=_AndroidDevice()
    device.AndroidDevice()
    def setConfig(self):
        self.device.orientation = 0;
        self.device.setScale(Scale)
        minicaptask =threading.Thread(target=self.device.StartMinicapServer,name='minicaptask',args=());
        minicaptask.start();
        time.sleep(1);
        minitouchtask = threading.Thread(target=self.device.StartMiniTouchServer, name='minitouchtask', args=());
        minitouchtask.start();
        time.sleep(1);

phone = PhoneConfig()
phone.setConfig()
time.sleep(5)
mini = _MinicapStream()
ad = _MiniTouchStream(phone.device)
t1 = threading.Thread(target=mini.ReadImageStream, name='thread1', args=())
t1.start()
t2 = threading.Thread(target=ad.ParseBanner, name='thread1', args=())
t2.start()
time.sleep(3)
print('*********************************************************')
print('********************** StartServer **********************')
print('*********************************************************')
ws_app = Application()
server = tornado.httpserver.HTTPServer(ws_app)
server.listen(8080)
tornado.ioloop.IOLoop.instance().start()


