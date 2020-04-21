# @File  : mini_test.py
# @Author: LiuXingsheng
# @Date  : 2020/1/6
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import mini_testUrlset
import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.mini)


def getJFBookListByAttrGroup_test():
    url = manager.getDomain() + mini_testUrlset.MiniUrlSet['getJFBookListByAttrGroup']
    url = url + '?gradeId=5&subjectId=1&pressId=0&pageSize=10&nowPage=1&module=219&term=%E4%B8%8B%E5%86%8C'
    sendRequestAndPrint(url)


def getGradeBySubject():
    url = manager.getDomain() + mini_testUrlset.MiniUrlSet['getGradeBySubject']
    url = url + '?gradeType=2&module=&classId=&subjectId=4'
    sendRequestAndPrint(url)


def getGradeList():
    url = manager.getDomain() + mini_testUrlset.MiniUrlSet['getGradeList']
    url = url + '?gradeType=1&versionName=3.8.0.1&devicemodel=S3%20Pro&module=218&packageName=com.eebbk.syncenglish&machineId=700H38400163D&deviceosversion=V1.2.0_180809'
    sendRequestAndPrint(url)


def getNewAllBookListByAttrGroup():
    url = manager.getDomain() + mini_testUrlset.MiniUrlSet['getNewAllBookListByAttrGroup']
    url = url + '?gradeType=1&gradeId=1&subjectId=1&pressId=44&pageSize=10&nowPage=1&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&module=219&term=%E4%B8%8B%E5%86%8C'
    sendRequestAndPrint(url)


def getBookListByModuleNew():
    url = manager.getDomain() + mini_testUrlset.MiniUrlSet['getBookListByModuleNew']
    url = url + '?devicemodel=S3%20Pro&versionName=3.8.0.1&gradeId=3&subjectId=3&packageName=com.eebbk.syncenglish&deviceosversion=V1.2.0_180809&pressId=12&keyword=&nowPage=1&module=218&machineId=700H38400163D'
    sendRequestAndPrint(url)


def getSubjectForSifting():
    url = manager.getDomain() + mini_testUrlset.MiniUrlSet['getSubjectForSifting']
    url = url + '?gradeId=3&devicemodel=S3%20Pro&versionName=3.8.0.1&gradeType=1&packageName=com.eebbk.syncenglish&deviceosversion=V1.2.0_180809&istb=false&module=218&machineId=700H38400163D'
    sendRequestAndPrint(url)


def getAllBookListByPress():
    url = manager.getDomain() + mini_testUrlset.MiniUrlSet['getAllBookListByPress']
    url = url + '?gradeType=1&nowPage=1&subjectId=1&module=219&pressId=12'
    sendRequestAndPrint(url)


def getPressForSifting():
    url = getUrl('getPressForSifting')
    url = url + '?gradeId=3&devicemodel=S3%20Pro&versionName=3.8.0.1&gradeType=1&subjectId=3&packageName=com.eebbk.syncenglish&deviceosversion=V1.2.0_180809&istb=false&module=218&machineId=700H38400163D'
    sendRequestAndPrint(url)


def getPressBySubject():
    url = getUrl('getPressBySubject')
    url = url + '?gradeType=1&versionName=6.10.0.0&devicemodel=S3%20Pro&subjectId=1&packageName=com.eebbk.synchinese&deviceosversion=V1.2.0_180809&istb=true&module=219&machineId=700H38400163D'
    sendRequestAndPrint(url)


def getDianduBookListByAttrGroup():
    url = getUrl('getDianduBookListByAttrGroup')
    url = url + '?gradeId=4&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&module=219&gradeType=1&pageSize=10&pressId=12&subjectId=1&nowPage=1'
    sendRequestAndPrint(url)


