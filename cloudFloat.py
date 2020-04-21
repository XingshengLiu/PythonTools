# @File  : cloudFloat.py
# @Author: LiuXingsheng
# @Date  : 2018/11/19
# @Desc  :
import requests, os, xlrd, xlsxwriter, demjson, json, time, random_pic
from xpinyin import Pinyin
from io import StringIO
from io import BytesIO
import os
import pickle
import argparse, json
from InterfaceStructure.resources import requestheaders

TESTDOMAIN = 'http://test.eebbk.net'
VIDEODOMAIN = 'http://videodata.eebbk.net'
EXEDOMAIN = 'http://exercise.lewen.com'
AIVOICE = 'http://wisdomvoice.eebbk.net'
AIDESK = 'http://wisdomdesktop.eebbk.net'
ALPHA_VOICE_DOMAIN = 'http://ite.eebbk.net/wisdomvoice'
ALPHA_DESK_DOMAIN = 'http://ite.eebbk.net/wisdomdesktop'

VIDEODATAITEM = '/videoData'
VOICEITEM = '/wisdomvoice'
DESKITEM = '/wisdomdesktop'
M1000_ITEM = '/N001_M1000_api'


# 好题精炼
def getSocialExercise():
    paramList = []
    url = TESTDOMAIN + '/wisdomVoice/getSocialExercise?'
    params1 = getSocialData('六年级', '数学', '人教版', '上册', '综合运用百分数的知识解决生活中的实际问题')
    params2 = getSocialData('三年级', '数学', '人教版', '下册', '面积单位之间的换算')
    params3 = getSocialData('四年级', '数学', '人教版', '下册', '加减法混合简便运算')
    paramList.append(params1)
    paramList.append(params2)
    paramList.append(params3)
    for params in paramList:
        result = requests.get(url=url, params=params)
        print(result.text)


def getSocialData(gradeName, subjectName, publisher, termName, knowledgeName):
    return {'gradeName': str(gradeName), 'subjectName': str(subjectName), 'publisher': str(publisher),
            'termName': str(termName), 'knowledgeName': str(knowledgeName)}


def getFamousExercise():
    paramList = []
    url = TESTDOMAIN + M1000_ITEM + '/wisdomVoice/getFamousExercise?'
    params1 = getFamousData('三年级', '数学', '北师大版', '上册', '混合运算', '小熊购物', 0)
    params2 = getFamousData('四年级', '语文', '北师大版', '上册', '第一单元', '师恩难忘', 0)
    params3 = getFamousData('六年级', '英语', '河北教育版', '上册', 'At the Airport', 'Lesson 1', 0)
    params4 = getFamousData('一年级', '数学', '人教版', '下册', '认识图形', '认识图形', 0)
    paramList.append(params1)
    paramList.append(params2)
    paramList.append(params3)
    paramList.append(params4)
    for params in paramList:
        result = requests.get(url=url, params=params)
        print(result.text)


def getFamousData(gradeName, subjectName, publisher, termName, chapterName, childChapterName, isCatalogue):
    return {'gradeName': str(gradeName), 'subjectName': str(subjectName), 'publisher': str(publisher),
            'termName': str(termName), 'chapterName': str(chapterName), 'childChapterName': str(childChapterName),
            'isCatalogue': str(isCatalogue)}


# 名师辅导班
def getWisdomVideo():
    paramList = []
    url = VIDEODOMAIN + '/openInterface/getWisdomVideo?'
    params1 = getgetVideoData('语文', '三年级', '人教版', '上册', '金色的草地', '预习')
    params2 = getgetVideoData('数学', '四年级', '人教版', '下册', '鸡兔同笼', '复习')
    params3 = getgetVideoData('英语', '五年级', '人教版精通', '上册', 'Unit 1 We have new friends', '预习')
    paramList.append(params1)
    paramList.append(params2)
    paramList.append(params3)
    for params in paramList:
        result = requests.get(url=url, params=params)
        print(result.text)


def getgetVideoData(subject, grade, publisher, volume, courseName, type):
    return {'subject': str(subject), 'grade': str(grade), 'publisher': str(publisher), 'volume': str(volume),
            'courseName': str(courseName), 'type': str(type)}


