# @File  : english-pointread-online-api_test.py
# @Author: LiuXingsheng
# @Date  : 2019/12/26
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import english_pointread_online_api_testUrlSet
import requests
import demjson
import xlsxwriter
import os
from collections import Counter

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.english_pointread_online_api)


def test_getPublishers():
    publishlist = []
    url = manager.getDomain() + english_pointread_online_api_testUrlSet.PointreadOnlineUrlset['getPublishers']
    print(url)
    result = requests.get(url=url)
    objedata = demjson.decode(result.text)
    if objedata and objedata['data']:
        for item in objedata['data']:
            publishlist.append(item['id'])
    else:
        print('数据返回为空')
    return publishlist


def test_getPublisherBooks():
    bookidlist = []
    url = manager.getDomain() + english_pointread_online_api_testUrlSet.PointreadOnlineUrlset['getPublisherBooks']
    print(url)
    result = requests.get(url=url)
    objdata = demjson.decode(result.text)
    print(objdata)
    if objdata and objdata['data']:
        for item in objdata['data']:
            if 'englishBookVos' in item and item['englishBookVos']:
                for pushlish in item['englishBookVos']:
                    if item['englishBookVos']:
                        bookidlist.append(pushlish['id'])
                    else:
                        print('出版社id {0} 书籍为空'.format(item['id']))
            else:
                print('出版社id {0} 书籍为空'.format(item['id']))
    else:
        print('data 为空')
    bookrepeat = dict(Counter(bookidlist))
    print('重复书本id和章节', {key: value for key, value in bookrepeat.items() if value > 1})
    return bookidlist


def test_getBookUnitsInfos(bookidlist):
    comlist = []
    wrongbookidlist = []
    unitNameList = []
    url = manager.getDomain() + english_pointread_online_api_testUrlSet.PointreadOnlineUrlset['getBookUnitsInfos']
    print(url)
    for book in bookidlist:
        result = requests.get(url=url, params={'bookId': str(book)})
        if result.status_code != requests.codes.ok:
            wrongbookidlist.append(book)
        else:
            objdata = demjson.decode(result.text)
            if objdata and objdata['data']:
                if 'catalogueVos' in objdata['data']:
                    for itemold in objdata['data']['catalogueVos']:
                        if 'unitPartVos' in itemold and itemold['unitPartVos']:
                            for item in itemold['unitPartVos']:
                                comlist.append((item['bookId'], item['unitId']))
                                unitNameList.append((item['bookId'], item['unitName']))
                        else:
                            print('没有unitPartVos信息')
                            wrongbookidlist.append(book)
                else:
                    print('没有catalogueVos目录信息')
                    wrongbookidlist.append(book)
            else:
                print('数据为空')
    print('获取书本单元信息异常的id有', wrongbookidlist)
    # wrongbooklist = dict(Counter(wrongbookidlist))
    # print('重复书本id和章节', {key: value for key, value in wrongbooklist.items() if value > 1})
    return comlist, unitNameList


def test_getBookByPublisher(publishlist):
    url = manager.getDomain() + english_pointread_online_api_testUrlSet.PointreadOnlineUrlset['getBookByPublisher']
    print(url)
    for publish in publishlist:
        result = requests.get(url=url, params={'publisherId': str(publish)})
        print('出版社id为：{0} 返回的书本有：{1}'.format(str(publish), result.text))


