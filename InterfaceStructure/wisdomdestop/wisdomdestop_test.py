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
    result = requests.get(url=url, headers=requestheaders.askhomework_header)
    print(result.text)
    nonvlist = []
    objtdata = demjson.decode(result.text)
    if objtdata['data']:
        if len(objtdata['data']['screensaver']) == 30:
            print('锁屏数据为30个单词')
            for item in objtdata['data']['screensaver']:
                for item_1 in item['englishWordExtendVos']:
                    if item_1['partSpeech'] == "n.":
                        pass
                    else:
                        nonvlist.append(item['word'])
        else:
            print('锁屏数据异常，数量为', len(objtdata['data']['screensaver']))
    print('非名词数据', nonvlist)


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
        result = requests.get(url=url, params=param, headers=requestheaders.askhomework_header)
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
        result = requests.get(url=url, params=param, headers=requestheaders.askhomework_header)
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
        result = requests.get(url=url, params=params, headers=requestheaders.askhomework_header)
        print(result.text)
        if result.status_code == 200:
            objdata = demjson.decode(result.text)
            if objdata['resultData']:
                if num == len(objdata['resultData']):
                    print('传入获取课程数量与预期一致')
                    if num == 4:
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
        result = requests.get(url=url, params=param, headers=requestheaders.askhomework_header)
        print(result.text)
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
    result = requests.get(url=url, headers=requestheaders.askhomework_header)
    print(result.text)


def coursePackageById(contentlist):
    flag = 1
    url = manager.getDomain() + wisdomdesktop_testUrlSet.UrlSet['coursePackageById']
    print(url)
    nulllist = []
    resoucenulllist = []
    for item in contentlist:
        param = {'putAwayTime': item[1], 'coursePackageId': item[0], 'accountId': '700S593001AE5',
                 'machineId': '700S593001AE5', 'deviceosversion': 'V1.2.0_190822',
                 'packageName': 'com.eebbk.vtraining',
                 'versionName': '2.5.0.0', 'userId': '700S593001AE5', 'versionCode': '2050000', 'devicemodel': 'S5'}
        result = requests.get(url=url, params=param, headers=requestheaders.askhomework_header)
        objdata = demjson.decode(result.text)
        if objdata['resultData']:
            if objdata['resultData']['backupCoursePackageCoverUrl'] and objdata['resultData']['coursePackageCoverUrl']:
                if objdata['resultData']['teacherList']:
                    for teacher in objdata['resultData']['teacherList']:
                        if teacher['videoUrl'] and teacher['imageUrl'] and teacher['imageUrlHD']:
                            pass
                        else:
                            print(item, '教师资料异常')
                            flag = 0
                else:
                    print(item, '教师列表为空')
                    flag = 0
            else:
                flag = 0
                resoucenulllist.append(item[0])
        else:
            flag = 0
            nulllist.append(item)
    if flag:
        print(contentlist, '上述id相关资源均正常返回')
    else:
        print('请求为空 或 资源为空的id为', nulllist, resoucenulllist)


def coursePackageStudyResults():
    url = manager.getDomain() + wisdomdesktop_testUrlSet.UrlSet['coursePackageStudyResults']
    print(url)
    params = {'putAwayTime': '', 'accountId': '700S593001AE5', 'machineId': '700S593001AE5', 'coursePackageId': '1061',
              'deviceosversion': 'V1.0.0_200414', 'packageName': 'com.eebbk.vtraining', 'versionName': '2.4.0.0',
              'userId': '700S593001AE5', 'versionCode': '2040000', 'devicemodel': 'S5'}
    result = requests.get(url=url, params=params, headers=requestheaders.askhomework_header)
    print(result.text)

def test():
    url = 'http://testaliyun.eebbk.net/wrongdiagnosis/api/print/previewPrint'
    params = {"accountId":"VA700S620041208","chooseAll":False,"machineId":"700S620041208",
              "printDetail":[{"choose":True,"collectionId":91220,"similarIds":"130983"},{"choose":True,"collectionId":91219},{"choose":True,"collectionId":91218,"similarIds":"130977"},{"choose":True,"collectionId":91217},{"choose":True,"collectionId":91216,"similarIds":"130971,130972"},{"choose":True,"collectionId":91215,"similarIds":"130968,130969,130970"},{"choose":True,"collectionId":91214,"similarIds":"130965,130967"},{"choose":True,"collectionId":91213,"similarIds":"130963,130964"},{"choose":True,"collectionId":91212,"similarIds":"130959,130960,130961"},{"choose":True,"collectionId":91210,"similarIds":"130953"},{"choose":True,"collectionId":90997},{"choose":True,"collectionId":90992},{"choose":True,"collectionId":79488,"similarIds":"100126"},{"choose":True,"collectionId":79487,"similarIds":"100121,100122"},{"choose":True,"collectionId":79484,"similarIds":"100115"},{"choose":True,"collectionId":79483},{"choose":True,"collectionId":79481},{"choose":True,"collectionId":79480},{"choose":True,"collectionId":79479,"similarIds":"100100,100101"},{"choose":True,"collectionId":79478,"similarIds":"100097"},{"choose":True,"collectionId":79474,"similarIds":"100088"},{"choose":True,"collectionId":79471,"similarIds":"100081,100082"},{"choose":True,"collectionId":79465},{"choose":True,"collectionId":79461},{"choose":True,"collectionId":79457},{"choose":True,"collectionId":79395,"similarIds":"99919"},{"choose":True,"collectionId":79377},{"choose":True,"collectionId":79376},{"choose":True,"collectionId":79373,"similarIds":"99851,99852"},{"choose":True,"collectionId":79370},{"choose":True,"collectionId":79365,"similarIds":"99832"},{"choose":True,"collectionId":79364},{"choose":True,"collectionId":79360},{"choose":True,"collectionId":79356},{"choose":True,"collectionId":79355,"similarIds":"99803"},{"choose":True,"collectionId":79353,"similarIds":"99801,99802"},{"choose":True,"collectionId":79352},{"choose":True,"collectionId":79347},{"choose":True,"collectionId":79346,"similarIds":"99780,99781,99782"},{"choose":True,"collectionId":79333,"similarIds":"99750"},{"choose":True,"collectionId":79331},{"choose":True,"collectionId":79327},{"choose":True,"collectionId":79323},{"choose":True,"collectionId":79321},{"choose":True,"collectionId":79319},{"choose":True,"collectionId":79314,"similarIds":"99698"},{"choose":True,"collectionId":79305},{"choose":True,"collectionId":79300},{"choose":True,"collectionId":79251,"similarIds":"99532"},{"choose":True,"collectionId":79248,"similarIds":"99524"},{"choose":True,"collectionId":79243,"similarIds":"99509,99510"},{"choose":True,"collectionId":79240},{"choose":False,"collectionId":79239,"similarIds":"99496"},{"choose":True,"collectionId":79237},{"choose":True,"collectionId":79233},{"choose":True,"collectionId":79231,"similarIds":"99475,99476"},{"choose":True,"collectionId":79230}]
              }
    result = requests.post(url=url,json=params,headers={'Content-Type': 'application/json'})
    print(result.text)

if __name__ == '__main__':
    # getIndexScreensaver()
    # getSynChineseWordGrades()
    # getSynEnglishWordGrades()
    contentlist = myCourse()
    singleCourseCatalog(contentlist)
    getSupendedAdvertising()
    coursePackageById(contentlist)
    coursePackageStudyResults()
    # test()