def getClassTypeInfoByNameForWisdom():
    paramList = []
    url = VIDEODOMAIN + '/openInterface/getClassTypeInfoByNameForWisdom?'
    params1 = getClassTypeData('语文', '五年级', '人教版', '上册', '语言基础班')
    params2 = getClassTypeData('数学', '四年级', '人教版', '下册', '同步提高班')
    params3 = getClassTypeData('英语', '三年级', '人教版精通', '上册', '同步基础班')
    paramList.append(params1)
    paramList.append(params2)
    paramList.append(params3)
    for params in paramList:
        result = requests.get(url=url, params=params, headers=getCommonHeader())
        print(result.text)

    header = {'Content-type': ''}


def getClassTypeData(subject, grade, publisher, volume, classType):
    return {'subject': str(subject), 'grade': str(grade), 'publisher': str(publisher), 'volume': str(volume),
            'classType': str(classType)}


def getTeacherInfoByNameForWisdom():
    paramList = []
    url = VIDEODOMAIN + '/openInterface/getTeacherInfoByNameForWisdom'
    params1 = getTeacherInfoData('语文', '五年级', '胡一帆')
    params2 = getTeacherInfoData('数学', '四年级', '赵然')
    params3 = getTeacherInfoData('英语', '三年级', '屈慧贞')
    params4 = getTeacherInfoData('数学', '一年级', '兰海')
    paramList.append(params1)
    paramList.append(params2)
    paramList.append(params3)
    paramList.append(params4)
    for params in paramList:
        result = requests.get(url=url, params=params, headers=getCommonHeader())
        print(result.text)


def getTeacherInfoData(subject, grade, teacherName):
    return {'subject': str(subject), 'grade': str(grade), 'teacherName': str(teacherName)}


def getVideoPlayInfo():
    paramList = []
    url = AIVOICE + '/api/video/getVideoPlayInfo'
    params1 = getVideoInfoData('语文', '花的学校')
    paramList.append(params1)
    for params in paramList:
        result = requests.get(url=url, params=params, headers=getCommonHeader())
        print(result.text)


def getVideoInfoData(subject, texts):
    return {'subject': str(subject), 'texts': str(texts)}


# 云孚语义测试
class Bean:
    mean = ''
    speech = ''
    slice = ''
    spell = ''
    noSpell = ''
    withSpell = ''
    resultNoSpellmean = ''
    resultWithSpellmean = ''
    resultNoSpell = ''
    resultWithSpell = ''


# 生成拼音
def generateSpell():
    beanList = []
    workbook = xlrd.open_workbook(os.getcwd() + '\\data.xlsx')
    sheet = workbook.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        bean = Bean()
        bean.mean = sheet.cell_value(row, 0).strip().replace('/', '-')
        bean.speech = sheet.cell_value(row, 1).strip()
        bean.slice = sheet.cell_value(row, 2).strip()
        beanList.append(bean)
    for bean in beanList:
        p = Pinyin()
        spellList = p.get_pinyin(bean.slice, " ")
        phonetices = spellList.split(" ")
        str1 = str(phonetices).replace('[', '{')
        str2 = str1.replace(']', '}')
        str3 = str2.replace('\'', '\"')
        str4 = str3.replace(' ', '')
        bean.spell = str4
    i = 1
    workbook = xlsxwriter.Workbook(os.getcwd() + '\\data_former.xlsx')
    ws = workbook.add_worksheet(u'Sheet1')
    ws = workbook.get_worksheet_by_name('Sheet2')
    ws.write(i, 3, 'test')
    for bean in beanList:
        ws.write(i, 0, bean.mean)
        ws.write(i, 1, bean.speech)
        ws.write(i, 2, bean.slice)
        i = i + 1
    workbook.close()
    return beanList


