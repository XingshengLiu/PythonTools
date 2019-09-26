# @File  : familyTest.py
# @Author: LiuXingsheng
# @Date  : 2018/12/20
# @Desc  :

import requests, time
import http_common

# 账号token
ACCESS_TOKEN = 'eyJhY2NvdW50IjoiMTg1NzYzNzAxMDYiLCJhY2NvdW50SWQiOiIxOTQ4MTY3IiwibWFjaGluZUlkIjoiOGEyNDRkM2UiLCJjcmVhdGVUaW1lIjoxNTQ1NzIxNTk0NjcyfQ'
Access_Token_Alpha = 'eyJhY2NvdW50IjoiMTg1NzYzNzAxMDYiLCJhY2NvdW50SWQiOiIxOTQ4MTY3IiwibWFjaGluZUlkIjoiOGEyNDRkM2UiLCJjcmVhdGVUaW1lIjoxNTQ1MTIyMDc1NjUwfQ'
Access_Token_Test = 'eyJhY2NvdW50IjoiMTg1NzYzNzAxMDYiLCJhY2NvdW50SWQiOiIzMDYwOSIsIm1hY2hpbmVJZCI6IjhhMjQ0ZDNlIiwiY3JlYXRlVGltZSI6MTU0NTEyNjgwMDYzMn0'

# 正式环境域名
# REQUEST_DOMAIN = "https://assistant-pad.eebbk.net"


# 集成环境域名
REQUEST_DOMAIN = "https://assistant-pad.alpha.eebbk.net"


# 测试环境域名
# REQUEST_DOMAIN = "https://test.eebbk.net/assistant-pad"


# 获取时间戳
def getTimestamp():
    t = time.time()
    cur_time = int(t)
    time_local = time.localtime(cur_time)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return str(dt)


def getK5Header():
    requestHeader = {'accountId': '2306881', 'apkPackageName': 'com.eebbk.parentalcontrol', 'apkVersionCode': '2200',
                     'deviceModel': 'Redmi Note 4X',
                     'deviceOSVersion': 'V9.5.1.0.NCFCNFA', 'machineId': '9e1b9b0f0804', 'padMachineId': 'OK1001000105',
                     'padDeviceModel': 'K5'}
    return requestHeader


def getParams(timestamp):
    requestParams = {'machineId': '700H38300018B', 'phoneModel': 'Xiaomi-MI 3C',
                     'phoneSysver': 'V7.1.5.0.KXDCNCK', 'appId': 'com.eebbk.parentalcontrol', 'appVer': '2.200',
                     'phoneId': '8a244d3e',
                     'token': ACCESS_TOKEN, 'timestamp': timestamp}
    return requestParams


def getHeader(timestamp):
    requestHeader = {'accountId': '30609', 'apkPackageName': 'com.eebbk.parentalcontrol', 'apkVersionCode': '2200',
                     'deviceModel': 'MI 3C', 'appVer': '2.2.0.0', 'md5': 'f2354b28eb8880b3677b6f7dd323ce97',
                     'deviceOSVersion': 'V7.1.5.0.KXDCNCK', 'machineId': '8a244d3e', 'padDeviceModel': 'S3 Pro',
                     'padMachineId': '700H38300018B', 'timestamp': timestamp}
    return requestHeader


def getHeaderTestNoMd5(timestamp):
    requestHeader = {'accountId': '30609', 'apkPackageName': 'com.eebbk.parentalcontrol', 'apkVersionCode': '2301',
                     'deviceModel': 'MI 3C', 'appVer': '2.3.0.1',
                     'deviceOSVersion': 'V7.1.5.0.KXDCNCK', 'machineId': '8a244d3e', 'padDeviceModel': 'S3 Pro',
                     'padMachineId': '700H38300018B', 'timestamp': timestamp}
    return requestHeader


def getHeader_Concern(timestamp):
    """
    人文关怀手机端header
    :param timestamp:
    :return:
    """
    return {'accountId': '1948167', 'apkPackageName': 'com.eebbk.parentalcontrol', 'apkVersionCode': '2400',
            'deviceModel': 'MI 3C', 'appVer': '2.4.0.0',
            'deviceOSVersion': 'V7.1.5.0.KXDCNCK', 'machineId': '8a244d3e', 'padDeviceModel': 'S3 Pro',
            'padMachineId': '700H38300018B', 'timestamp': timestamp}


