# @File  : wisdomdestop_test.py
# @Author: LiuXingsheng
# @Date  : 2020/3/17
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import wisdomdesktop_testUrlSet
from InterfaceStructure.resources import requestheaders
import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.TestDomainType_Asia)
manager.setItemName(constants.wisdomdesktop)


def getIndexScreensaver():
    url = manager.getDomain() + wisdomdesktop_testUrlSet.UrlSet['getIndexScreensaver']
    print(url)
    result = requests.get(url=url)
    print(result.text)
    nonvlist = []
    objtdata = demjson.decode(result.text)
    if objtdata['data']:
        if len(objtdata['data']['screensaver']) == 30 :
            print('锁屏数据为30个单词')
            for item in objtdata['data']['screensaver']:
                for item_1 in item['englishWordExtendVos']:
                    if item_1['partSpeech'] == "n.":
                        pass
                    else:
                        nonvlist.append(item['word'])
        else:
            print('锁屏数据异常，数量为', len(objtdata['data']['screensaver']))
    print('非名词数据',nonvlist)


def getSynChineseWordGrades():
    url = manager.getDomain() + wisdomdesktop_testUrlSet.UrlSet['getSynChineseWordGrades']
    print(url)
    paramlist = [{'machineId': '700S593001AE5', 'grade': '三年级', 'pageNum': 1, 'pageSize': 10},
                 {'machineId': '700S593001AE5', 'grade': '二年级', 'pageNum': 1, 'pageSize': 5},
                 {'machineId': '700S593001AE5', 'grade': '一年级', 'pageNum': 2, 'pageSize': 5},
                 {'machineId': '700S593001AE5', 'grade': '四年级', 'pageNum': 3, 'pageSize': 5},
                 {'machineId': '700S593001AE5', 'grade': '五年级', 'pageNum': 1, 'pageSize': 5},
                 {'machineId': '700S593001AE5', 'grade': '六年级', 'pageNum': 1, 'pageSize': 5}]
    for param in paramlist:
        result = requests.get(url=url, params=param)
        objdata = demjson.decode(result.text)
        if objdata['data']:
            if objdata['data']['currentPage'] == param['pageNum'] and objdata['data']['pageSize'] == param['pageSize'] \
                    and len(objdata['data']['recordList']) == param['pageSize']:
                print('当前页及数量均正常')
            else:
                print('数据异常', param, '返回：', objdata)


def getSynEnglishWordGrades():
    url = manager.getDomain() + wisdomdesktop_testUrlSet.UrlSet['getSynEnglishWordGrades']
    print(url)
    paramlist = [{'machineId': '700S593001AE5', 'grade': '三年级', 'pageNum': 1, 'pageSize': 10},
                 {'machineId': '700S593001AE5', 'grade': '二年级', 'pageNum': 1, 'pageSize': 5},
                 {'machineId': '700S593001AE5', 'grade': '一年级', 'pageNum': 2, 'pageSize': 5},
                 {'machineId': '700S593001AE5', 'grade': '四年级', 'pageNum': 3, 'pageSize': 5},
                 {'machineId': '700S593001AE5', 'grade': '五年级', 'pageNum': 1, 'pageSize': 5},
                 {'machineId': '700S593001AE5', 'grade': '六年级', 'pageNum': 1, 'pageSize': 5}]
    for param in paramlist:
        result = requests.get(url=url, params=param)
        objdata = demjson.decode(result.text)
        if objdata['data']:
            if objdata['data']['currentPage'] == param['pageNum'] and objdata['data']['pageSize'] == param['pageSize'] \
                    and len(objdata['data']['recordList']) == param['pageSize']:
                print('当前页及数量均正常')
                print(objdata)
            else:
                print('数据异常', param, '返回：', result.text)


def myCourse():
    url = manager.getDomain() + wisdomdesktop_testUrlSet.UrlSet['myCourse']
    print(url)
    contentlist = []
    for num in [2, 3, 4, 5, 6]:
        params = {'accountId': '700S593001AE5', 'machineId': '700S593001AE5', 'deviceosversion': 'V1.2.0_190822',
                  'count': str(num), 'packageName': 'com.eebbk.vtraining', 'versionName': '2.5.0.0',
                  'userId': '700S593001AE5',
                  'versionCode': '2050000', 'direction': 'down', 'devicemodel': 'S5'}
        result = requests.get(url=url, params=params)
        if result.status_code == 200:
            objdata = demjson.decode(result.text)
            if objdata['resultData']:
                if num == len(objdata['resultData']):
                    print('传入获取课程数量与预期一致')
                    if num == 6:
                        for item in objdata['resultData']:
                            contentlist.append((item['coursePackageId'], item['putAwayTime']))
                    else:
                        pass
                else:
                    print('传入数量不一致', num, len(objdata['resultData']))
                    print(result.text)
        else:
            print('请求异常')
    return contentlist


def singleCourseCatalog(contentlist):
    url = manager.getDomain() + wisdomdesktop_testUrlSet.UrlSet['singleCourseCatalog']
    print(url)
    nulllist = []
    for item in contentlist:
        param = {'putAwayTime': item[1], 'coursePackageId': item[0], 'accountId': '700S593001AE5',
                 'machineId': '700S593001AE5', 'deviceosversion': 'V1.2.0_190822',
                 'packageName': 'com.eebbk.vtraining',
                 'versionName': '2.5.0.0', 'userId': '700S593001AE5', 'versionCode': '2050000', 'devicemodel': 'S5'}
        result = requests.get(url=url, params=param)
        objdata = demjson.decode(result.text)
        if objdata['resultData']:
            for item in objdata['resultData']:
                if item['id'] and item['name']:
                    pass
                else:
                    nulllist.append(item[1])
    print('无id或课程名为空的coursepackage id 有', nulllist)


def getSupendedAdvertising():
    url = manager.getDomain() + wisdomdesktop_testUrlSet.UrlSet['getSupendedAdvertising']
    print(url)
    result = requests.get(url=url)
    print(result.text)


if __name__ == '__main__':
    getIndexScreensaver()
    # getSynChineseWordGrades()
    # getSynEnglishWordGrades()
    contentlist = myCourse()
    singleCourseCatalog(contentlist)
    getSupendedAdvertising()
