# @File  : askhomework_test.py
# @Author: LiuXingsheng
# @Date  : 2019/12/24
# @Desc  :
from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import askhomewor_testUrlSet
from InterfaceStructure.resources import requestheaders
import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.askhomework)


def test_getASRInfoByMachineId():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getASRInfoByMachineId']
    print(url)
    rulefstheaderdic = {'V100': '7V100030F50F0'}
    rulesndheaderdic = {'S5': '70S5C9826ECB6'}
    print('规则一：\n')
    for key, value in rulefstheaderdic.items():
        requestheaders.askhomework_header['machineId'] = value
        requestheaders.askhomework_header['deviceModel'] = key
        result = requests.get(url=url, headers=requestheaders.askhomework_header)
        if value in "NMKHJGGHTYIUI":
            if 'VIVO' in result.text:
                print(key, value, '符合预期走思必驰')
            else:
                print(key, value, '不符合预期未走思必驰', result.text)
        else:
            if 'VIVO' in result.text:
                print(key, value, '符合预期走VIVO')
            else:
                print(key, value, '不符合预期未走VIVO', result.text)
    # print('\n规则二：\n')
    # ruletest(url, rulesndheaderdic, 'SBC')


def ruletest(url, headerpic, type):
    for key, value in headerpic.items():
        requestheaders.askhomework_header['machineId'] = value
        requestheaders.askhomework_header['deviceModel'] = key
        result = requests.get(url=url, headers=requestheaders.askhomework_header)
        if type in result.text:
            print(key, value, '符合预期走{0}'.format(type))
        else:
            print(key, value, '不符合预期未走{0}'.format(type), result.text)


def test_getPoetryDetailAndSecondKnow():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getPoetryDetailAndSecondKnow']
    print(url)
    # 类型，poetryName、sentence、uncertainty
    paramList = []
    param1 = {'keyWord': '望庐山瀑布', 'type': 'poetryName'}
    param2 = {'keyWord': '凄凄惨惨戚戚', 'type': 'sentence'}
    param3 = {'keyWord': '古诗吗', 'type': 'uncertainty'}
    param4 = {'keyWord': 'test', 'type': 'poetryName'}
    param5 = {'keyWord': '123', 'type': 'sentence'}
    param6 = {'keyWord': '***', 'type': 'uncertainty'}
    param7 = {'keyWord': '', 'type': 'uncertainty'}
    param8 = {'keyWord': ' ', 'type': 'uncertainty'}
    paramList.append(param1)
    paramList.append(param2)
    paramList.append(param3)
    paramList.append(param4)
    paramList.append(param5)
    paramList.append(param6)
    paramList.append(param7)
    paramList.append(param8)

    for item in paramList:
        result = requests.get(url=url, headers=requestheaders.askhomework_header, params=item)
        print(result.text)


def test_getPoetryDetailAndSecondKnowByFuzzyPoetryNameOrSentence():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet[
        'getPoetryDetailAndSecondKnowByFuzzyPoetryNameOrSentence']
    print(url)
    paramList = []
    param1 = {'fuzzyPoetryNameOrSentence': '我要复习静夜思'}
    param2 = {'fuzzyPoetryNameOrSentence': '我要复习123@#$'}
    param3 = {'fuzzyPoetryNameOrSentence': '我要复习test'}
    param4 = {'fuzzyPoetryNameOrSentence': '八百里分麾下炙'}
    param5 = {'fuzzyPoetryNameOrSentence': ' '}
    param6 = {'fuzzyPoetryNameOrSentence': ''}
    paramList.append(param1)
    paramList.append(param2)
    paramList.append(param3)
    paramList.append(param4)
    paramList.append(param5)
    paramList.append(param6)
    for item in paramList:
        result = requests.get(url=url, headers=requestheaders.askhomework_header, params=item)
        print(result.text)


def test_getPoetryDetailAndSecondKnowById():
    # id 传空 传none 均为400
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getPoetryDetailAndSecondKnowById']
    print(url)
    paramList = []
    param1 = {'14147'}
    param2 = {'-100'}
    param3 = {'0'}
    paramList.append(param1)
    paramList.append(param2)
    paramList.append(param3)
    for item in paramList:
        result = requests.get(url=url, params={'poetryId': item}, headers=requestheaders.askhomework_header)
        print(result.text)