# 云孚语义测试
def cloudFloatSpellMeaningTool():
    beanList = generateSpell()
    urlNoSpell = "http://113.108.235.182:8174/bbk-nlp/npl/intentionRecognition"
    urlWithSpell = "http://113.108.235.182:8174/bbk-nlp/npl/intentionRecognition/phonetics"
    for bean in beanList:
        if len(bean.slice) == 0 or (bean.mean == '空'):
            bean.slice = ' '
            bean.resultNoSpellmean = ' '
            bean.resultNoSpell = '不计入'
            bean.resultWithSpellmean = ' '
            bean.resultWithSpell = '不计入'
            bean.noSpell = ' '
            bean.withSpell = ' '
        else:
            paramsNoSpell = {'sentence': bean.slice}
            paramsWithSpell = {'phonetics': bean.spell}
            paramsWithSpell.update(paramsNoSpell)
            resultNoSpell = requests.get(url=urlNoSpell, params=paramsNoSpell)
            resultWithSpell = requests.request(method="GET", url=urlWithSpell, params=paramsWithSpell)
            infoNoSpell = demjson.decode(resultNoSpell.text)
            infoWithSpell = demjson.decode(resultWithSpell.text)
            if 'data' in infoNoSpell:
                infoNSP2 = infoNoSpell['data']
                bean.noSpell = str(infoNSP2)
                if 'intent' in infoNSP2:
                    infoNSP3 = infoNSP2['intent']
                    if 'yfIntent' in infoNSP3:
                        bean.resultNoSpellmean = (str(infoNoSpell['data']['intent']['yfIntent']).strip()).split('__')[1]
                    else:
                        bean.resultNoSpellmean = str(infoNSP2['intent'])
                    if bean.resultNoSpellmean == bean.mean or '我不太会呢' in str(infoNSP2):
                        bean.resultNoSpell = '1'
                    else:
                        bean.resultNoSpell = '0'
            if 'data' in infoWithSpell:
                infoWSP2 = infoWithSpell['data']
                bean.withSpell = str(infoWSP2)
                if 'intent' in infoWSP2:
                    infoWSP3 = infoWSP2['intent']
                    if 'yfIntent' in infoWSP3:
                        bean.resultWithSpellmean = \
                            (str(infoWithSpell['data']['intent']['yfIntent']).strip()).split("__")[1]
                    else:
                        bean.resultWithSpellmean = str(infoWSP2['intent'])
                    if bean.resultWithSpellmean == bean.mean or '我不太会呢' in str(infoWSP2):
                        bean.resultWithSpell = '1'
                    else:
                        bean.resultWithSpell = '0'
    i = 1
    workbook = xlsxwriter.Workbook(os.getcwd() + '\\data_result.xlsx')
    ws = workbook.add_worksheet(u'Sheet1')
    writeTheTitle(ws)
    for bean in beanList:
        ws.write(i, 0, bean.mean)
        ws.write(i, 1, bean.speech)
        ws.write(i, 2, bean.slice)
        ws.write(i, 3, bean.spell)
        ws.write(i, 4, bean.noSpell)
        ws.write(i, 5, bean.resultNoSpellmean)
        ws.write(i, 6, bean.resultNoSpell)
        ws.write(i, 7, bean.withSpell)
        ws.write(i, 8, bean.resultWithSpellmean)
        ws.write(i, 9, bean.resultWithSpell)
        i = i + 1
    workbook.close()
    beanList.clear()


class BaikeBean:
    sentence = ''
    expect = ''
    data = ''
    result = ' '


def generateBaikeDta():
    beanlist = []
    workbook = xlrd.open_workbook(os.getcwd() + '\\baike.xlsx')
    sheet = workbook.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        bean = BaikeBean()
        bean.sentence = sheet.cell_value(row, 0).strip()
        bean.expect = sheet.cell_value(row, 1).strip()
        beanlist.append(bean)
    return beanlist


def baikeTools():
    url = 'http://113.108.235.182:8174/bbk-nlp/baike/api'
    baikelist = generateBaikeDta()
    for bean in baikelist:
        requestdata = requests.get(url=url, params='sentence=' + str(bean.sentence))
        data = demjson.decode(requestdata.text)
        bean.data = requestdata.text
        print(data['data']['key'])
        if str(data['data']['key']).replace('\'', '').replace('[', '').replace(']', '') == bean.expect:
            bean.result = '正确'
        else:
            bean.result = '错误'
    i = 1
    workbook = xlsxwriter.Workbook(os.getcwd() + '\\百科结果.xlsx')
    ws = workbook.add_worksheet(u'Sheet1')
    for bean in baikelist:
        ws.write(i, 0, bean.sentence)
        ws.write(i, 1, bean.expect)
        ws.write(i, 2, bean.data)
        ws.write(i, 3, bean.result)
        i = i + 1
    workbook.close()
    baikelist.clear()