def getHeader_Concern_Pad(timestamp):
    """
    人文关怀平板端header 测试环境
    :param timestamp:
    :return:
    """
    return {'accountId': 'test_accountId', 'apkPackageName': 'com.eebbk.parentsupport', 'apkVersionCode': '540',
            'deviceModel': 'S3 Pro', 'deviceOSVersion': 'V1.1.0_180713', 'machineId': '700H38300018B',
            'padDeviceModel': 'S3 Pro', 'timestamp': timestamp}


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
    # # print(result.text)
    assert '"code":"0"' in result.text


def getInstalledApkInfos_v3():
    timestamp = getTimestamp()
    url = REQUEST_DOMAIN + "/api/padControl/v3/verifyToken/getInstalledApkInfos"
    requestParams = getParams(timestamp)
    specParams = {'pageNo': '1', 'pageSize': '200', 'category': '4'}
    requestParams.update(specParams)
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    # # print(result.text)
    assert '"code":"0"' in result.text


def getBindAccountList():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'pageNo': '1', 'pageSize': '200', 'category': '4'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + "/api/parentGroup/verifyToken/getBindAccountList"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    # # print(result.text)
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
    # # print(result.text)
    assert '"code":"0"' in result.text


def getAreaCodeList():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    url = REQUEST_DOMAIN + "/api/account/getAreaCodeList"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.get(url, params=requestParams)
    # # print(result.text)
    assert '"code":"0"' in result.text


def getUserSettings():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    url = REQUEST_DOMAIN + "/api/userControlTime/verifyToken/getUserSettings"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def getUserInfoByMachineId():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    url = REQUEST_DOMAIN + "/api/userCenter/verifyToken/getUserInfoByMachineId"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    # # print(result.text)
    assert '"code":"0"' in result.text


def getAppMarketOpeningDegree():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    url = REQUEST_DOMAIN + "/api/padControl/verifyToken/getAppMarketOpeningDegree"
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), data=requestParams)
    # # print(result.text)
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
    # # print(result.text)
    assert '"code":"0"' in result.text


