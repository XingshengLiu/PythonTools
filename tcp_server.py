# @File  : tcp_server.py
# @Author: LiuXingsheng
# @Date  : 2019/1/5
# @Desc  :

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8888))
s.listen()
print('服务启动')

# 等待客户端连接
con,address = s.accept()
# 客户端连接成功打印
print(address)

# 从客户端接受数据
data = con.recv(1024)
print('从客户端接受消息：{0}'.format(data.decode()))

con.send('你好'.encode())

# 释放资源
con.close()
s.close()




