# @File  : iter_interfaceTest.py
# @Author: LiuXingsheng
# @Date  : 2019/4/18
# @Desc  :

import requests, demjson

APP_STORE_ITEDOMAIN = 'http://test.eebbk.net/app-store-api'
APP_STORE_TESTDOMAIN = 'http://ite.eebbk.net/app-store-api-pad'
APP_STORE_FORMALDOMAIN = 'http://h600s.eebbk.net'
TESTDOMAIN = 'http://test.eebbk.net/terminalWorth'
terminalWorthDomain = 'https://terminalworth.eebbk.net/terminalWorth'


def getAllDeviceList():
    return [{'deviceModel': 'H8S', 'deviceOSVersion': 'V1.62'},
            {'deviceModel': 'H9', 'deviceOSVersion': 'V1.60'},
            {'deviceModel': 'S1', 'deviceOSVersion': 'V1.20'},
            {'deviceModel': 'S2', 'deviceOSVersion': 'V1.30'},
            {'deviceModel': 'S3', 'deviceOSVersion': 'V1.3.2_180302'},
            {'deviceModel': 'S1S', 'deviceOSVersion': 'V1.4.3'},
            {'deviceModel': 'H9S', 'deviceOSVersion': 'V1.3.0_180817'},
            {'deviceModel': 'H8SM', 'deviceOSVersion': 'V2.4.2_181012'},
            {'deviceModel': 'K5', 'deviceOSVersion': 'V1.4.3_180831'},
            {'deviceModel': 'H9A', 'deviceOSVersion': 'V1.2.1_181127'},
            {'deviceModel': 'H3000S', 'deviceOSVersion': 'V1.2.0_180818'},
            {'deviceModel': 'H5000', 'deviceOSVersion': 'V1.1.0_180830'},
            {'deviceModel': 'H8A', 'deviceOSVersion': 'V1.0.0_190223'}]


def getListByApkPackageNames(devceList):
    url = APP_STORE_FORMALDOMAIN + '/service/apkInfoTerminal/getListByApkPackageNames'
    print('自研应用------------------学习诊断')
    for item in devceList:
        item.update({'apkPackageNames': 'com.eebbk.leakfilling'})
        result = requests.get(url=url, params=item)
        print(result.text)
    print('自研应用------------------同步语文')
    for item in devceList:
        item.update({'apkPackageNames': 'com.eebbk.synchinese'})
        result = requests.get(url=url, params=item)
        print(result.text)
    print('三方应用------------------贝关怀')
    for item in devceList:
        item.update({'apkPackageNames': 'com.zontonec.ztkid'})
        result = requests.get(url=url, params=item)
        print(result.text)
    print('三方应用------------------悟空数学')
    for item in devceList:
        item.update({'apkPackageNames': 'air.com.gongfubb.wk123'})
        result = requests.get(url=url, params=item)
        print(result.text)


# -----------------------------------终端项目
def getAllProvinces():
    print('---------------------查询所有的省份-------------------')
    proviceList = []
    url = terminalWorthDomain + '/app/provinces/getAllProvinces'
    result = requests.get(url=url)
    info = demjson.decode(result.text)
    if info is None:
        assert False
    else:
        data = info['data']
        for item in data:
            proviceList.append(item['provinceId'])
    print(proviceList)
    return proviceList


def selectAllSellPointByProvinceId(provinceList):
    print('---------------------查询所有的售点信息-------------------')
    url = terminalWorthDomain + '/app/provinces/selectAllSellPointByProvinceId'
    for province in provinceList:
        result = requests.get(url=url, params={'provinceId': province})
        info = demjson.decode(result.text)
        if info is None:
            assert False
        else:
            data = info['data']
            # print(data)
            print('province id ：', province)
            if data is None:
                assert False
            else:
                pass


def getheader():
    return {'machineId': '700H38300018B', 'accountId': '4051922', 'apkPackageName': 'com.eebbk.askhomework',
            'apkVersionCode': '1.0.0', 'deviceModel': 'S3 Pro', 'deviceOSVersion': 'V1.0.0_180409'}


def getMoreStudyByGradeSubject():
    print('---------------------根据年纪+科目获取学习方案数据-------------------')
    paramList = []
    url = terminalWorthDomain + '/app/appinfo/getMoreStudyByGradeSubject'
    header = {'deviceModel': 'S3 Pro', 'deviceOSVersion': 'V1.00'}
    paramList.append({'gradeName': '三年级', 'subjectName': '数学'})
    paramList.append({'gradeName': '四年级', 'subjectName': '语文'})
    paramList.append({'gradeName': '五年级', 'subjectName': '英语'})
    for param in paramList:
        result = requests.get(url=url, params=param, headers=header)
        print(result.text)


def getHotQuestionByGrade():
    print('---------------------年级热点问题-------------------')
    gradeList = {'一年级', '二年级', '三年级', '四年级', '五年级', '六年级'}
    url = terminalWorthDomain + '/app/question/getHotQuestionByGrade'
    for grade in gradeList:
        result = requests.get(url=url, params={'gradeName': grade})
        print(result.text)


def getAnswerByVoiceResult():
    print('--------------------根据语音识别结果获取答案信息接口--------------------')
    url = terminalWorthDomain + '/app/question/getAnswerByVoiceResult'
    voiceList = []
    voiceList.append('北极星长什么样子')
    voiceList.append('ABAC式的词语')
    voiceList.append('一吨等于多少千克')
    voiceList.append('描写思乡的诗')
    for voice in voiceList:
        result = requests.get(url=url, params={'voiceResult': voice})
        print(result.text)


def main():
    # deviceList = getAllDeviceList()
    # getListByApkPackageNames(deviceList)
    provinceList = getAllProvinces()
    selectAllSellPointByProvinceId(provinceList)
    getMoreStudyByGradeSubject()
    getHotQuestionByGrade()
    getAnswerByVoiceResult()


if __name__ == '__main__':
    main()
