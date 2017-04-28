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
Scale=3
out_screen_size=[360,580]
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('Main/default.html')
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    is_control=False
    screen_ratioX=0
    screen_ratioY=0
    def check_origin(self, origin):
        print(origin)
        return True

    def open(self):
        self.write_message(str(out_screen_size))
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
    #跟据输出显示大小和手机屏幕实际大小得出宽和高的比值
    def get_screen_ratio(self):
        self.screen_ratioX=(phone.device.width/phone.device.virtualscale)/out_screen_size[0]
        self.screen_ratioY = (phone.device.height / phone.device.virtualscale) /out_screen_size[1]

    #根据接收的参数判断动作后向手机端发送相应的指令
    def TouchEvent(self,buffer):
        self.get_screen_ratio()
        str = buffer;
        strArry = str.split(':');

        if len(strArry) < 2:
            return;
        type=strArry[0]
        xy=strArry[1]
        if type == '3':
            pnt = xy.split(',');
            #跟据输出显示大小和手机屏幕实际大小的比值，换算实际手机中的坐标
            X = int(float(pnt[0]))*self.screen_ratioX
            Y = int(float(pnt[1]))*self.screen_ratioY
            ad.TouchMove(X, Y);

        elif type == '1':
            pnt = xy.split(',');
            X = int(float(pnt[0]))*self.screen_ratioX
            Y = int(float(pnt[1]))*self.screen_ratioY
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