def test_getPoetryDetailAndSecondKnowBySummaryNameOrEpigraph():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getPoetryDetailAndSecondKnowBySummaryNameOrEpigraph']
    print(url)
    paramList = []
    param1 = {'虞美人'}
    param2 = {'定风波'}
    param3 = {'望岳'}
    param4 = {'happy'}
    param5 = {'123'}
    param6 = {' '}
    paramList.append(param1)
    paramList.append(param2)
    paramList.append(param3)
    paramList.append(param4)
    paramList.append(param5)
    paramList.append(param6)
    for item in paramList:
        result = requests.get(url=url, params={'poetrySummaryNameOrEpigraph': item},
                              headers=requestheaders.askhomework_header)
        print(result.text)


def getInitialVowelTypeAndSyllableDetailInfos():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getInitialVowelTypeAndSyllableDetailInfos']
    print(url)
    paramList = []
    # 声母韵母类型：（声母/韵母/整体认读/26个字母）
    param1 = {'letter': 'a', 'letterType': '声母'}
    param2 = {'letter': 'en', 'letterType': '韵母'}
    param3 = {'letter': 'zhi', 'letterType': '整体认读'}
    param4 = {'letter': 'i', 'letterType': '26个字母'}
    param5 = {'letter': '', 'letterType': '26个字母'}
    param6 = {'letter': 'test', 'letterType': '整体认读'}
    paramList.append(param1)
    paramList.append(param2)
    paramList.append(param3)
    paramList.append(param4)
    paramList.append(param5)
    paramList.append(param6)
    for item in paramList:
        result = requests.get(url=url, params=item, headers=requestheaders.askhomework_header)
        print(result.text)


def getInitialVowelWholeAnimationByLetter():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getInitialVowelWholeAnimationByLetter']
    print(url)
    paramList = []
    param1 = {'A'}
    param2 = {'f'}
    param3 = {'zhi'}
    param4 = {'test'}
    param5 = {'123'}
    param6 = {''}
    param7 = {'tian'}
    param8 = {'a'}
    paramList.append(param1)
    paramList.append(param2)
    paramList.append(param3)
    paramList.append(param4)
    paramList.append(param5)
    paramList.append(param6)
    paramList.append(param7)
    paramList.append(param8)
    for item in paramList:
        result = requests.get(url=url, params={'letter': item}, headers=requestheaders.askhomework_header)
        print(result.text)


def getSegmentersByType():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getSegmentersByType']
    print(url)
    paramList = []
    param1 = {'str': 'muther', 'type': 'getFullOrEnglishSegmentersByStr'}
    param2 = {'str': 'I\'ae', 'type': 'getFullOrEnglishSegmentersByStr'}
    param3 = {'str': 'go ajead', 'type': 'getEglishPhraseSegmenters'}
    param4 = {'str': '123', 'type': 'getEglishPhraseSegmenters'}
    paramList.append(param1)
    paramList.append(param2)
    paramList.append(param3)
    paramList.append(param4)
    for item in paramList:
        result = requests.get(url=url, params=item, headers=requestheaders.askhomework_header)
        print(result.text)


def getArticleExtraStyleRecommendDetail():
    # goodWordType参数0 或 1 数据返回有区别
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getArticleExtraStyleRecommendDetail']
    url = url + '?recommendTypeId=14701&recommendTypeChildId=14719&goodWordType=1'
    print(url)
    result = requests.get(url=url, headers=requestheaders.askhomework_header)
    print(result.text)


def getArticleCatalogAllData():
    # goodWordType参数0 或 1 数据返回有区别
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getArticleCatalogAllData']
    url = url + '?catalogId=10519&goodWordType=1'
    result = requests.get(url=url, headers=requestheaders.askhomework_header)
    print(result.text)


def getArticleCatalogRecommend():
    # goodWordType参数0 或 1 数据返回有区别
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getArticleCatalogRecommend']
    url = url + '?catalogId=10519&goodWordType=1'
    result = requests.get(url=url, headers=requestheaders.askhomework_header)
    print(result.text)


def searchPictrueWriting():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['searchPictrueWriting']
    print(url)
    param1 = {'searchTitle': '有趣的动物', 'grade': '三年级', 'publisher': '人教版'}
    result = requests.get(url=url, params=param1, headers=requestheaders.askhomework_header)
    print(result.text)


def getLeLeCompositionBySameKey():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getLeLeCompositionBySameKey']
    print(url)
    titleList = []
    titleList.append('快乐的一天')
    titleList.append('美丽的校园')
    titleList.append('我的自行车')
    for title in titleList:
        result = requests.get(url=url, params={'k': title, 'gradeName': '三年级'},
                              headers=requestheaders.askhomework_header)
        print(result.text)


