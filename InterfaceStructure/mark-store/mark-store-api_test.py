# @File  : mark-store-api_test.py
# @Author: LiuXingsheng
# @Date  : 2020/3/7
# @Desc  :
from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import mark_store_testUrlSet
import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.TestDomainType_Asia)
manager.setItemName(constants.markstore)
Token = 'fab4eabe51d7e0f1db1733371d4d0ee89ce540d0117534ca6684ebfed089f2c4dc6007f864e0faf0'
testaccountId = '2201'


def getCommmonHeader():
    return {'accountId': testaccountId, 'machineId': '7V100030F50F5', 'apkPackageName': 'com.eebbk.learningcenter',
            'apkVersionCode': '1000000', 'deviceModel': 'V100',
            'deviceOSVersion': 'V1.0.0_200220',
            'token': Token}


def getTaskList():
    taskList = []
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['getTaskList']
    print(url)
    result = requests.get(url=url, headers=getCommmonHeader(),
                          params={'accountId': testaccountId, 'appId': '',
                                  'apkPackageName': 'com.eebbk.learningcenter'})
    print(result.text)
    objdata = demjson.decode(result.text)
    if objdata['data']:
        for item in objdata['data']:
            taskList.append((item['todayTaskId'], item['taskName'], item['appKey'], item['moduleId'], item['taskMark'],
                             item['ruleCode']))
    return taskList


def updateTodayTask(taskList):
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['updateTodayTask']
    print(url)
    for task in taskList:
        result = requests.get(url=url, headers=getCommmonHeader(),
                              params={'accountId': testaccountId, 'taskId': task[0], 'taskName': task[1],
                                      'getStatus': '1',
                                      'currentProgress': '0'})
        print(result.text)


def completedTask(taskList):
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['completedTask']
    print(url)
    for task in taskList:
        result = requests.get(url=url, headers=getCommmonHeader(),
                              params={'accountId': testaccountId, 'taskType': '2', 'taskId': task[0],
                                      'taskName': task[1],
                                      'token': Token,
                                      'appKey': task[2], 'moduleId': task[3], 'mark': 15, 'ruleCode': task[5]})
        print(result.text)


def getMarkStoreList():
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['getMarkStoreList']
    print(url)
    result = requests.get(url=url, params={'accountId': testaccountId, 'kindType': '22', 'isVirtual': '1'},
                          headers=getCommmonHeader())
    print(result.text)


def redeemGoods():
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['redeemGoods']
    print(url)
    requests.get(url=url,params={'accountId':'','storeId':'','token':'','quantity':'1'})


def updateUserStore():
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['updateUserStore']
    print(url)
    result = requests.get(url=url, params={'accountId': testaccountId, 'storeId': '69', 'kindType': '22'},headers=getCommmonHeader())
    print(result.text)


def getUserGoods():
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['getUserGoods']
    print(url)
    result = requests.get(url=url, params={'accountId': testaccountId, 'kindType': '22'}, headers=getCommmonHeader())
    print(result.text)


def getLastTaskCoin():
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['getLastTaskCoin']
    print(url)
    result = requests.get(url=url, params={'accountId': testaccountId}, headers=getCommmonHeader())
    print(result.text)
    objdata = demjson.decode(result.text)
    if objdata['data']:
        return objdata['data']['totalCount']


def addLastTaskCoin():
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['addLastTaskCoin']
    print(url)
    result = requests.get(url=url,
                          params={'accountId': testaccountId, 'token': Token, 'appKey': '1100', 'moduleId': '1100'},
                          headers=getCommmonHeader())
    print(result.text)


def getUserUsingStore():
    url = manager.getDomain() + mark_store_testUrlSet.markstoreUrlSet['getUserUsingStore']
    print(url)
    result = requests.post(url=url, params={'accountId': testaccountId, 'kindType': '22'}, headers=getCommmonHeader())
    print(result.text)


if __name__ == '__main__':
    taskList = getTaskList()
    # updateTodayTask(taskList)
    # getTaskList()
    completedTask(taskList)
    oldtotalcount = getLastTaskCoin()
    # addLastTaskCoin()
    # newtotalcount = getLastTaskCoin()
    # if newtotalcount - oldtotalcount == 45:
    #     print('完成任务增加正确')
    # else:
    #     print('旧积分为 {0} 新积分为 {1}'.format(oldtotalcount, newtotalcount))
    # getMarkStoreList()
    # getUserGoods()
    # getUserUsingStore()
    # updateUserStore()
    # getUserUsingStore()
