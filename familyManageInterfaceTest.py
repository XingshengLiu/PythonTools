# @File  : familyManageInterfaceTest.py
# @Author: LiuXingsheng
# @Date  : 2018/10/19
# @Desc  : 家长管理接口拨测

import requests, time
import http_common

# 账号token
ACCESS_TOKEN = 'eyJhY2NvdW50IjoiMTg1NzYzNzAxMDYiLCJhY2NvdW50SWQiOiIzMDYwOSIsIm1hY2hpbmVJZCI6IjhhMjQ0ZDNlIiwiY3JlYXRlVGltZSI6MTU1MjEwNDI3NTg1NH0'

# 正式环境域名
REQUEST_DOMAIN = "http://assistant-pad.eebbk.net"

# 集成环境域名
# REQUEST_DOMAIN = "http://assistant-pad.alpha.eebbk.net"

# 测试环境域名
# REQUEST_DOMAIN = "http://test.eebbk.net/assistant-pad"


# 获取时间戳
def getTimestamp():
    t = time.time()
    cur_time = int(t)
    time_local = time.localtime(cur_time)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return str(dt)


# 通用请求头
def getHeader(timestamp):
    requestHeader = {'accountId': '2306881', 'apkPackageName': 'com.eebbk.parentalcontrol', 'apkVersionCode': '2200',
                     'deviceModel': 'Redmi Note 4X',
                     'deviceOSVersion': 'V9.5.1.0.NCFCNFA', 'machineId': '9e1b9b0f0804', 'padDeviceModel': 'S3 Pro',
                     'padMachineId': '700H38400163D', 'timestamp': timestamp}
    return requestHeader


# 通用参数
def getParams(timestamp):
    requestParams = {'machineId': '700H38300018B', 'phoneModel': 'xiaomi-Redmi Note 4X',
                     'phoneSysver': 'V9.5.1.0.NCFCNFA', 'appId': 'com.eebbk.parentalcontrol', 'appVer': '2.200',
                     'phoneId': '9e1b9b0f0804',
                     'token': ACCESS_TOKEN, 'timestamp': timestamp}
    return requestParams


# 生成MD5加密串
def getMD5Str(url, param):
    md5 = http_common.get_md5_for_request(url, param)
    signDict = {"sign": md5}
    return signDict


def getInstalledApkInfos_v2():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'pageNo': '1', 'pageSize': '200', 'category': '4'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + "/api/padControl/v2/verifyToken/getInstalledApkInfos"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    print(result.text)


def getInstalledApkInfos_v3():
    timestamp = getTimestamp()
    url = REQUEST_DOMAIN + "/api/padControl/v3/verifyToken/getInstalledApkInfos"
    requestParams = getParams(timestamp)
    specParams = {'pageNo': '1', 'pageSize': '200', 'category': '4'}
    requestParams.update(specParams)
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    print(result.text)


def getBindAccountList():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'pageNo': '1', 'pageSize': '200', 'category': '4'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + "/api/parentGroup/verifyToken/getBindAccountList"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    print(result.text)
    assert '"code":"0"' in result.text


def getAppUseDetails():
    t = time.time()
    cur_time = int(t)
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'dateTime': str(cur_time), 'type': '7'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + "/api/appUseTime/verifyToken/getAppUseDetails"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    print(result.text)
    assert '"code":"0"' in result.text


def getAreaCodeList():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    url = REQUEST_DOMAIN + "/api/account/getAreaCodeList"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.get(url, params=requestParams)
    print(result.text)
    assert '"code":"0"' in result.text


def getUserSettings():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    url = REQUEST_DOMAIN + "/api/userControlTime/verifyToken/getUserSettings"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    print(result.text)
    assert '"code":"0"' in result.text


def getUserInfoByMachineId():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    url = REQUEST_DOMAIN + "/api/userCenter/verifyToken/getUserInfoByMachineId"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    print(result.text)
    assert '"code":"0"' in result.text


def getAppMarketOpeningDegree():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    url = REQUEST_DOMAIN + "/api/padControl/verifyToken/getAppMarketOpeningDegree"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    print(result.text)
    assert '"code":"0"' in result.text


def getWhiteList():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'ps': '10', 'direct': '2', 'whiteId': '0'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + "/api/browserServer/verifyToken/getWhiteList"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    print(result.text)
    assert '"code":"0"' in result.text


def addLock():
    url = "http://questionanswer.eebbk.net/m1000/parent/addLock?machineId=700H38400163D&accountId=700H38400163D&status=0&BBK_ROUTE_FLAG=questionanswer"
    result = requests.get(url=url)
    print(result.text)
    assert '"errorCode":"101002"' in result.text


def gettLock():
    url = "http://questionanswer.eebbk.net/m1000/parent/getLock?machineId=700H38400163D&accountId=700H38400163D"
    result = requests.get(url=url)
    print(result.text)
    print('耗时是%s' % str(result.elapsed.microseconds / 1000))
    assert '"errorCode":"101002"' in result.text


def getLastedVersion():
    url = REQUEST_DOMAIN + '/answer/isLastedVersion'
    result = requests.get(url=url, params={'machineId': '700H38300018B'})
    print(result.text)

def addTimes():
    timestamp = getTimestamp()
    url = REQUEST_DOMAIN + '/api/englishRead/addTimes'
    requestParams = getParams(timestamp)
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    reuslt = requests.post(url=url,headers=getHeader(timestamp),data=requestParams)
    print(reuslt.text)


def main():
    # getInstalledApkInfos_v2()
    # getInstalledApkInfos_v3()
    # getAreaCodeList()
    # getBindAccountList()
    # getAppUseDetails()
    # getUserSettings()
    # getUserInfoByMachineId()
    # getAppMarketOpeningDegree()
    # getWhiteList()
    # # 未加密接口
    # addLock()
    # gettLock()
    addTimes()
    # getLastedVersion()


if __name__ == '__main__':
    main()
