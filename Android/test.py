# -*- coding:utf8 -*-
import threading
import time

import sys
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from Minicap import Banner
import socket

import hashlib
import base64

class websocket_thread(threading.Thread):
    def __init__(self, connection):
        super(websocket_thread, self).__init__()
        self.connection = connection

    def run(self):
        print('new websocket client joined!')
        reply = 'i got u, from websocket server.'
        length = len(reply)
        while True:
            time.sleep(1)
            print('发送数据：')
            self.connection.send(b'ssssssaaaaaeeeee')

class _MinicapStream():
    host = ''
    port = 51234
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    client = ''
    bytequeue=[b'']
    update=False
    banner=Banner._Banner()
    # 测试，连接本机
    HOST = '127.0.0.1'
    # 设置侦听端口
    PORT = 1313
    chunk = 4096
    ADDR = (HOST, PORT)
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)
        #ret_bytes = self.client.recv(1024)
        #ret_str = str(ret_bytes, encoding="utf-8")
        #print(ret_str)

    #存放由socket接收的图片字节信息数组的队列

    def ImageByteQueue(self):
        return self.bytequeue

    def Banner(self):
        return self.banner

    #读取图片流到队列
    def ReadImageStream(self):
        reallen=0
        readBannerBytes = 0
        bannerLength = 2
        readFrameBytes = 0
        frameBodyLength = 0
        frameBody =b''
        chunk = self.client.recv(self.chunk)

        print(chunk)
        while len(chunk)!= 0:
            len_buf = len(chunk)
            #print(chunk)
            cursor=0
            while cursor<len_buf:
                #读取banner信息
                if readBannerBytes < bannerLength:
                    if readBannerBytes==0:
                        self.banner.Version = chunk[cursor];
                    elif readBannerBytes == 1:
                        self.banner.Length = bannerLength = chunk[cursor];
                    elif readBannerBytes>1&readBannerBytes<6:
                        self.banner.Pid += (chunk[cursor] << ((readBannerBytes - 2) * 8))
                    elif readBannerBytes > 5 & readBannerBytes < 10:
                        self.banner.RealWidth += (chunk[cursor] << ((cursor - 6) * 8));
                    elif readBannerBytes > 9 & readBannerBytes < 14:
                        self.banner.RealHeight += (chunk << ((cursor - 10) * 8));
                    elif readBannerBytes > 13 & readBannerBytes < 18:
                        self.banner.VirtualWidth += (chunk[cursor] << ((cursor - 14) * 8));
                    elif readBannerBytes > 17 & readBannerBytes < 22:
                        self.banner.VirtualHeight += (chunk[cursor] << ((cursor - 2) * 8));
                    elif readBannerBytes ==22:
                        self.banner.Orientation += chunk[cursor] * 90;
                    elif readBannerBytes == 23:
                        self.banner.Quirks = chunk[cursor];
                    readBannerBytes += 1
                    cursor+=1

                #读取每张图片的头4个字节(图片大小)
                elif readFrameBytes < 4:
                    frameBodyLength += (chunk[cursor] << (readFrameBytes * 8))
                    cursor += 1;
                    readFrameBytes += 1;

                else:
                    #读取图片内容
                    if len_buf - cursor >= frameBodyLength:
                        #print(len(chunk))
                        #print(cursor)
                        #print(len_buf)
                        frameBody = frameBody+chunk[cursor:cursor + frameBodyLength]
                        print(frameBody)
                        self.AddStream(frameBody);
                        cursor += frameBodyLength;
                        frameBodyLength = readFrameBytes = 0;
                        #return frameBody
                        frameBody =b'';
                    else:
                        frameBody = frameBody+chunk[cursor:len_buf]
                        frameBodyLength -= len_buf - cursor;
                        readFrameBytes += len_buf - cursor;
                        cursor = len_buf;
            chunk = self.client.recv(self.chunk)

    # 写入图片流到队列，并通知监听器更新对象
    def AddStream(self,frameBody):
        self.bytequeue.append(frameBody)
        if self.update==False:
            self.update=True
    def send(self):
        ws_app = Application()
        server = tornado.httpserver.HTTPServer(ws_app)
        server.listen(8080)
        tornado.ioloop.IOLoop.instance().start()
class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        pass

    def on_message(self, message):
        mini = _MinicapStream()
        t1 = threading.Thread(target=mini.ReadImageStream, name='thread1', args=())
        t1.start()
        while True:
            if mini.update:
                sends=mini.bytequeue[len(mini.bytequeue)-1]
                print(sys.getsizeof(sends))
                print(len(sends))
                mini.update = False
                self.write_message(sends)

    def on_close(self):
        pass


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/ws', WebSocketHandler)
        ]

        settings = {"template_path": "."}
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()









