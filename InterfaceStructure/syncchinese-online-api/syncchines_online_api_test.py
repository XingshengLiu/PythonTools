# @File  : syncchines_online_api_test.py
# @Author: LiuXingsheng
# @Date  : 2020/2/26
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import syncchinese_online_api_testUrlSet

import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.syncchinese_online_api)


def getBookCatalogInfo():
    bookList = []
    url = manager.getDomain() + syncchinese_online_api_testUrlSet.syncchineseOnlineApi['getBookCatalogInfo']
    print(url)
    result = requests.get(url)
    print(result.text)
    objdata = demjson.decode(result.text)
    for item in objdata['data']:
        if 'data' in item:
            for item1 in item['data']:
                if 'data' in item1:
                    for item2 in item1['data']:
                        if 'data' in item2:
                            for item3 in item2['data']:
                                bookList.append(item3['id'])
    print(bookList)
    return bookList


def searchBookContents(booklist):
    contentList = []
    url = manager.getDomain() + syncchinese_online_api_testUrlSet.syncchineseOnlineApi['searchBookContents']
    print(url)
    for item in booklist:
        result = requests.get(url, params={'bookId': item})
        objdata = demjson.decode(result.text)
        if 'contentsList' in objdata['data']:
            for item in objdata['data']['contentsList']:
                contentList.append((item['id'], item['bookId'], item['name']))
    print(contentList)
    return contentList


def getContentInfoByContent(contentList):
    contentnullList = []
    url = manager.getDomain() + syncchinese_online_api_testUrlSet.syncchineseOnlineApi['getContentInfoByContent']
    print(url)
    for item in contentList:
        result = requests.get(url=url, params={'content': str(item[2])})
        objdata = demjson.decode(result.text)
        if 'pathInfos' in objdata:
            if objdata['pathInfos']:
                pass
            else:
                contentnullList.append(item)
    print('音频内容为空的课程标题', contentnullList)


def getContentVoiceDuration(bookList):
    resnullList = []
    url = manager.getDomain() + syncchinese_online_api_testUrlSet.syncchineseOnlineApi['getContentVoiceDuration']
    print(url)
    for item in bookList:
        result = requests.get(url=url, params={'bookId': str(item)})
        objdata = demjson.decode(result.text)
        if 'data' in objdata:
            for item in objdata['data']:
                if item['duration']:
                    pass
                else:
                    resnullList.append(item['id'])
    print('时长为空的课文id是', resnullList)


def getContentVoiceUrl(contentList):
    voicenulllist = []
    url = manager.getDomain() + syncchinese_online_api_testUrlSet.syncchineseOnlineApi['getContentVoiceUrl']
    print(url)
    for item in contentList:
        result = requests.get(url=url, params={'bookId': item[1], 'contentIds': item[0]})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            print('bookId :{0} contentIds: {1} 数据为：{2}'.format(item[1], item[0], result.text))
            pass
        else:
            voicenulllist.append((item[1], item[0]))
    print('voiceurl为空的数据有', voicenulllist)


if __name__ == '__main__':
    booklist = getBookCatalogInfo()
    # getContentVoiceDuration(booklist)
    # contentList = searchBookContents(booklist)
    # getContentInfoByContent(contentList)
    # getContentVoiceUrl(contentList)
