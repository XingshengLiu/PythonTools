# @File  : count.py
# @Author: LiuXingsheng
# @Date  : 2018/7/21
# @Desc  : 实现简单计算器
import requests


class Calculator():
    def __init__(self, a, b):
        self.a = int(a)
        self.b = int(b)

    def add(self):
        return self.a + self.b

    def sub(self):
        return self.a - self.b

    def mul(self):
        return self.a * self.b

    def div(self):
        return self.a / self.b


def print_url(r):
    print(r.url)


hooks = dict(response=print_url)

url = 'http://wisdomdesktop.eebbk.net' + '/app/recommendVideo/getVideoTraningData'
header = {'machineId': '700H384001DDU', 'deviceModel': 'S3 Pro'}  # 四年级
result = requests.get(url=url, headers=header,hooks=dict(response=print_url))
