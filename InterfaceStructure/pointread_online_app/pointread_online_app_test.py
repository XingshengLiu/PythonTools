# @File  : pointread_online_app_test.py
# @Author: LiuXingsheng
# @Date  : 2020/1/8
# @Desc  :
from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import pointread_online_app_testUrlSet
import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.pointread_online_app)

bookList = [1071, 1073, 1075]


# 1077, 1079, 1081, 1083, 1085, 1087, 1089, 1091, 1093, 1095, 1097, 1099, 1117, 1119, 1121,
#             1125, 1127, 1129, 1131, 1133, 1135, 1137, 1139, 1141, 1143, 1145, 1147, 1149, 1151, 1153, 1155, 1157, 1159,
#             1161, 1163, 1165, 1167, 1169, 1171, 1173, 1175, 1177, 1179, 1181, 1183, 1185, 1187, 1189, 1191, 1193, 1195,
#             1199, 1201, 1203, 1221, 1223, 1225, 1227, 1229, 1231, 1233, 1235, 1237, 1239, 1241, 1243, 1245]


def updateBackupSwitch():
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppUrlSet['updateBackupSwitch']
    param = {'switchStatus': '1'}
    result = requests.get(url=url, params=param)
    print(result.text)


def searchBookContents():
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppUrlSet['searchBookContents']
    for book in bookList:
        param = {'bookId': book}
        result = requests.get(url=url, params=param)
        print(result.text)


def pictureSearchAndVivoOcr():
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppUrlSet['pictureSearchAndVivoOcr']
    param = {
        'pictureUrl': 'https://search-characterword-dn.eebbk.net/search-characterword/file/2019/12/20/0842/1/8c7dd922ad47494fc02c388e12c00eac',
        'isZipData': '0', 'ptX': '80', 'ptY': '164'}
    header = {'Content-Type': 'multipart/form-data'}
    result = requests.request(method='POST', url=url, headers=header, params=param)
    print(result.text)


def getPublishers():
    publishList = []
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppOralUrlSet['getPublishers']
    print(url)
    result = requests.get(url=url)
    print(result.status_code,result.text)
    objdata = demjson.decode(result.text)
    if objdata['data']:
        for item in objdata['data']:
            publishList.append(item['id'])
    print('出版社列表', publishList)
    return publishList


def getPublisherBooks():
    bookList = []
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppOralUrlSet['getPublisherBooks']
    print(url)
    result = requests.get(url=url)
    objdata = demjson.decode(result.text)
    if objdata['data']:
        for item in objdata['data']:
            for bookitem in item['englishBookVos']:
                bookList.append(bookitem['id'])
    print('书籍列表', bookList)
    return bookList


def getBookByPublisher(publishList):
    booknulllist = []
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppOralUrlSet['getBookByPublisher']
    print(url)
    for id in publishList:
        result = requests.get(url=url, params={'publisherId': str(id)})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            pass
        else:
            booknulllist.append(id)
    print('数据为空的记录', booknulllist)


def getBookUnitsInfos(booklist):
    combinelist = []
    nulllist = []
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppOralUrlSet['getBookUnitsInfos']
    print(url)
    for book in booklist:
        result = requests.get(url=url, params={'bookId': str(book)})
        objdata = demjson.decode(result.text)
        if objdata['data'] and objdata['data']['catalogueVos']:
            for item in objdata['data']['catalogueVos']:
                combinelist.append((item['bookId'], item['unitId']))
        else:
            nulllist.append(book)
    print('书本id和单元id 集合数据', combinelist)
    print('空数据有', nulllist)
    return combinelist


def getPartInfoByBookUnit(combineList):
    voiceresnulllist = []
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppOralUrlSet['getPartInfoByBookUnit']
    print(url)
    for cp in combineList:
        result = requests.get(url=url, params={'bookId': str(cp[0]), 'unit': str(cp[1])})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            for item in objdata['data']:
                for chapter in item['contentVos']:
                    if chapter['voiceUrl']:
                        pass
                    else:
                        voiceresnulllist.append(chapter['id'])
    print('语音资源为空的数据有', voiceresnulllist)

def test_pictureSearch():
    url = manager.getDomain() + pointread_online_app_testUrlSet.PointreadOnlineAppUrlSet['pictureSearch']
    print(url)
    param = {'zipType': '0', 'ptX': '835', 'ptY': '873','bookId':'651','pageNo':'2'}
    with open(r'H:\测试图片\小布快搜单张可用\YuvData1586743598831_0_835_873_1600_2096.jpg',
            'rb')as f:
        file = {'file': f.read()}
    result = requests.post(url=url, data=param, files=file)
    print(result.text)
    assert 'bookName' in result.text
    assert 'outlineText' in result.text
    assert 'pageId' in result.text
    assert 'pageNo' in result.text
    assert 'pictureSearchResultVo' in result.text
    assert '轻松优美的音乐' in result.text

if __name__ == '__main__':
    # searchBookContents()
    # pictureSearchAndVivoOcr()
    # publishList = getPublishers()
    # booklist = getPublisherBooks()
    # getBookByPublisher(publishList)
    # combinelist = getBookUnitsInfos(booklist)
    # getPartInfoByBookUnit(combinelist)
    test_pictureSearch()

