# @File  : syncchinese_test.py
# @Author: LiuXingsheng
# @Date  : 2020/3/27
# @Desc  :


from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import syncchinese_testUrlSet
import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.syncchinese)


def getUrlandprint(item):
    url = manager.getDomain() + syncchinese_testUrlSet.syncChineseUrlSet[item]
    print(url)
    return url


def getStoreShowMudole():
    url = getUrlandprint('getStoreShowMudole')
    result = requests.get(url=url, params={'deviceModel': 'S5', 'versionCode': '6120000'})
    if result.status_code == 200:
        objdata = demjson.decode(result.text)
        if 'data' in objdata:
            devicelist = objdata['data']['module'].split(';')
            print('显示的机型有', devicelist)
            for deivce in devicelist:
                result = requests.get(url=url, params={'deviceModel': deivce, 'versionCode': '6120000'})
                if objdata['data']['module'] in result.text:
                    pass
                else:
                    print(deivce, '请求异常', result.text)
    else:
        print('请求异常', result.text)


if __name__ == '__main__':
    getStoreShowMudole()
