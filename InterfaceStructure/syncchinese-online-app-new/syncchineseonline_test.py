# @File  : syncchineseonline_test.py
# @Author: LiuXingsheng
# @Date  : 2019/12/20
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import syncchineseonline_testUrlSet
import requests
import pytest
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.TestDomainType_Ali)
manager.setItemName(constants.syncchinese_online_app_new)

bookList = ['1', '2', '3', '4', '5', '6']


def test_getBookCatalogues():
    subtargetList = []
    subtargetnullIdList = []
    fathertargetList = []
    targetnullfatherIdList = []

    url = manager.getDomain() + '/app/chinese/getBookCatalogues'
    print(url)
    for book in bookList:
        param = {'bookId': str(book)}
        result = requests.get(url=url, params=param)
        objdata = demjson.decode(result.text)
        if objdata:
            if objdata['data']:
                if objdata['data']['catalogueVos']:
                    for item in objdata['data']['catalogueVos']:
                        if 'targetId' in item:
                            fathertargetList.append(item['targetId'])
                        else:
                            targetnullfatherIdList.append((item['bookId'], item['parentOrder']))
                        if 'subCatalogueList' in item:
                            for targetId in item['subCatalogueList']:
                                if 'targetId' in targetId:
                                    subtargetList.append(targetId['targetId'])
                                else:
                                    subtargetnullIdList.append((targetId['bookId'], targetId['id']))
                        else:
                            pass
                else:
                    assert False
        else:
            assert False
    subtargetList = list(set(subtargetList))
    fathertargetList = list(set(fathertargetList))
    # targetnullfatherIdList = list(set(targetnullfatherIdList))
    # subtargetnullIdList = list(set(subtargetnullIdList))
    print(subtargetList)
    print(fathertargetList)
    return subtargetList, fathertargetList


def test_getAssistantMain():
    contentnullList = []
    (subtargetList, fathertargetList) = test_getBookCatalogues()
    url = manager.getDomain() + '/app/chinese/getAssistantMain'
    print('subtargetid结果：-------------------------')
    for item in (subtargetList, fathertargetList):
        for targeId in item:
            param = {'targetId': str(targeId)}
            result = requests.get(url=url, params=param)
            objdata = demjson.decode(result.text)
            if objdata['data']:
                pass
            else:
                contentnullList.append(targeId)
    print('内容为空的targeid：', contentnullList)


def test_getContentTemplateWithTgtId(path, subtargetList, fathertargetList):
    contentnullList = []
    url = manager.getDomain() + path
    for item in (subtargetList, fathertargetList):
        for targeId in item:
            param = {'targetId': str(targeId)}
            result = requests.get(url=url, params=param)
            objdata = demjson.decode(result.text)
            if objdata['data']:
                pass
            else:
                contentnullList.append(targeId)
            if ('strangerWordList' in objdata['data']) or ('polyphoneList' in objdata['data']):
                if objdata['data']['strangerWordList']:
                    pass
                else:
                    contentnullList.append(targeId)
            else:
                pass
    print('{0} 内容为空的targeid：{1} 长度是：{2}'.format(path, contentnullList, len(contentnullList)))


def getBookCatalogInfo():
    pass


def getContentInfoByContent():
    pass


def getContentVoiceDuration():
    pass


def getContentVoiceUrl():
    pass


if __name__ == '__main__':
    (subtargetList, fathertargetList) = test_getBookCatalogues()
    print('子目录长度', len(subtargetList))
    print('书本目录长度：{0} 总长度：{1}'.format(len(fathertargetList), len(fathertargetList) + len(subtargetList)))
    for item in syncchineseonline_testUrlSet.UrlSet:
        test_getContentTemplateWithTgtId(syncchineseonline_testUrlSet.UrlSet[item], subtargetList, fathertargetList)
