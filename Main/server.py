import threading

import time
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import tornado.web
from Android.AndroidDevice import _AndroidDevice
from Minicap.MinicapStream import _MinicapStream


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.write_message('ok')

    def on_message(self, message):
        mini = _MinicapStream()
        t1 = threading.Thread(target=mini.ReadImageStream, name='thread1', args=())
        t1.start()
        while True:
            if mini.update:
                sends = mini.bytequeue
                mini.update = False
                self.write_message(sends,True)

    def on_close(self):
        pass

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/ws', WebSocketHandler)
        ]
        settings = {"template_path": "."}
        tornado.web.Application.__init__(self, handlers, **settings)
class PhoneConfig():
    device=_AndroidDevice()
    device.AndroidDevice()
    def setConfig(self):
        self.device.virtualscale = 3;
        self.device.orientation = 0;
        self.device.setScale(3)
        minicaptask =threading.Thread(target=self.device.StartMinicapServer,name='test',args=());
        minicaptask.start();
        time.sleep(1);

if __name__ == '__main__':
    phone=PhoneConfig()
    phone.setConfig()
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()