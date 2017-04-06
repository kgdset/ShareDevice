import socket
host=''
port=51234
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen(1)

y=b"""HTTP/1.0 200 OK


hello world


://www.baidu.com">baidu
"""
while 1:
  clientsock,clientaddr = s.accept()
  #process the connection
  print ("Got connection from", clientsock.getpeername())
  data = clientsock.recv(4096)
  n=clientsock.send(y)
  clientsock.close()