# @File  : searchCharacterwod_test.py
# @Author: LiuXingsheng
# @Date  : 2020/2/17
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import searchcharacterword_testUrlSet
import requests
import demjson


def getS3pheader():
    return {'machineId': '700S3760026BY', 'accountId': '4051922', 'apkPackageName': 'com.eebbk.askhomework',
            'apkVersionCode': '3000000', 'deviceModel': 'S3 Pro',
            'deviceOSVersion': 'V1.0.0_180409'}


def getS5header():
    return {'machineId': '700S593001B3V', 'deviceModel': 'S5', 'apkVersionName': '4.0.0.0.0',
            'apkVersionCode': '4000000', 'accountId': '4051922',
            'apkPackageName': 'com.eebbk.askhomework', 'deviceOSVersion': 'V1.0.0_180409'}


manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.search_characterword)


def getChineseStudies():
    wronglist = []
    correctlist = []
    url = manager.getDomain() + searchcharacterword_testUrlSet.searchCharacterword['getChineseStudies']
    print(url)
    result = requests.get(url=url, headers=getS5header())
    print(result.text)
    objdata = demjson.decode(result.text)
    if objdata['data']:
        for item in objdata['data']:
            if 'poetryDurations' in item:
                for poetry in item['poetryDurations']:
                    if poetry['duration'] and poetry['poetryName']:
                        correctlist.append(poetry['id'])
                    else:
                        wronglist.append(poetry['id'])
            else:
                if item['duration']:
                    correctlist.append(item['id'])
                else:
                    wronglist.append(item['id'])
    print('诗名为空或时长为空的诗歌id为', wronglist)
    return correctlist


def getPoetryVoiceList(correctlist):
    nulllist = []
    url = manager.getDomain() + searchcharacterword_testUrlSet.searchCharacterword['getPoetryVoiceList']
    print(url)
    for item in correctlist:
        result = requests.get(url=url, params={'ids': item, 'pageNum': '1', 'pageSize': '15'})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            pass
        else:
            nulllist.append(item)
    print('资源为空的id', nulllist)


def getPoetryDetailBySentence():
    sentenceList = []
    url = manager.getDomain() + searchcharacterword_testUrlSet.searchCharacterword['getPoetryDetailBySentence']
    print(url)
    sentenceparam2 = {'凄凄惨惨戚戚'}
    sentenceparam3 = {'羌笛何须怨杨柳'}
    sentenceparam4 = {'枯藤老树昏鸦'}
    sentenceparam1 = {'test'}
    sentenceparam5 = {'任意文本'}
    sentenceparam6 = {'1+1=?'}
    sentenceList.append(sentenceparam1)
    sentenceList.append(sentenceparam2)
    sentenceList.append(sentenceparam3)
    sentenceList.append(sentenceparam4)
    sentenceList.append(sentenceparam5)
    sentenceList.append(sentenceparam6)
    for item in sentenceList:
        print(item)
        result = requests.post(url=url, params={'sentence': item}, headers=getS5header())
        print(result.status_code, result.text)


if __name__ == '__main__':
    corretlist = getChineseStudies()
    getPoetryVoiceList(corretlist)
    # getPoetryDetailBySentence()
