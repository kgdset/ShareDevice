from Minicap import Banner
import socket
import sys
import matplotlib.pyplot as plt
import numpy as np
class _MinicapStream():
    host = ''
    port = 51234
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    client = ''
    bytequeue=''
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
                        #self.AddStream(frameBody);
                        cursor += frameBodyLength;
                        frameBodyLength = readFrameBytes = 0;
                        clientsock, clientaddr = self.s.accept()
                        # process the connection
                        print("Got connection from", clientsock.getpeername())
                        data = clientsock.recv(len(frameBody))
                        n = clientsock.send(frameBody)
                        clientsock.close()
                        frameBody =b'';
                    else:
                        frameBody = frameBody+chunk[cursor:len_buf]
                        frameBodyLength -= len_buf - cursor;
                        readFrameBytes += len_buf - cursor;
                        cursor = len_buf;
            chunk = self.client.recv(self.chunk)

    # 写入图片流到队列，并通知监听器更新对象
    def AddStream(self,frameBody):
        self.bytequeue.Enqueue(frameBody)
        #if (Update != null)
            #使用事件来通知给订阅者
            #Update()

if __name__ == '__main__':
    client =_MinicapStream()
    client.ReadImageStream()