# 智慧语音
def getCommonHeader():
    return {'machineId': '700H38300018B', 'apkPackageName': 'com.eebbk.synchinese', 'apkVersionCode': '1002',
            'deviceModel': 'S3 Pro', 'deviceOsVersion': 'V1.3.0_181119'}


def getClassTypeInfoByNameForWisdom_voice():
    paramList = []
    url = AIVOICE + '/api/video/getClassTypeInfoByNameForWisdom'
    params1 = getClassTypeVoiceData('三年级', '语文', '人教版', '上册', '', '', '', '我的预习 我做主', '', '同步基础班', '预习')
    params2 = getClassTypeVoiceData('四年级', '数学', '人教版', '上册', '', '', '', '亿以内数的读法与写法', '', '同步基础班', '复习')
    paramList.append(params1)
    paramList.append(params2)
    header = getCommonHeader()
    for param in paramList:
        result = requests.get(url=url, params=param, headers=header)
        print(result.text)


def getClassTypeVoiceData(grade, subject, publisher, volume, module, unit, unitName, lesson, texts, classType, intent):
    return {'grade': str(grade), 'subject': str(subject), 'publisher': str(publisher), 'volume': str(volume),
            'module': str(module), 'unit': str(unit), 'unitName': str(unitName), 'lesson': str(lesson),
            'texts': str(texts),
            'classType': str(classType), 'intent': str(intent)}


def getTeacherInfoByNameForWisdom_voice():
    paramList = []
    url = AIVOICE + '/api/video/getTeacherInfoByNameForWisdom'
    params1 = getTeacherInfoVoice('沙苗苗', '预习')
    params2 = getTeacherInfoVoice('兰海', '复习')
    params3 = getTeacherInfoVoice('王雨洁', '复习')
    paramList.append(params1)
    paramList.append(params2)
    paramList.append(params3)
    header = getCommonHeader()
    for params in paramList:
        result = requests.get(url=url, headers=header, params=params)
        print(result.text)


def getTeacherInfoVoice(teacherName, intent):
    return {'teacherName': str(teacherName), 'intent': str(intent)}


# 智慧桌面
def getAskHomeworkData():
    url = AIDESK + '/app/askhomework/getAskHomeworkData'
    params = {'machineId': '700H38300018B', 'province': '广东省', 'city': '东莞市', 'grade': '三年级'}
    result = requests.get(url=url, params=params)
    print(result.text)


def getMarketStoreData():
    url = AIDESK + '/app/marketStore/getMarketStoreData'
    header = {'deviceModel': 'S3 Pro', 'deviceOSVersion': 'V1.3.0_181119',
              'machineId': '700H38300018B'}
    param = getSync_VideoData('广东省', '广州市', '五年级', '2')
    result = requests.get(url=url, params=param, headers=header)
    print(result.text)


def getVideoTraningData():
    """
    获取名师辅导班信息
    :return:
    """
    url = AIDESK + '/app/recommendVideo/getVideoTraningData'
    headerList = []
    header2 = {'machineId': '700S5940002EX', 'deviceModel': 'S5', 'apkVersionCode': '2050204'}  # 四年级
    header3 = {'machineId': '70S3A95002541', 'deviceModel': 'S3 Prow', 'apkVersionCode': '2050204'}  # 三年级
    # header2 = {'machineId': '700H3840008BM', 'deviceModel': 'S3 Pro', 'apkVersionCode': '2050206'}  # 四年级
    # header3 = {'machineId': '700H3840008BM', 'deviceModel': 'S3 Pro', 'apkVersionCode': '2050200'}  # 三年级
    # headerList.append(header1)
    headerList.append(header2)
    headerList.append(header3)
    # headerList.append(header4)
    for header in headerList:
        result = requests.get(url=url, headers=header)
        print(result.text)


def getSyncSubjectData():
    headerList = []
    url = AIDESK + '/app/syncSubject/getSyncSubjectData'
    # url = TESTDOMAIN + DESKITEM + '/app/syncSubject/getSyncSubjectData'
    header1 = {'machineId': '700H384001DDU', 'apkVersionCode': '2050201', 'deviceModel': 'H7000'}
    # header2 = {'machineId': '50S3S10000092', 'apkVersionCode': '2050202', 'deviceModel': 'S3 Pro'}
    header2 = {'machineId': '70S3A95002541', 'apkVersionCode': '2050201', 'deviceModel': 'S3 Prow'}
    headerList.append(header1)
    headerList.append(header2)
    param = getSync_VideoData('广东省', '深圳市', '五年级', '3')
    for header in headerList:
        result = requests.get(url=url, params=param, headers=header)
        print(result.text)