def deleteUsableInterval():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'id': 353, 'padMachineId': '700H38300018B'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/deleteUsableInterval'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def getUserTimeLimitList():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'dateType': 0, 'padMachineId': '700H38300018B'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/getUserTimeLimitList'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.get(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def getUserTimeUseTimeAndRemainingTimeLimit():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'padMachineId': '700H38300018B'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/getUseTimeAndRemainingTimeLimit'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def getUserSettingsTest():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'machineId': '700H38300018B'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/getUserSettings'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeaderTestNoMd5(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def saveUserTimeUsableInterval():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {
        'jsonList': '[{"title":"休息日","endTime":"22:22","startTime":"22:23",'
                    '"machineId":"700H38300018B","id":999,"isOpen":1,"dateType":1}]'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/saveUserTimeUsableInterval'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def syncUserControlTime():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'operationType': '上学日', 'operationData': '3600000',
                  'dataList': '[{"week":"aaaaabb","title":"上学日","machineId":"700H38300018B","resId":1,'
                              '"id":0,"duration":3600000},{"week":"bbbbbaa","title":"休息日","machineId":"700H38300018B",'
                              '"resId":2,"id":1,"duration":7200000}]',
                  'machineId': '700H38300018B', 'accountId': '30609'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/syncUserControlTime'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def updateUsableIntervalSwitch():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'dateType': '0', 'isOpen': '1', 'padMachineId': '700H38300018B'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/updateUsableIntervalSwitch'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def updateUserTimeUsableInterval():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {
        'json': '{"title":"休息日","endTime":"21:00","startTime":"07:00","machineId":"700H38300018B",'
                '"id":361,"isOpen":1,"isResponse":2,"dateType":1}'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/updateUserTimeUsableInterval'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def saveUserTimeTempLimitInfo():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {
        'json': '{"title":"今日","machineId":"700H38300018B","playDuration":6000000,'
                '"totalDuration":8400000,"dateTime":20181108}'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/saveUserTimeTempLimitInfo'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def saveUserTimeTotalAndPlayLimitInfo():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {
        'playJson': '{"title":"休息日","machineId":"700H38300018B","playDuration":7200000,'
                    '"isResponse":2,"isChange":1,"isOpen":1,"dateType":1}',
        'totalJson': '{"title":"休息日","machineId":"700H38300018B","totalDuration":0,'
                     '"isResponse":0,"isChange":0,"dateType":1,"isOpen":0}'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/api/userControlTime/verifyToken/saveUserTimeTotalAndPlayLimitInfo'
    signDict = getMD5Str(url, requestParams)
    requestParams.update(signDict)
    result = requests.post(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


# 以下为未加密请求
def addLock():
    url = "http://questionanswer.eebbk.net/m1000/parent/addLock?machineId=700H38400163D&" \
          "accountId=700H38400163D&status=0&BBK_ROUTE_FLAG=questionanswer"
    result = requests.get(url=url)
    # print(result.text)
    assert '"errorCode":"101002"' in result.text


def gettLock():
    url = "http://questionanswer.eebbk.net/m1000/parent/getLock?machineId=700H38400163D&accountId=700H38400163D"
    result = requests.get(url=url)
    # print(result.text)
    assert '"errorCode":"101002"' in result.text


def getEyeSwitchInfo():
    timestamp = getTimestamp()
    url = REQUEST_DOMAIN + '/safe/getEyeSwitchInfo/700H38400163D'
    result = requests.request(method="GET", url=url, headers=getHeader(timestamp))
    # # print(result.text)
    assert '"code":"200"' in result.text


def getProtectEyeInfo():
    timestamp = getTimestamp()
    url = REQUEST_DOMAIN + '/safe/getProtectEyeInfo/700H38400163D'
    result = requests.request(method="GET", url=url, headers=getHeader(timestamp))
    # # print(result.text)
    assert '"code":"200"' in result.text


def getCurrentLoveAgreementStatus():
    url = REQUEST_DOMAIN + '/mobileContract/getCurrentLoveAgreementStatus?padMachineId=OK1001000105'
    result = requests.request(method='GET', url=url, headers=getK5Header())
    # # print(result.text)
    assert '"code":"200"' in result.text


def getInitContractInfo():
    url = REQUEST_DOMAIN + '/mobileContract/getInitContractInfo'
    result = requests.request(method='GET', url=url, headers=getK5Header())
    # # print(result.text)
    assert '"code":"200"' in result.text


def getOnlineOrImStatus():
    url = REQUEST_DOMAIN + '/mobileContract/getOnlineOrImStatus?padMachineId=OK1001000105'
    result = requests.request(method='GET', url=url, headers=getK5Header())
    # # print(result.text)
    assert '"code":"200"' in result.text


def getApkInfoByPackaeName():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'apkPackageNames': 'com.eebbk.askhomework', 'machineId': '70S3S88092982', 'deviceModel': 'S3 Pro'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/padUserControlTime/verifyToken/getApkInfoByPackaeName'
    result = requests.get(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


def getPadUserTimeLimitList():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'machineId': '700H38300018B'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/padUserControlTime/verifyToken/getPadUserTimeLimitList'
    result = requests.get(url=url, headers=getHeader(timestamp), params=requestParams, cert=())
    print(result.text)
    assert '"code":"0"' in result.text


def getUseTimeAndRemainingTimeLimit():
    timestamp = getTimestamp()
    requestParams = getParams(timestamp)
    specParams = {'machineId': '700H38300018B'}
    requestParams.update(specParams)
    url = REQUEST_DOMAIN + '/padUserControlTime/verifyToken/getUseTimeAndRemainingTimeLimit'
    result = requests.get(url=url, headers=getHeader(timestamp), params=requestParams)
    # print(result.text)
    assert '"code":"0"' in result.text


# 查看当天和前七天使用记录列表
def getApkUseRecordList():
    timestamp = getTimestamp()
    specParams = {'dateTime': '1', 'machineId': '700H38300018B', 'category': 4}
    url = REQUEST_DOMAIN + '/learn/apkUseRecord/getApkUseRecordList'
    result = requests.get(url=url, headers=getHeader(timestamp), params=specParams)
    assert '"code":"200"' in result.text


"""
人文关怀需求
"""


def getCarePushSwitchPojoList():
    """
    获取人文关怀推送开关
    :return:
    """
    timestamp = getTimestamp()
    url = REQUEST_DOMAIN + '/remind/push/getCarePushSwitchPojoList'
    param = 'accountId=1948167'
    result = requests.get(url=url, params=param, headers=getHeader_Concern(timestamp))
    print(result.text)


def updateCarePushSwitch():
    """
    更新开关
    :return:
    """
    timestamp = getTimestamp()
    url = REQUEST_DOMAIN + '/remind/push/updateCarePushSwitch'
    requestParams = getParams(timestamp)
    specParams = {'msgType': '122', 'isOpen': '0', 'accountId': '1948167'}
    requestParams.update(specParams)
    result = requests.post(url=url, headers=getHeader_Concern(timestamp), data=requestParams)
    print(result.text)


def reportCarePushRecord():
    """
    平板端上报人文关怀记录
    :return:
    """
    timestamp = getTimestamp()
    millstamp = int(round(time.time() * 1000))
    url = REQUEST_DOMAIN + '/remind/push/reportCarePushRecord'
    paramsStr = '''[{"dateTime":%s,"machineId":"700H38300018B","msgType":"126","content":22222}]''' % (
        str(millstamp))
    header = getHeader_Concern_Pad(timestamp)
    header.update({'deviceModel':'H9A'})
    header.update({'padDeviceModel': 'H9A'})
    header.update({'Content-Type': 'application/json'})
    print(header)
    print(paramsStr)
    result = requests.post(url=url, headers=header, data=paramsStr)
    print(result.text)


def getBanner():
    """
    获取banner信息
    :return:
    """
    timestamp = getTimestamp()
    url = REQUEST_DOMAIN + '/learn/banner/getBanner'
    result = requests.get(url=url, headers=getHeaderTestNoMd5(timestamp))
    assert '"code":"200"' in result.text


# # 推送接口
# def reportCarePushRecord():
#     timestamp = getTimestamp()
#     url = REQUEST_DOMAIN + '/remind/push/reportCarePushRecord'
#     param = {
#         'carePushRecordPojoList': '''[{"content": "1111111111","dateTime": 1547096766000,"machineId": "700K57000083E","msgType": "126"}]'''}
#     headers = getHeaderTestNoMd5(timestamp)
#     headers.update({'Content-Type': 'application/json'})
#     result = requests.post(url=url, headers=headers, data=param)
#     print(result.text)


def main():
    """
    所有save接口不做拨测，只做测试用途
    :return:
    """
    # getInstalledApkInfos_v2()
    # getInstalledApkInfos_v3()
    # getAreaCodeList()
    # getBindAccountList()
    # getAppUseDetails()
    # getUserSettings()
    # getUserInfoByMachineId()
    # getAppMarketOpeningDegree()
    # getWhiteList()
    # getUserTimeUseTimeAndRemainingTimeLimit()
    # syncUserControlTime()
    # getUserSettingsTest()
    # getUserTimeLimitList()
    # saveUserTimeTempLimitInfo()
    # saveUserTimeUsableInterval()
    # updateUsableIntervalSwitch()
    # 此删除接口需要先调用save，然后getUserTimeLimitList获取Id，根据获取到的Id去删除
    # deleteUsableInterval()
    # updateUserTimeUsableInterval()
    # saveUserTimeTotalAndPlayLimitInfo()cloud
    # 以下为人文关怀需求
    # updateCarePushSwitch()
    # getCarePushSwitchPojoList()
    # post接口不做拨测
    reportCarePushRecord()
    # # 未加密接口
    # addLock()
    # gettLock()
    # getEyeSwitchInfo()
    # getProtectEyeInfo()
    # getCurrentLoveAgreementStatus()
    # getInitContractInfo()
    # getOnlineOrImStatus()
    # getApkInfoByPackaeName()
    # getPadUserTimeLimitList()
    # getUseTimeAndRemainingTimeLimit()
    # getApkUseRecordList()
    # getBanner()


if __name__ == '__main__':
    main()
