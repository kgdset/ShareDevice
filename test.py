#!/usr/bin/python3
# 文件名：server.py

# 导入 socket、sys 模块
import socket
import sys
DEVICES_LIST={}
def getDeviceListAll():
    # 创建 socket 对象
    serversocket = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()

    port = 9999

    # 绑定端口
    serversocket.bind((host, port))

    # 设置最大连接数，超过后排队
    serversocket.listen(5)

    while True:
        # 建立客户端连接
        clientsocket, addr = serversocket.accept()
        host=addr[0]
        print(host)
        #print("连接地址: %s" % str(addr))
        msg = clientsocket.recv(4096).decode('utf-8')
        DEVICES_LIST[host]=eval(msg)
        print(DEVICES_LIST)
        # msg = '欢迎访问菜鸟教程！' + "\r\n"
        clientsocket.send(msg.encode('utf-8'))
        clientsocket.close()
getDeviceListAll()