def getBookInfo():
    url = getUrl('getBookInfo')
    url = url + '?IMEI=000H3000S0000326&devicemodel=S3%20Pro&versionName=2.5.1.1&apkVersionCode=100&title=%5B%E4%BA%BA%E6%95%99%E7%89%88%5D%E6%95%B0%E5%AD%A6%E5%85%AD%E4%B8%8A_%E5%9C%86%E7%9A%84%E8%AE%A4%E8%AF%86%E5%92%8C%E7%94%A8%E5%9C%86%E8%A7%84%E7%94%BB%E5%9C%86%E7%9A%84%E6%96%B9%E6%B3%95(V2.0).avi&packageName=com.eebbk.synmath&deviceOSVersion=V1.3.2_190216&apkPackageName=com.eebbk.synmath&deviceosversion=V1.3.2_190216&deviceModel=S3%20Pro&apkVersionName=2.5.1.1&machineId=H3000S0000326'
    sendRequestAndPrint(url)


def getAllBookListByAttrGroup():
    url = getUrl('getAllBookListByAttrGroup')
    url = url + '?gradeId=1&province=%E5%B9%BF%E4%B8%9C%E7%9C%81&module=219&gradeType=1&pageSize=10&pressId=12&term=%E4%B8%8B%E5%86%8C&subjectId=1&nowPage=1'
    sendRequestAndPrint(url)


def getBookListByAttrGroup():
    url = getUrl('getBookListByAttrGroup')
    url = url + '?gradeId=4&nowPage=1&subjectId=1&module=219&pressId=12&term=%E4%B8%8B%E5%86%8C'
    sendRequestAndPrint(url)


def getUrl(itemName):
    return manager.getDomain() + mini_testUrlset.MiniUrlSet[str(itemName)]


def sendRequestAndPrint(url):
    print('--------------------------------------------')
    print(url)
    result = requests.get(url)
    print(result.text)


def getSchoolInfoByType(districtlist):
    nulllist = []
    url = getUrl('getSchoolInfoByType')
    print(url)
    for id in districtlist:
        result = requests.get(url=url, params={'type': '2', 'areaId': str(id)})
        objdata = demjson.decode(result.text)
        if objdata:
            for item in objdata['schoolList']:
                if item['id'] and judgeType2(item['type']):
                    pass
                else:
                    nulllist.append((item['areaId'], item['name']))
    print('空id的学校有', nulllist)


def judgeType2(num):
    if num == 2 or num == 3 or num == 4 or num == 5 or num == 6 or num == 7:
        return True
    else:
        return False


def judgeType1(num):
    if num == 1 or num == 7:
        return True
    else:
        return False


def getAllMessage():
    nulllist = []
    districtlist = []
    url = getUrl('getAllMessage')
    print(url)
    result = requests.get(url=url)
    objdata = demjson.decode(result.text)
    if objdata['provinces']:
        for item in objdata['provinces']:
            for item1 in item['cities']:
                if item1['resId']:
                    districtlist.append(item1['resId'])
                else:
                    nulllist.append(item1['cityName'])
    print('空的城市名', nulllist)
    return districtlist


def test():
    url = getUrl('getSchoolInfoByType')
    result = requests.get(url=url, params={'type': '1', 'areaId': '1020012'})
    print(result.text)


if __name__ == '__main__':
    # getJFBookListByAttrGroup_test()  # 正式环境比测试环境少了一部分数据
    # getGradeBySubject()
    # getGradeList()
    # getNewAllBookListByAttrGroup() # 测试环境有数据 正式环境无数据
    # getBookListByModuleNew()   # 正式环境比测试环境少了一部分数据
    # getSubjectForSifting()
    # getAllBookListByPress()    # 正式环境测试环境同本书 文件大小不一样
    # getPressForSifting()
    # getPressBySubject()
    # # getDianduBookListByAttrGroup()
    # getBookInfo()
    # getAllBookListByAttrGroup() # 资源文件大小不一样 测试153M 正式155M
    # getBookListByAttrGroup() # 资源文件 测试环境139M  正式环境137M
    # getSchoolInfoByType()
    districtlist = getAllMessage()
    getSchoolInfoByType(districtlist)
    # test()
