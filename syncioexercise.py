# @File  : syncioexercise.py
# @Author: LiuXingsheng
# @Date  : 2020/12/29
# @Desc  :

import asyncio
import aiohttp
from aiohttp import FormData
import time
import os
import requests


def test():
    testpath = r'\\172.28.2.84\kf2share1\AIData\业务全链路\智慧小布\全链路-点问搜题\11月\PointAndAskFile\粗框图'
    url = 'http://pointquestion.eebbk.net/pointquestion-app/app/topicProcess/searchDifficultProblems'
    # url = 'http://47.112.238.105:8014/pointquestion-app/app/topicProcess/searchDifficultProblems'
    header = {'machineId': '700S593001AE5', 'accountId': '37511587', 'apkPackageName': 'com.eebbk.aisearch.fingerstyle',
              'apkVersionCode': '4040000', 'apkVersionName': 'V4.4.0.0', 'deviceModel': 'S5',
              'deviceOSVersion': 'V1.0.0_180409'}
    key = 'QuestionData20201119091946_489_217_700S5940013F0_material_PAAPhoto_70S5C08007836_PAAPhoto20201117120138_1001_1118_1566_2448_3264.jpg'
    with open(os.path.join(testpath,
                           key),
              'rb') as f:
        file = {'file': f.read()}
    ordx_y = key.split('_')
    t1 = time.time()
    for i in range(10):
        requests.post(url=url, headers=header, files=file,
                               params={'xPoint': ordx_y[-4], 'yPoint': ordx_y[-3], 'isLimitTimes': '0'})
    t2 = time.time()
    print('同步发送10个请求耗时',t2-t1)

def testpytHon():
    t1 = time.time()
    for i in range(10):
        requests.get(url='http://python.org')
    t2 = time.time()
    print(t2-t1)

async def fetch():
    t1 = time.time()
    for i in range(10):
        async with aiohttp.ClientSession() as session:
            async with session.get('http://python.org') as response:
                await response.text()
    t2 = time.time()
    print(t2-t1)


def test_123()->int:
    s = '123'
    d=  '456'
    return 1

Adict = {'code':'0001','msg':'success','data':'test'}
Atuple = (1,5,7)
Alist = [1,2,2,3]
Aset = {1,3,4}
Aset.add(5)
Aset.add(5)
Alist.append(3)



if __name__ == '__main__':
    print(test_123(),type(test_123()))
    print(Adict['code'])
    print(Atuple[1])
    print(Aset)
    print(Alist)

