# coding:utf-8
import os

from Android import ADB
import re

class _AndroidDevice():
    width=0;
    height=0;
    virtualwidth=0;
    virtualheight=0;
    virtualscale='';
    orientation='';
    sdk='';
    abi=''
    #os.chdir("../")
    lib_path=os.getcwd()+'\\'
    print(lib_path)
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

    def __init__(self,device_id='', minicapport = 1313,minitouchport = 1111):
        self.adb1 = ADB.AdbTools(device_id)
        self.minicapport=minicapport
        self.minitouchport=minitouchport
        self.InitDeviceInfo();
        self.PushFile();

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
        self.orientation = value;



    def ExecuteAdbCommand(self, command):

        return self.adb1.adb(command);

    def GetScreenSize(self):
        result = self.adb1.get_screen_normal_size();
        self.width = int(result[0]);
        self.height = int(result[1]);
        self.virtualwidth = int(self.width * (self.height / self.virtualscale) / self.height);
        self.virtualheight = int(self.height / self.virtualscale);

    def GetABI(self):
        return self.ExecuteAdbCommand(self.GET_DEVICE_ABI_COMMAND);

    def GetSdkVersion(self):
        return self.ExecuteAdbCommand(self.GET_DEVICE_SDK_COMMAND);
    def PushFile(self):
        self.PushMinicapFiles();
        self.PushMiniTouchFiles();
        self.PushMiniTouchFiles();

    def pushFile(self,localpath, devicepath):
        command = str.format("{0} {1} {2}", self.PUSH_COMMAND, localpath, devicepath);
        self.ExecuteAdbCommand(command);

    def PushMinicapFiles(self):
        self.pushFile(self.MINICAP_FILE_PATH, self.MINICAP_DEVICE_PATH);
        self.pushFile(self.MINICAPSO_FILE_PATH, self.MINICAP_DEVICE_PATH);
        command = str.format("shell chmod 777 {0}/minicap", self.MINICAP_DEVICE_PATH)
        self.ExecuteAdbCommand(command);

    def StartMinicapServer(self):
        print('Start MinicapServer')
        command = str.format("forward tcp:{0} localabstract:minicap", self.minicapport);
        self.ExecuteAdbCommand(command);
        command = str.format("shell LD_LIBRARY_PATH={0} /data/local/tmp/minicap -P {1}x{2}@{3}x{4}/{5}",
                             self.MINICAP_DEVICE_PATH, self.width, self.height, self.virtualwidth, self.virtualheight,
                             self.orientation);
        self.ExecuteAdbCommand(command);

    def PushMiniTouchFiles(self):
        self.pushFile(self.MINITOUCH_FILE_PATH, self.MINICAP_DEVICE_PATH);
        command = str.format("shell chmod 777 {0}/minitouch", self.MINICAP_DEVICE_PATH);
        self.ExecuteAdbCommand(command);

    def StartMiniTouchServer(self):
        print('Start MiniTouchServer')
        command = str.format("forward tcp:{0} localabstract:minitouch", self.minitouchport);
        self.ExecuteAdbCommand(command);
        command = str.format("shell {0}/minitouch", self.MINICAP_DEVICE_PATH, self.width, self.height,
                             self.virtualwidth, self.virtualheight, 0);
        self.ExecuteAdbCommand(command);


    def InitDeviceInfo(self):

        self.abi = self.GetABI();
        self.sdk = self.GetSdkVersion().strip();
        print(self.abi)
        self.MINICAP_FILE_PATH = str.format("Lib/minicap/bin/{0}/minicap", self.abi);
        self.MINICAPSO_FILE_PATH = str.format("Lib/minicap/shared/android-{0}/{1}/minicap.so", self.sdk, self.abi);
        self.MINITOUCH_FILE_PATH = str.format("Lib/minitouch/{0}/minitouch", self.abi);

        def pushFile(self,localpath,devicepath):
            command = str.format("{0} {1} {2}", self.PUSH_COMMAND, localpath, devicepath);
            self.ExecuteAdbCommand(command);





