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
    PORT = 8080
    BUFSIZ = 1024
    ADDR = (HOST, PORT)
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(self.ADDR)

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
        while reallen == self.client.recv(self.BUFSIZ)!=0:
            len = reallen
            for cursor in range(0,len):
                #读取banner信息
                if (readBannerBytes < bannerLength):

if __name__ == '__main__':
    client =_MinicapStream()



