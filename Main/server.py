import os
import threading

import time
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.web
from Android.AndroidDevice import _AndroidDevice
from Main import config
from Main.DeviceControl import _DeviceControl
from Minicap.MinicapStream import _MinicapStream
Scale=config.SCALE
PORT=config.PORT
out_screen_size=config.OUT_SCREEN_SIZE
phone=''
phone_port=['1111','2222','3333','4444']

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        print(self.request.remote_ip)
        device_id=self.get_argument('device_id')
        global phone
        phone = PhoneConfig(device_id)
        phone.setConfig()
        self.render('Main/default.html')

class PhoneConfig():
    minicap = ''
    device_control = ''
    phone_list={}
    def __init__(self,device_id=''):
        if device_id not in phone_port:
            self.phone_list[device_id]=phone_port[len(self.phone_list)]
        self.capport=int(self.phone_list.get(device_id))
        self.touchport=self.capport+1
        self.device=_AndroidDevice(device_id,self.capport,self.touchport)


    def setConfig(self):
        self.device.setOrientation(0)
        self.device.setScale(Scale)
        minicaptask =threading.Thread(target=self.device.StartMinicapServer,name='minicaptask',args=());
        minicaptask.start();
        time.sleep(1);
        minitouchtask = threading.Thread(target=self.device.StartMiniTouchServer, name='minitouchtask', args=());
        minitouchtask.start();
        time.sleep(5)
        self.minicap = _MinicapStream(self.capport)
        self.device_control = _DeviceControl(self.device,self.touchport)
        t1 = threading.Thread(target=self.minicap.ReadImageStream, name='thread1', args=())
        t1.start()
        t2 = threading.Thread(target=self.device_control.minitouch.ParseBanner, name='thread1', args=())
        t2.start()
        time.sleep(3)
        print('*********************************************************')
        print('********************** StartServer **********************')
        print('*********************************************************')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    is_control=False

    def check_origin(self, origin):
        print(origin)
        return True

    def open(self):
        self.write_message(str(out_screen_size))
        self.start_server()

    def on_message(self, message):
        if len(message)>1:
            if(message=='control'):
                self.is_control=True
            else:
                if self.is_control:
                    phone.device_control.TouchEvent(message)
                else:
                    pass

    def start_server(self):

        t3 = threading.Thread(target=self.senddata, name='thread2', args=())
        t3.start()

    def senddata(self):
        while True:
            time.sleep(1/config.REFRESH_RATE)
            try:
                if phone.minicap.update:
                    sends = phone.minicap.bytequeue
                    phone.minicap.update = False
                    self.write_message(sends,True)
            except:
                print('断开一个连接！')
                print(self.request.remote_ip)
                return

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



ws_app = Application()
server = tornado.httpserver.HTTPServer(ws_app)
server.listen(PORT)
tornado.ioloop.IOLoop.instance().start()



