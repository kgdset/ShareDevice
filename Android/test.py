import struct

from Minicap import Banner
import socket
import sys

class _MinicapStream():
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
    #用于提取byte数组
    def subByteArray(arr,start,end):
        len = end - start;
        newbyte = len;
        #Buffer.BlockCopy(arr, start, newbyte, 0, len);
        return newbyte;

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
        frameBody =''
        recv_cnt = 0
        reallen = self.client.recv(self.chunk)
        len_buf = len(reallen)
        print(len_buf)
        print(reallen[6])

        recv_cnt = recv_cnt + 1



        # 写入图片流到队列，并通知监听器更新对象
    def AddStream(self,frameBody):
        self.bytequeue.Enqueue(frameBody)
        #if (Update != null)
            #使用事件来通知给订阅者
            #Update()

if __name__ == '__main__':
    client =_MinicapStream()
    client.ReadImageStream()




