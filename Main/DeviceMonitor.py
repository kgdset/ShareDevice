import time

from Android.ADB import AdbTools
class _DeviceMonitor():
    DEVICES_LIST = {}
    Is_Update=False
    Is_first=True
    devicelist=[]
    old_devicelist=[]
    def getDeviceList(self):
        while True:

            self.devicelist= AdbTools().get_devices()
            #print(self.devicelist)
            if len(self.devicelist)>0:
                if self.Is_first:
                    self.old_devicelist=self.devicelist
                if self.devicelist!=self.old_devicelist or self.Is_first:
                    self.old_devicelist=self.devicelist
                    self.DEVICES_LIST.clear()
                    self.DEVICES_LIST['IsUpdate'] = True
                    for i in self.devicelist:
                        print(i)
                        model=AdbTools(i).get_device_model()
                        version=AdbTools(i).get_device_android_version()
                        screen_size=AdbTools(i).get_screen_normal_size()
                        DEVICES_DETAILS_LIST={'model':model,'version':version,'screen_size':screen_size}
                        self.DEVICES_LIST[i]=DEVICES_DETAILS_LIST

                else:
                    self.DEVICES_LIST['IsUpdate']=False
            else:
                self.DEVICES_LIST.clear()
            self.Is_first = False
            time.sleep(5)



    def DeviceMonitor_start(self):
        self.getDeviceList()


