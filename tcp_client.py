# @File  : tcp_client.py
# @Author: LiuXingsheng
# @Date  : 2019/1/5
# @Desc  :

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8888))

s.send(b'hello')
data = s.recv(1024)
print('从服务器接收消息：{0}'.format(data.decode()))

s.close()
