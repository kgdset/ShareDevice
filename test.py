import os
import threading

import time
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('test.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    is_control = False
    clients = set()
    test=9
    @staticmethod
    def send_to_all(message):
        for c in WebSocketHandler.clients:
            c.write_message(message)
    def check_origin(self, origin):
        print(origin)
        return True

    def open(self):
        self.test=self.test+1
        self.write_message('Welcome to WebSocket')
        WebSocketHandler.clients.add(self)
        WebSocketHandler.send_to_all(str(id(self)) + '连接')
        self.start_server(self)


    def start_server(self,obj):

        t3 = threading.Thread(target=self.senddata, name='thread2', args=())
        t3.start()

    def senddata(self):
        while True:
            time.sleep(1)
            self.write_message(str(self.test))


    def on_message(self, message):
        pass


    def on_close(self):
        WebSocketHandler.clients.remove(self)
        WebSocketHandler.send_to_all(str(id(self)) + '断开连接')

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/ws', WebSocketHandler)
        ]
        settings = {"template_path": ".",
                    "static_path": os.path.join(os.path.dirname(__file__), "static")}
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__=='__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()