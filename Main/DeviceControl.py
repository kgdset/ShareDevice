#根据接收的参数判断动作后向手机端发送相应的指令
from Main import config
from MiniTouch.MiniTouchStream import _MiniTouchStream
class _DeviceControl():

    def __init__(self,device,port,device_id):
        self.device=device
        self.device_id=device_id
        self.minitouch = _MiniTouchStream(device,port)
        self.get_screen_ratio()


    # 跟据输出显示大小和手机屏幕实际大小得出宽和高的比值
    def get_screen_ratio(self):
        self.screen_ratioX = (self.device.width / self.device.virtualscale) / config.OUT_SCREEN_SIZE[0]
        self.screen_ratioY = (self.device.height / self.device.virtualscale) /config.OUT_SCREEN_SIZE[1]


    def TouchEvent(self,buffer):
        str1 = buffer;
        strArry = str1.split(':');
        if len(strArry) < 2:
            return;
        type=strArry[0]
        xy=strArry[1]
        if type == '3':
            pnt = xy.split(',');
            #跟据输出显示大小和手机屏幕实际大小的比值，换算实际手机中的坐标
            X = int(float(pnt[0]))*self.screen_ratioX
            print("X:"+str(X))
            Y = int(float(pnt[1]))*self.screen_ratioY
            print("Y:"+str(Y))
            self.minitouch.TouchMove(X, Y);

        elif type == '1':
            pnt = xy.split(',');
            X = int(float(pnt[0]))*self.screen_ratioX
            Y = int(float(pnt[1]))*self.screen_ratioY
            self.minitouch.TouchDown(X, Y);

        elif type == "2":
            self.minitouch.TouchUp();
        elif type == "4":
            self.minitouch.ClickKeycode(xy,self.device_id);