def getSnyAndBishenAndLeleCompositions():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getSnyAndBishenAndLeleCompositions']
    print(url)
    titleList = []
    titleList.append('快乐的一天')
    titleList.append('美丽的校园')
    titleList.append('我的母亲')
    for title in titleList:
        result = requests.get(url=url, params={'query': title, 'gradeName': '三年级', 'subCate': '记叙文'},
                              headers=requestheaders.askhomework_header)
        print(result.text)


def getLeLeCompositions():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getLeLeCompositions']
    print(url)
    titleList = []
    titleList.append('快乐的一天')
    titleList.append('美丽的校园')
    titleList.append('我的自行车')
    for title in titleList:
        result = requests.get(url=url, params={'k': title, 'gradeName': '三年级'},
                              headers=requestheaders.askhomework_header)
        print(result.text)


def getHotAskMethod():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getHotAskMethod']
    print(url)
    headerList = []
    v100_header = {'machineId': '7V100030F50F5', 'apkPackageName': 'com.eebbk.askhomework',
                   'apkVersionCode': '1000000', 'deviceModel': 'V100',
                   'deviceOSVersion': 'V1.0.0_200220'}
    headerList.append(v100_header)
    headerList.append(requestheaders.askhomework_header)
    for header in headerList:
        result = requests.get(url=url, headers=header)
        print(result.text)


def queryCommonModuleByHanziStrAndphoneticStr1():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['queryCommonModuleByHanziStrAndphoneticStr1']
    print(url)
    result = requests.get(url=url,
                          params={'hanziStr': '风', 'phoneticStr': 'fēn', 'gradeName': '六年级', 'editionType': '人教版'},
                          headers=requestheaders.askhomework_header)
    if 'makeCharacter' in result.text and 'writingRule' in result.text:
        print('makeCharacter、writingRule增加字段确认存在')
    else:
        print('增加字段不存在')


def getUserActiveCorpuss():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getUserActiveCorpuss']
    print(url)
    resultnotactive = requests.get(url=url, headers=requestheaders.askhomework_header)
    if 'false' in resultnotactive.text:
        print(requestheaders.askhomework_header['machineId'], '非活跃用户上报')
    requestheaders.askhomework_header.update({'machineId': '700S5940011EX'})
    resultactive = requests.get(url=url, headers=requestheaders.askhomework_header)
    if 'true' in resultactive.text:
        print(requestheaders.askhomework_header['machineId'], '活跃用户上报')


def getListBySkillName():
    urlTest = 'http://ite.eebbk.net/ask-homework' + askhomewor_testUrlSet.AskUrlSet['getListBySkillName']
    urlFormal = 'http://askhomework.eebbk.net' + askhomewor_testUrlSet.AskUrlSet['getListBySkillName']
    paramList = ['字词', '古诗词', '国学', '作文', '拼音字母', '语文听写', '语文点读', '单位换算', '数学概念', '数学口诀']
    for item in paramList:
        print('*****************', item, '********************')
        for header in [requestheaders.askhomework_header, requestheaders.askhomework_header_S3P,
                       requestheaders.askhomework_header_S1W,requestheaders.askhomework_header_V100]:
            print('--------------', header['deviceModel'], '-------------------------')
            result = requests.get(url=urlTest, headers=header, params={'skillName': item})
            # print(result.text)
            objdata = demjson.decode(result.text)
            if objdata['data']:
                pass
            else:
                print('返回数据均为空')
            result_s5 = requests.get(url=urlFormal, headers=header, params={'skillName': item})
            # print(result_s5.text)
            objdata_s5 = demjson.decode(result_s5.text)
            if objdata_s5['data']:
                pass
            else:
                print('返回数据均为空')
            if objdata_s5['data'] == objdata['data']:
                print(item, '数据一致')
            else:
                print(item, '数据不一致')