# subjectTypeId 1 语文 2英语 3数学
def getSync_VideoData(province, city, grade, subjectTypeId):
    return {'province': str(province), 'city': str(city), 'grade': str(grade), 'subjectTypeId': str(subjectTypeId)}


def writeTheTitle(ws):
    ws.write(0, 0, '云孚意图')
    ws.write(0, 1, '思必驰意图')
    ws.write(0, 2, '根据思必驰意图生成的句子')
    ws.write(0, 3, '拼音')
    ws.write(0, 4, '不带拼音返回数据')
    ws.write(0, 5, '不带拼音意图')
    ws.write(0, 6, '不带拼音结果')
    ws.write(0, 7, '带拼音返回数据')
    ws.write(0, 8, '带拼音意图')
    ws.write(0, 9, '带拼音结果')


def readFile():
    with open('D:\\test.txt', 'r+') as f:
        while True:
            s = f.read(3)
            if s == '':
                break
            print(s)


def readStringIO():
    f = StringIO('hello\nHi!\nGoodBye!')
    while True:
        s = f.readline()
        if s == '':
            break
        print(s)


def writeByteIO():
    f = BytesIO()
    count = f.write('中文'.encode('utf-8'))
    print(count)
    print(f.getvalue())
    print(f.getbuffer())


def readByteIO():
    f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
    print(f.read())
    StringIO.seek(0, 2)


def test_pickle():
    d = dict(name='Bob', age='20', score=80)
    print(d)
    print(pickle.dumps(d))


class Student():
    def __init__(self, name, age, scor):
        self.name = name
        self.age = age
        self.scor = scor


def test_pck():
    s = Student('Bob', 20, 88)
    print(json.dumps(s, default=lambda obj: obj.__dict__))


def stringIOtest():
    # test = StringIO('abcqwe')
    # print(test.getvalue())
    # print(test.tell())
    # test.write("d")
    # print(test.getvalue())
    # print(test.tell())
    # test.write("f")
    # print(test.getvalue())
    # print(test.tell())
    # test.seek(0, 2)
    # print(test.tell())
    # test.write('l')
    # print(test.getvalue())
    # print(test.tell())
    # test.write('m')
    # print(test.getvalue())
    # test.seek(1,0)
    # print(test.read())
    # print(os.name)
    # print(os.environ)
    # print(os.environ.get('PROGRAMW6432'))
    print(os.path.abspath('.'))
    path = os.path.join(os.path.abspath('.'), 'test')
    print(path)
    os.mkdir(path)
    test = os.path.split(path)
    print(test)
    os.rmdir(path)


def sendRobotSceret():
    url = 'https://api-develop.robot.okii.com/robot/api/secretSend/sendSecret'
    param = {'accountId': '7433440', 'machineId': '9d4fb401241aa1f8', 'secretContent': 'please call me daddy',
             'secretType': '1'}
    header = {'phoneModel': 'iphone X', 'phoneSysver': 'IOS 12.1', 'token': '2a8d881ea0b6aca987f09658b28122d6',
              'accountId': '7433440'}
    # for i in range(3):
    #     time.sleep(10)
    #     print(param)
    print(param)
    result = requests.post(url=url, params=param, headers=header)
    print(result.text)
    print('请求完成')


def testArgumetn():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--test_dir', dest='test_dir')
    parser.add_argument('--label_file', dest='label_file')
    args = parser.parse_args()
    print('参数是：', args)