def test_getPartInfoByBookUnit(comlist):
    print(comlist)
    nullList = []
    detaillist = []
    url = manager.getDomain() + english_pointread_online_api_testUrlSet.PointreadOnlineUrlset['getPartInfoByBookUnit']
    print(url)
    for item in comlist:
        result = requests.get(url=url, params={'bookId': str(item[0]), 'unit': str(item[1])})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            for itemnew in objdata['data']:
                for item2 in itemnew['contentVos']:
                    if item2['voiceUrl']:
                        pass
                    else:
                        nullList.append((itemnew['partId'], item2['id'], item2['blockId']))
        detaillist.append((str(item[0]), str(item[1]), result.text))
    column = 1
    workbook = xlsxwriter.Workbook(os.path.join(os.getcwd(), 'detail.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    ws.write(0, 0, '书本id')
    ws.write(0, 1, '单元id')
    ws.write(0, 2, '数据返回')
    for item in detaillist:
        ws.write(column, 0, str(item[0]))
        ws.write(column, 1, str(item[1]))
        ws.write(column, 2, str(item[2]))
        column = column + 1
    workbook.close()
    print('voice为空的列表为', nullList)


def getUnitVoiceInfo(unitNameList):
    notsameList = []
    contentnullList = []
    url = manager.getDomain() + english_pointread_online_api_testUrlSet.PointreadOnlineUrlset['getUnitVoiceInfo']
    print(url)
    for item in unitNameList:
        result = requests.get(url=url, params={'unitName': str(item[1])})
        objdata = demjson.decode(result.text)
        if objdata and objdata['data']:
            if objdata['data']['textName'] == item[1] and objdata['data']['pathInfos']:
                pass
            elif (str(objdata['data']['textName']).replace(' ', '')) != item[1]:
                notsameList.append((item[0], item[1], objdata['data']['bookId'], objdata['data']['textName']))
            elif objdata['data']['pathInfos'] is None:
                contentnullList.append((objdata['data']['bookId'], objdata['data']['textName']))
    print('内容为空的数据', contentnullList)
    print('请求单元名和返回单元不一致数据', notsameList)


def getBookUnitInfoByBookId(bookidlist):
    nullList = []
    datalist = []
    url = manager.getDomain() + english_pointread_online_api_testUrlSet.PointreadOnlineUrlset['getBookUnitInfoByBookId']
    print(url)
    for book in bookidlist:
        result = requests.get(url=url, params={'bookId': book})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            for item in objdata['data']:
                if item['duration']:
                    datalist.append((book, item['model'],item['id']))
                else:
                    nullList.append((book, item['model'],item['id']))
    b = dict(Counter(datalist))
    print('重复书本id和章节', {key: value for key, value in b.items() if value > 1})
    print('时长为空的书本id和章节id为：', nullList)


def test():
    url = manager.getDomain() + english_pointread_online_api_testUrlSet.PointreadOnlineUrlset['getBookUnitInfoByBookId']
    result = requests.get(url=url, params={'bookId': 987})
    print(result.text)


def test1():
    url = 'http://test.eebbk.net/syncchinese/api/morningListening/addMorningListeningDetail'
    params = {"machineId": "700S593001AE5",
              "isNight": 1,
              "startTime": 1578011686076,
              "duration": 10000,
              "contentDuration": 500000,
              "content":
                  {
                      "typeId": 1,
                      "moduleName": "同步语文",
                      "gradeName": "三年级",
                      "volumeName": "上册",
                      "publisherName": "人教版",
                      "bookName": "人教小学语文三年级上册",
                      "textinfo": [
                          {
                              "textName": "蜗牛"
                          },
                          {
                              "textName": "出师表"
                          }
                      ]
                  }}
    result = requests.post(json=params, url=url)
    print(result.text)


if __name__ == '__main__':
    print('***********************************\n')
    # publishlist = test_getPublishers()
    # print('出版社id列表为：', publishlist)
    print('***********************************\n')
    bookidlist = test_getPublisherBooks()
    # print('bookList 是', bookidlist)
    print('***********************************\n')
    # combinelist = test_getBookUnitsInfos(bookidlist)
    # print('comlist 是', combinelist[0])
    # print('***********************************\n')
    # test_getBookByPublisher(publishlist)
    # print('***********************************\n')
    # test_getPartInfoByBookUnit(combinelist[0])
    # getUnitVoiceInfo(combinelist[1])
    getBookUnitInfoByBookId(bookidlist)
    # test()
    # test1()