def getSkillClassChildListByClassId(classidlist):
    print(classidlist)
    urlTest = 'http://ite.eebbk.net/ask-homework' + askhomewor_testUrlSet.AskUrlSet['getSkillClassChildListByClassId']
    urlFormal = 'http://askhomework.eebbk.net' + askhomewor_testUrlSet.AskUrlSet['getSkillClassChildListByClassId']
    print(urlTest)
    for item in classidlist:
        print('************************一级id:',item,'****************************')
        for header in [requestheaders.askhomework_header, requestheaders.askhomework_header_S3P,
                       requestheaders.askhomework_header_S1W,requestheaders.askhomework_header_V100]:
            print('--------------', header['deviceModel'], '-------------------------')
            result = requests.get(url=urlTest, headers=header, params={'classId': item})
            objdata = demjson.decode(result.text)
            if objdata['data']:
                pass
            else:
                print(item, '数据为空')
            result_s5 = requests.get(url=urlFormal, headers=header, params={'classId': item})
            objdata_s5 = demjson.decode(result_s5.text)
            if objdata_s5['data']:
                pass
            else:
                print(item, '数据为空')
            if objdata_s5['data'] == objdata['data']:
                print('class id 是', item, '数据一致')
            else:
                print('class id 是', item, '数据不一致')


def getTopOperates():
    classidlist = []
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getTopOperates']
    print(url)
    result = requests.get(url=url, headers=requestheaders.askhomework_header)
    print(result.text)
    objdata = demjson.decode(result.text)
    if 'picType' in result.text:
        print('正确返回 有pictype 字段')
        for item in objdata['data']['skillClassVos']:
            classidlist.append(item['id'])
        return classidlist
    else:
        print('错误 无picType字段')
        return classidlist


def getLegalComplianceH5():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getLegalComplianceH5']
    print(url)
    result = requests.get(url=url, headers=requestheaders.askhomework_header)
    print(result.text)


def getThemeSkin():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getThemeSkin']
    print(url)
    result = requests.get(url=url, headers=requestheaders.askhomework_header)
    objdata = demjson.decode(result.text)
    if objdata['data']:
        for item in objdata['data']:
            if 'horizontalScreenMinImg' in item and 'verticalScreenMinImg' in item and 'horizontalThumbnailImg' in item:
                print('horizontalScreenMinImg、verticalScreenMinImg、horizontalThumbnailImg 新增字段返回')
                pass
            else:
                print(item['id'], '没有新增的字段')
    else:
        print('getThemeSkin data 为空', objdata)


def getArticleExtraMoreStyles():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getArticleExtraMoreStyles']
    print(url)
    result = requests.get(url=url, headers=requestheaders.askhomework_header, params={'gradeName': '三年级'})
    print(result.text)


def getBishenCompositions():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['getBishenCompositions']
    print(url)
    result = requests.get(url=url, headers=requestheaders.askhomework_header,
                          params={'gradeName': '三年级', 'query': '美丽的校园', 'subCate': '记叙文'})
    print(result.text)


def test_uploadActivationInfo():
    url = manager.getDomain() + askhomewor_testUrlSet.AskUrlSet['uploadActivationInfo']
    print(url)
    for device in [('S3 Prow', 'QXQXQXQXQXQXQ'), ('S1W', 'Q1Q1q1q1q1q1q'), ('V100', 'gugugugugugug'),
                   ('S5', 'uuuuuuuuuuuuu'), ('S6', 'ooiiooppuuyuh')]:
        requestheaders.askhomework_header.update({'deviceModel': device[0], 'machineId': device[1]})
        result = requests.post(url=url, headers=requestheaders.askhomework_header, params={'activationType': 'awaken'})
        print(result.text)


if __name__ == '__main__':
    # test_getASRInfoByMachineId()
    # test_getPoetryDetailAndSecondKnow()
    # test_getPoetryDetailAndSecondKnowByFuzzyPoetryNameOrSentence()
    # test_getPoetryDetailAndSecondKnowById()
    # test_getPoetryDetailAndSecondKnowBySummaryNameOrEpigraph()
    # getInitialVowelTypeAndSyllableDetailInfos()
    # getInitialVowelWholeAnimationByLetter()
    # getSegmentersByType()
    # getArticleExtraStyleRecommendDetail()
    # getArticleCatalogAllData()
    # getArticleCatalogRecommend()
    # searchPictrueWriting()
    # getLeLeCompositionBySameKey()
    # getSnyAndBishenAndLeleCompositions()
    # getLeLeCompositions()
    # getHotAskMethod()
    # queryCommonModuleByHanziStrAndphoneticStr1()
    # getUserActiveCorpuss()
    # ----------------------一次迭代-------------------------
    getListBySkillName()
    classidlist = getTopOperates()
    getSkillClassChildListByClassId(classidlist)
    getLegalComplianceH5()
    getThemeSkin()
    getArticleExtraMoreStyles()
    getBishenCompositions()
    # ---------------------唤醒激活-----------------------
    # test_uploadActivationInfo()