def migiration():
    urllist = [
        '/api/basicInfo/getGrades?subjectName=%E8%AF%AD%E6%96%87',
        '/api/basicInfo/getPublishers?gradeName=%E4%B8%89%E5%B9%B4%E7%BA%A7&subjectName=%E8%AF%AD%E6%96%87',
        '/api/basicInfo/getVolumes',
        '/api/bookCatalog/getBookCatalogInfo?province=%E5%B9%BF%E4%B8%9C&city=%E4%B8%9C%E8%8E%9E&centerGrade=1&grade=1&subject=%E8%AF%AD%E6%96%87&publisher=%E4%BA%BA%E6%95%99%E7%89%88&volume=%E4%B8%8A&intent=%E5%A4%8D%E4%B9%A0',
        '/api/bookCatalog/getBookSimpleCatalogInfo?province=%E5%B9%BF%E4%B8%9C&city=%E4%B8%9C%E8%8E%9E&centerGrade=1&grade=1&subject=%E8%AF%AD%E6%96%87&publisher=%E4%BA%BA%E6%95%99%E7%89%88&volume=%E4%B8%8A&intent=%E5%A4%8D%E4%B9%A0',
        '/api/bookCatalog/getSyntheticalInfo?province=%E5%B9%BF%E4%B8%9C&city=%E4%B8%9C%E8%8E%9E&centerGrade=1&grade=1&subject=%E8%AF%AD%E6%96%87&publisher=%E4%BA%BA%E6%95%99%E7%89%88&volume=%E4%B8%8A&intent=%E5%A4%8D%E4%B9%A0',
        '/api/exercise/getExampleExerciseInfo?province=%E5%B9%BF%E4%B8%9C&city=%E4%B8%9C%E8%8E%9E&centerGrade=1&grade=1&subject=%E8%AF%AD%E6%96%87&publisher=%E4%BA%BA%E6%95%99%E7%89%88&volume=%E4%B8%8A&intent=%E5%A4%8D%E4%B9%A0',
        '/api/exercise/getFamousBookExerciseInfo?province=%E5%B9%BF%E4%B8%9C&city=%E4%B8%9C%E8%8E%9E&centerGrade=1&grade=1&subject=%E8%AF%AD%E6%96%87&publisher=%E4%BA%BA%E6%95%99%E7%89%88&volume=%E4%B8%8A&intent=%E5%A4%8D%E4%B9%A0',
        '/api/exercise/getFamousBookExerciseInfo?province=广东省&centerGrade=三年级&city=东莞市&subject=语文&intent=复习课文',
        '/api/video/getClassTypeInfoByNameForWisdom?province=广东省&centerGrade=三年级&city=东莞市&subject=英语&intent=看视频&classType=同步提高班',
        '/api/video/getTeacherInfoByNameForWisdom?province=广东省&centerGrade=三年级&teacherName=子衿老师&city=东莞市&intent=看视频',
        '/api/video/getVideoPlayInfo?province=广东省&centerGrade=三年级&city=东莞市&subject=语文&intent=预习课文',
        '/api/bookCatalog/getBookSimpleCatalogInfo?province=广东省&centerGrade=三年级&city=东莞市&subject=语文&grade=三年级&intent=预习找书',
        '/api/exercise/getFamousBookExerciseInfo?province=广东省&centerGrade=三年级&texts=天地人&city=东莞市&subject=语文&intent=复习课文',
        '/api/exercise/getExampleExerciseInfo?province=广东省&centerGrade=三年级&city=东莞市&subject=数学&intent=复习知识点&knowledge=加法的意义']
    for urltes in urllist:
        result = requests.get(url=AIVOICE + urltes, headers=requestheaders.askhomework_header_S3P)
        print(result.text)
    for urlt in ['/app/h110wisdomdesktop/getSynEnglishWordGrades?grade=三年级&machineId=1','/app/h110wisdomdesktop/getSynChineseWordGrades?grade=三年级&machineId=1']:
        result = requests.get(url=AIDESK + urlt, headers=requestheaders.askhomework_header_S3P)
        print(result.text)


def main():
    # getWisdomVideo()
    # 智慧语音
    migiration()
    getClassTypeInfoByNameForWisdom()
    getTeacherInfoByNameForWisdom()
    getVideoPlayInfo()
    getClassTypeInfoByNameForWisdom_voice()
    getTeacherInfoByNameForWisdom_voice()
    # 智慧桌面
    getVideoTraningData()
    getSyncSubjectData()
    getAskHomeworkData()
    getMarketStoreData()
    # 以下不变
    # getSocialExercise()
    # getFamousExercise()
    # cloudFloatSpellMeaningTool()
    # readFile()
    # # readStringIO()
    # writeByteIO()
    # readByteIO()
    # stringIOtest()
    # test_pickle()
    # test_pck()
    # baikeTools()
    # sendRobotSceret()
    # testArgumetn()


if __name__ == '__main__':
    main()
