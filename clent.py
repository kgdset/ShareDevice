#!/usr/bin/python3
# 文件名：client.py

# 导入 socket、sys 模块
import socket
import threading
import time
from Main import DeviceMonitor
devicemonitor=DeviceMonitor._DeviceMonitor()
t=threading.Thread(target=devicemonitor.DeviceMonitor_start,name='getdevices')
t.start()
time.sleep(5)
while True:
    time.sleep(1)
    # 创建 socket 对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    # 设置端口好
    port = 9999
    # 连接服务，指定主机和端口

    s.connect((host, port))
    msg1 = str(devicemonitor.DEVICES_LIST)
    s.send(msg1.encode('utf-8'))
    s.close()


