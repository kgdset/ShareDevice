import socket
import threading

import time
from Android import ADB
from Android.AndroidDevice import _AndroidDevice
from MiniTouch import Banner
class _MiniTouchStream():
    HOST = "127.0.0.1";
    PORT = 1111

    banner =''
    device=''
    chunk = 64

    #界面的显示比例
    def __init__(self,device,PORT = 1111):
        self.device = device
        self.PORT=PORT
        self.banner=Banner._Banner();
        ADDR = (self.HOST, PORT)
        self.socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(ADDR)

        #self.ParseBanner(self.socket)

    def Stop(self):
        try:
            self.socket.close();
        except socket.error:
            pass

    #首次接收minitouh的banner信息
    def ParseBanner(self):
        chunk =self.socket.recv(self.chunk);
        result=str(chunk)
        print(result)
        result=result.replace('b','')
        result=result.replace('\\n',' ')
        result=result.split(' ')

        #读取banner数据
        self.banner.version = int(result[1]);
        self.banner.maxcontacts = int(result[3]);
        self.banner.maxx = int(result[4]);
        self.banner.maxy = int(result[5]);
        self.banner.maxpressure = int(result[6]);
        self.banner.pid = int(result[8]);
        #换算真实设备和minitouch识别到支持的百分比
        self.banner.percentx = self.device.width / self.banner.maxx
        self.banner.percenty = self.device.height / self.banner.maxy

    #按键
    def ClickKeycode(self,key,device_id):
        t1 = threading.Thread(target=self.adb, name='thread1', args=(key,device_id))
        t1.start()

    def adb(self,cmd,device_id):
        print('cmd:'+cmd)
        print(device_id)
        adb=ADB.AdbTools(device_id)
        adb.shell('input keyevent ' + str(cmd))
    #用于执行按下操作
    def TouchDown(self,*downpoint):
        #转换为设备的真实坐标
        realpoint = self.PointConvert(downpoint)
        #通过minitouch命令执行点击;传递的文本'd'为点击命令，0为触摸点索引，XY为具体的坐标值，50为压力值，注意必须以\n结尾，否则无法触发动作
        cmd=str.format("d 0 {0} {1} 50\n", str(realpoint[0]), str(realpoint[1]))
        self.ExecuteTouch(cmd)

    def TouchUp(self):
        #松开触摸点
        cmd=str.format("u 0\n")
        self.ExecuteTouch(cmd)

    def TouchMove(self,*movepoint):
        #转换为设备的真实坐标
        realpoint = self.PointConvert(movepoint)
        #通过minitouch命令执行划动;传递的文本'd'为划动命令，0为触摸点索引，XY为要滑动到的坐标值，50为压力值，注意必须以\n结尾，否则无法触发动作
        cmd=str.format("m 0 {0} {1} 50\n", str(realpoint[0]), str(realpoint[1]))
        self.ExecuteTouch(cmd)

    #发送定义好的触摸动作命令进行动作执行
    def ExecuteTouch(self,touchcommand):
        #将动作数据转换为socket要提交的byte数据
        inbuff=bytes(touchcommand, encoding = "ASCII")
        #发送socket数据
        self.socket.send(inbuff);
        #提交触摸动作的命令
        ccommand = "c\n";
        inbuff =bytes(ccommand, encoding = "ASCII")
        #发送socket数据确认触摸动作的执行
        self.socket.send(inbuff);

    #设备真实坐标转换
    def PointConvert(self,point):
        #根据设备显示比例换算出设备真实坐标点
        realpoint = (int(point[0] / self.banner.percentx) * self.device.virtualscale, (int)(point[1] / self.banner.percenty) * self.device.virtualscale);
        return realpoint;
if __name__=='__main__':
    device = _AndroidDevice()
    device.AndroidDevice()
    device.virtualscale = 4;
    device.orientation = 0;
    device.setScale(3)
    minicaptask = threading.Thread(target=device.StartMiniTouchServer, name='test', args=());
    minicaptask.start();
    time.sleep(3)
    s=_MiniTouchStream(device)