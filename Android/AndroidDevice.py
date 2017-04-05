# coding:utf-8
from Android import ADB
import re
adb1 = ADB.AdbTools()
class AndroidDevice():
    width=0;
    height=0;
    virtualwidth=0;
    virtualheight=0;
    virtualscale='';
    orientation='';
    sdk='';
    abi=''

    MINICAP_FILE_PATH='';
    MINICAPSO_FILE_PATH='';
    MINITOUCH_FILE_PATH='';
    MINICAP_DEVICE_PATH = "/data/local/tmp";
    PUSH_COMMAND = "push";
    GET_SIZE_COMMAND = "shell dumpsys window windows | grep mScreenRect";
    GET_DEVICE_ABI_COMMAND = "shell getprop ro.product.cpu.abi";
    GET_DEVICE_SDK_COMMAND = "shell getprop ro.build.version.sdk";
    minicapport = 1313;
    minitouchport = 1111;

    def  Height(self):
        return self.height;

    def Width(self):
        return self.width;

    def  Abi(self):
        return self.abi;

    def SDK(self):
        self.sdk;

    def MINICAP_PORT(self):
        self.minicapport;


    def VirtualWidth(self):
        self.virtualwidth;

    def VirtualHeight(self):
        self.virtualheight;

    def Scale(self):
        self.virtualscale;
    def setScale(self,value):
        self.virtualscale = value;
        self.GetScreenSize();

    def Orientation(self):
        self.orientation;

    def setOrientation(self,value):
        orientation = value;

    def AndroidDevice(self):
        self.InitDeviceInfo();
        self.PushFile();

    def PushFile(self):
        self.PushMinicapFiles();
        self.PushMiniTouchFiles();
        self.PushMiniTouchFiles();

    def InitDeviceInfo(self):
        self.abi = self.GetABI().Trim();
        self.sdk = self.GetSdkVersion().Trim();
        self.MINICAP_FILE_PATH = str.Format("Lib/minicap/bin/{0}/minicap", self.abi);
        self.MINICAPSO_FILE_PATH = str.Format("Lib/minicap/shared/android-{0}/{1}/minicap.so", self.sdk, self.abi);
        self.MINITOUCH_FILE_PATH = str.Format("Lib/minitouch/{0}/minitouch", self.abi);

        def pushFile(self,localpath,devicepath):
            command = str.Format("{0} {1} {2}", self.PUSH_COMMAND, localpath, devicepath);
            self.ExecuteAdbCommand(command);

        def ExecuteAdbCommand(self,command):
            return adb1.adb(command);

        def GetScreenSize(self):

            result = ExecuteAdbCommand(self.GET_SIZE_COMMAND);
            match = re.match("\d{3,4}\,\d{3,4}",result)
            size = match.Groups[0].Value;
            width = int(size.Split(',').ToArray()[0]);
            height = int(size.Split(',').ToArray()[1]);
            virtualwidth = width * (height / self.virtualscale) / height;
            virtualheight = height / self.virtualscale;

        def GetABI(self):
            return ExecuteAdbCommand(self.GET_DEVICE_ABI_COMMAND);


        def GetSdkVersion(self):
            return ExecuteAdbCommand(self.GET_DEVICE_SDK_COMMAND);


        def PushMinicapFiles(self):
            pushFile(self.MINICAP_FILE_PATH, self.MINICAP_DEVICE_PATH);
            pushFile(self.MINICAPSO_FILE_PATH, self.MINICAP_DEVICE_PATH);
            command = str.format("shell chmod 777 {0}/minicap", self.MINICAP_DEVICE_PATH)
            ExecuteAdbCommand(command);

        def StartMinicapServer(self):
            command = str.format("forward tcp:{0} localabstract:minicap", self.minicapport);
            ExecuteAdbCommand(command);
            command = str.format("shell LD_LIBRARY_PATH={0} /data/local/tmp/minicap -P {1}x{2}@{3}x{4}/{5}",
                                 self.MINICAP_DEVICE_PATH, self.width, self.height, self.virtualwidth, self.virtualheight, self.orientation);
            ExecuteAdbCommand(command);


        def PushMiniTouchFiles(self):
            pushFile(self.MINITOUCH_FILE_PATH, self.MINICAP_DEVICE_PATH);
            command = str.format("shell chmod 777 {0}/minitouch", self.MINICAP_DEVICE_PATH);
            ExecuteAdbCommand(command);

        def StartMiniTouchServer(self):
            command = str.format("forward tcp:{0} localabstract:minitouch", self.minitouchport);
            ExecuteAdbCommand(command);
            command = str.format("shell {0}/minitouch", self.MINICAP_DEVICE_PATH, self.width, self.height, self.virtualwidth, self.virtualheight, 0);
            ExecuteAdbCommand(command);

