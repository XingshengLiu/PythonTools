# @File  : pointquestion_test.py
# @Author: LiuXingsheng
# @Date  : 2020/4/21
# @Desc  : 因电脑事故之前的脚本被重启后恢复掉了，TMD

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import pointquestion_testUrlSet
from InterfaceStructure.resources import requestheaders
import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.AlphaDomainType)
manager.setItemName(constants.pointquestion)
Type = 'Normal'


def searchDifficultProblems():
    url = manager.getDomain() + pointquestion_testUrlSet.PointquestionUrlSet['searchDifficultProblems']
    print(url)
    with open('../resources/FingerData3208407_0_367_217_2448_3264.jpg', 'rb')as f:
        file = {'file': f.read()}
        requestheaders.askhomework_header.update({'apkPackageName': 'com.eebbk.aisearch.fingerstyle'})
        result = requests.post(url=url, params={'xPoint': '367', 'yPoint': '217', 'isLimitTimes': '0'}, files=file,
                               headers=requestheaders.askhomework_header)
        if Type == 'Normal':
            objdata = demjson.decode(result.text)
            if objdata['data']:
                if objdata['data']['questions'] and objdata['data']['questionListId']:
                    print('搜题无异常')
                else:
                    print('题目或搜题结果未返回')
        else:
            print(result.text)


def topicProcess():
    url = manager.getDomain() + pointquestion_testUrlSet.PointquestionUrlSet['topicProcess']
    print(url)
    with open('../resources/FingerData3208407_0_367_217_2448_3264.jpg', 'rb')as f:
        file = {'file': f.read()}
        requestheaders.askhomework_header.update({'apkPackageName': 'com.eebbk.aisearch.fingerstyle'})
        result = requests.post(url=url,
                               params={'xPoint': '367', 'yPoint': '217', 'isLimitTimes': '0', 'yunfuVersion': '1'},
                               files=file,
                               headers=requestheaders.askhomework_header)
        if Type == 'Normal':
            objdata = demjson.decode(result.text)
            if objdata['data']:
                if objdata['data']['topicObject']['questions'] and objdata['data']['topicObject']['questionListId']:
                    print('搜题无异常')
                else:
                    print('题目或搜题结果未返回')
        else:
            print(result.text)


def getNewOcrGrayByModel():
    url = manager.getDomain() + pointquestion_testUrlSet.PointquestionUrlSet['getNewOcrGrayByModel']
    print(url)
    modellist = ['S6', 'S3 Prow', 'S1W', 'V100', 'S3 Pro', 'S5']
    for model in modellist:
        result = requests.get(url=url,
                              params={'deviceModel': model}, headers=requestheaders.askhomework_header)
        objdata = demjson.decode(result.text)
        print(model, objdata['data'])


def addNewOcrGrayMachineId(machineId):
    url = manager.getDomain() + pointquestion_testUrlSet.PointquestionUrlSet['addNewOcrGrayMachineId']
    print(url)
    result = requests.post(url=url,
                           params={'machineId': machineId, 'deviceModel': 'S5', 'apkVersionName': '4.2.1.1',
                                   'apkVersionCode': '40201010'}, headers=requestheaders.askhomework_header)
    print(result.text)


def getNewOcrGrayByMachineId(machineId):
    url = manager.getDomain() + pointquestion_testUrlSet.PointquestionUrlSet['getNewOcrGrayByMachineId']
    print(url)
    result = requests.get(url=url,
                          params={'machineId': machineId, 'deviceModel': 'S5', 'apkVersionName': '4.2.1.1',
                                  'apkVersionCode': '40201010'}, headers=requestheaders.askhomework_header)
    objdata = demjson.decode(result.text)
    if objdata['data'] == machineId:
        print('已正常添加')
    else:
        print('添加失败')


if __name__ == '__main__':
    machineId = '700S593001AE5'
    # getNewOcrGrayByModel()
    addNewOcrGrayMachineId(machineId)
    getNewOcrGrayByMachineId(machineId)
    # searchDifficultProblems()
    # topicProcess()
