# @File  : upload_client.py
# @Author: LiuXingsheng
# @Date  : 2019/1/5
# @Desc  :

import socket

HOST = '127.0.0.1'
PORT = 8888

fileName = 'testclient.jpg'

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    with open(fileName, 'rb') as f:
        b = f.read()
        s.sendall(b)
        print('客户端上传数据完成')