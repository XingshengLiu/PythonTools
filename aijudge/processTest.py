# @File  : processTest.py
# @Author: LiuXingsheng
# @Date  : 2019/9/11
# @Desc  : 智能诊断与推荐接口测试
import random_pic
import requests
import demjson

TEST_DOMAIN = 'http://testaliyun.eebbk.net'
NAME_ITEM = '/ai-diagnosis-app'
URL_DETAIL = '0'
URL_SIMILAR = '1'

TEACHER = '刘1'


def getHeader():
    return {'machineId': '700S519040201', 'deviceModel': 'S5', 'deviceOSVersion': 'V1.0.0_190309',
            'accountId': 'lxs_135'}


def getAllDiagnoseTopics(subCpList):
    """
    整体接口 根据所有的章节id获取诊断题目
    :param subList:
    :return:
    """
    for sectionICp in subCpList:
        getDiagnoseSuit(sectionICp)


def getDiagnoseTopicBySectionId(sectionId, qtId):
    """
    根据章节id获取诊断题目
    :return:
    """
    # 根据章节id获取的诊断题目列表
    print('------------------根据章节id获取的诊断题目列表----------------------------')
    idList = []
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getDiagnoseTopicBySectionId'
    # 章节id
    param = {'sectionId': sectionId, 'qtId': qtId}
    result = requests.get(url=url, params=param, headers=getHeader())
    jsonobj = demjson.decode(result.text)
    print('根据章节id获取诊断题目参数是：{0},返回数据是：{1}'.format(param, jsonobj))
    if jsonobj['data'] is None:
        return [], ''
    for item in jsonobj['data']['questionInfoList']:
        idList.append(item['questionId'])
    return idList, jsonobj['data']['nqt']


def wrapperUserAnswer(userItemList):
    """
    生成用户答案
    :param userItemList:
    :return:
    """
    userAnsList = []
    userChoice = ''
    for userItem in userItemList:
        if userItem == 1:
            userChoice = 'A'
        elif userItem == 2:
            userChoice = 'B'
        elif userItem == 3:
            userChoice = 'C'
        else:
            userChoice = 'D'
        userAnsList.append(userChoice)
    return userAnsList


def reportedAnswerResults(comprehensiveList):
    """
    上报答题情况
    :return:
    """
    idList = comprehensiveList[0]
    answersList = []
    strIdList = str(idList).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
    for i in range(len(idList)):
        answersList.append(random_pic.randint(0, 1))
    strAnswerList = ''.join(str(answersList).replace('[', '').replace(']', '').split())
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/reportedAnswerResults'
    param = {
        'topicIds': strIdList,
        'answers': strAnswerList,
    }
    print('上报答题情况请求参数是：', param)
    result = requests.post(url=url, params=param, headers=getHeader())
    print(result.content.decode('utf-8'))


def submitAnswerInfo(comprehensiveList, sectionId, sectionName):
    """
    提交答题信息
    :return:
    """
    print('---------------提交答题信息--------------------')
    idList = comprehensiveList[0]
    nqt = comprehensiveList[1]
    print('idList 是：', idList)
    answersList = []
    userItemList = []
    UserAnswerTimeList = []
    usedTotalTime = 0
    for i in range(len(idList)):
        answersList.append(random_pic.randint(0, 1))
        userItemList.append(random_pic.randint(1, 4))
        UserAnswerTimeList.append(random_pic.randint(5, 30))
    userAnsersList = wrapperUserAnswer(userItemList)
    for i in UserAnswerTimeList:
        usedTotalTime += i
    strAnswerList = ''.join(str(answersList).replace('[', '').replace(']', '').split())
    strUserAnswersList = ''.join(str(userAnsersList).replace('[', '').replace(']', '').replace('\'', '').split())
    strUserAnswerTimeList = ''.join(str(UserAnswerTimeList).replace('[', '').replace(']', '').split())
    strIdList = ''.join(str(idList).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '').split())
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/submitAnswerInfo'
    param = {
        'sectionId': sectionId,
        'sectionName': sectionName,
        'topicIds': strIdList,
        'answers': strAnswerList + ',',
        'userAnswers': strUserAnswersList,
        'answerTimeAlone': strUserAnswerTimeList, 'answerTime': usedTotalTime,
        'nqt': nqt}
    result = requests.post(url=url, params=param, headers=getHeader())
    print('提交答题结果请求参数是:{0} \n返回数据是：{1}'.format(param, result.content.decode('utf-8')))


def getDiagnoseResult():
    """
    获取学生诊断结果
    :return:
    """
    print("----------------------------获取学生诊断结果----------------------------")
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getDiagnoseResult'
    param = {'userInfo': TEACHER}
    result = requests.get(url=url, headers=getHeader(), params=param)
    print('获取学生诊断结果 请求参数是：{0}\n返回结果是{1}'.format(param, result.text))


def getFatherMenu():
    """
    获取年级教材版本
    :return:
    """
    menuIdList = []
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getFatherMenu'
    result = requests.get(url=url, headers=getHeader())
    if result.status_code != requests.codes.ok:
        print(result.status_code)
        return []
    content = result.content.decode('utf-8')
    contentobj = demjson.decode(content)
    if contentobj['data'] is not None:
        for item in contentobj['data']:
            for item_new in item['subMenu']:
                menuIdList.append(item_new['menuId'])
    return menuIdList


def getMenuByFatherMenuId(menuIdList):
    """
    获取二级菜单根据一级菜单ID
    :return:
    """
    subCouplelist = []
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getMenuByFatherMenuId'
    for item in menuIdList:
        param = {'fatherMenuId': str(item)}
        result = requests.get(url=url, params=param, headers=getHeader())
        if result.status_code != requests.codes.ok:
            print(result.status_code)
            return []
        objecontent = demjson.decode(result.text)
        print(objecontent)
        if objecontent['data'] is not None:
            for item in objecontent['data']:
                for subitem in item['subMenu']:
                    subCouplelist.append((subitem['menuId'], subitem['menuName'], subitem['qtId']))
    # print('获取的最内层sectionid 是', sublist)
    return subCouplelist


def getKnowledgeByMenuId(subCoupleList):
    """
    根据菜单id获取知识点
    :return:
    """
    print('---------------------根据菜单id获取知识点-----------------')
    subList = []
    for itemCp in subCoupleList:
        subList.append(itemCp[0])
    knowledgeIdList = []
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getKnowledgeByMenuId'
    for item in subList:
        sectionList = []
        result = requests.post(url=url, headers=getHeader(), params={'menuId': str(item)})
        objContent = demjson.decode(result.text)
        print('menuId 为：{0} 返回结果 ：{1} '.format(str(item), objContent))
        if objContent['data'] is not None:
            for newitem in objContent['data']:
                sectionList.append((item, newitem['knowledgeId']))
        knowledgeIdList.append(sectionList)
    return knowledgeIdList


def getQuestionByKnowledgeId(knowledgeIdList):
    """
    根据知识点获取练习题
    :param knowledgeIdList:
    :return:
    """
    practiceList = []
    print('--------------------根据知识点获取练习题------------------------')
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getQuestionByKnowledgeId'
    print('共有多少个小节：', len(knowledgeIdList))
    for sectionitem in knowledgeIdList:
        for knowledgeitem in sectionitem:
            result = requests.get(url=url,
                                  params={'sectionId': str(knowledgeitem[0]), 'knowledgeId': str(knowledgeitem[1])},
                                  headers=getHeader())
            contentobj = demjson.decode(result.text)
            print('sectionID 是：{0}，knowledegeId是：{1} 返回数据是：{2}'.format(str(knowledgeitem[0]), str(knowledgeitem[1]),
                                                                       result.text))
            if contentobj['data'] is not None:
                for item in contentobj['data']:
                    practiceList.append(item['questionId'])
            else:
                pass
    return practiceList


def coupleBackTopic(practiceList):
    """
    提交题目反馈
    :param practiceList:
    :return:
    """
    print('---------------------提交题目反馈--------------------')
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/coupleBackTopic'
    for topic in practiceList:
        param = {'topicId': str(topic), 'coupleBacks': random_pic.randint(1, 6),
                 'coupleBackDesc': '这是接口生成的反馈描述', 'contactInfo': '456789'}
        result = requests.post(url=url, params=param, headers=getHeader())
        print('提交反馈 参数是：{0}，返回结果是：{1}'.format(param, result.text))


def getSyncKnowledgeByKnowledgeId(knowledgeIdList):
    """
    根据知识点Id获取同步知识点
    :return:
    """
    errorPointList = []
    funcPointList = []
    print('--------------------------------根据知识点Id获取同步知识点--------------------------------')
    url = TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getSyncKnowledgeByKnowledgeId'
    for sectionitem in knowledgeIdList:
        for knowledgeitem in sectionitem:
            result = requests.get(url=url, params={'knowledgeId': str(knowledgeitem[1])}, headers=getHeader())
            contentobj = demjson.decode(result.text)
            print('请求参数是：{0}， 返回数据是{1}'.format(str(knowledgeitem[1]), result.text))
            if contentobj['data'] is not None:
                for erroritem in contentobj['data']['errorPointList']:
                    errorPointList.append((str(knowledgeitem[1]), erroritem['id']))
                for funcitem in contentobj['data']['konwFuncPointList']:
                    funcPointList.append((str(knowledgeitem[1]), funcitem['id']))
    return (errorPointList, funcPointList)


def getCourseDetailById(comprehensiveList, requestType):
    """
    根据方法技巧点、易错id获取教程详情
    :return:
    """
    errorList = comprehensiveList[0]
    funcList = comprehensiveList[1]
    print('--------------------------------根据方法技巧点或者易错id获取教程详情、获取相似练习题--------------------------------')
    print('--------------------------------易错id获取--------------------------------')
    print('易错id：', errorList)
    sendlooprequest(errorList, requestType)
    print('--------------------------------方法技巧点id获取--------------------------------')
    print('方法技巧id：', funcList)
    sendlooprequest(funcList, requestType)


def sendlooprequest(dataList, requestType):
    url = getUrl(requestType)
    if requestType == URL_SIMILAR:
        for combineIds in dataList:
            result = requests.get(url=url,
                                  params={'pointInfoId': str(combineIds[1]), 'knowledgeId': str(combineIds[0])},
                                  headers=getHeader())
            print('获取相似题 知识点id：{0}，方法技巧点或易错点id为：{1}，返回数据为：{2}'.format(str(combineIds[0]), str(combineIds[1]),
                                                                      result.text))
    else:
        for combineIds in dataList:
            result = requests.get(url=url,
                                  params={'pointInfoId': str(combineIds[1])},
                                  headers=getHeader())
            print('获取课程详情 方法技巧点或易错点id为：{0}，返回数据为：{1}'.format(str(combineIds[1]), result.text))


def getUrl(requestType):
    if requestType == URL_SIMILAR:
        return TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getSimilarExercisesById'
    else:
        return TEST_DOMAIN + NAME_ITEM + '/app/diagnosis/getCourseDetailById'


def getDiagnoseResultByQuestion(comprehensiveList):
    """
    模型接口 获取诊断结果
    :param idList:
    :return:
    """
    idList = comprehensiveList[0]
    nqt = comprehensiveList[1]
    answersList = []
    for i in range(len(idList)):
        answersList.append(random_pic.randint(0, 1))
    strAnswerList = str(answersList)
    trueStrAnswerList = ''.join(strAnswerList.split())
    url = TEST_DOMAIN + '/recommend-system-api/diagnose/api/getDiagnoseResultByQuestion'
    param = {'qt': nqt, 'answer': trueStrAnswerList}
    print('请求参数是：', param)
    result = requests.get(url=url, params=param)
    print(result.text)


def getDiagnoseSuit(sectionCp):
    """
    诊断题目 上报答案，获取结果 测试套件
    :param sectionId:
    :return:
    """
    sectionId = sectionCp[0]
    sectionName = sectionCp[1]
    qtId = sectionCp[2]
    comprehensiveList = getDiagnoseTopicBySectionId(sectionId, qtId)
    # reportedAnswerResults(comprehensiveList)
    submitAnswerInfo(comprehensiveList, sectionId, sectionName)
    # getDiagnoseResult()
    print('*******************************************************')


def specialTest(subCoupleList):
    urlGetSectionList = 'http://172.28.162.21:9011/diagnosis/test/getSectionList'
    urlGetDiaResult = 'http://172.28.162.21:9011/diagnosis/test/getDiagnoseResult'
    result = requests.post(url=urlGetSectionList, params={'sectionId': 1})
    if result.status_code != requests.codes.ok:
        print(result.status_code)
        return
    objData = demjson.decode(result.text)
    print(len(objData['data']['knowledgeList']))
    knowledgeHas = objData['data']['questionStateT']
    for knowledge in knowledgeHas:
        print(knowledge)
        result = requests.post(url=urlGetDiaResult, params={'sectionId': '1', 'userState': knowledge})
        print(result.text)
    for itemCp in subCoupleList:
        sectionid = itemCp[0]
        result = requests.post(url=urlGetSectionList, params={'sectionId': sectionid})
        if result.status_code != requests.codes.ok:
            print(result.status_code)
            return
        objData = demjson.decode(result.text)
        knowledgeHas = objData['data']['questionStateT']
        for knowledge in knowledgeHas:
            print(knowledge)
            result = requests.post(url=urlGetDiaResult, params={'sectionId': sectionid, 'userState': knowledge})
            print(result.text)


def test():
    numberList = [1, 2, 3, 4, 5]
    numberTuple = (1, 2, 3, 4,5)
    print(numberList[:2])
    print(numberList[:-2])
    print(numberList[1:])
    print(numberList[-2:])
    # numberList.reverse()
    # print(numberList)

    # for i in range(len(numberTuple) - 1, -1, -1):
    #     print(numberTuple[i])

def rightStrip(tempStr,splitStr):
    endindex = tempStr.rfind(splitStr)
    while endindex != -1 and endindex == len(tempStr) - 1:
         tempStr = tempStr[:endindex]
         endindex = tempStr.rfind(splitStr)
    return tempStr

def leftStrip(tempStr,splitStr):
    startindex = tempStr.find(splitStr)
    while startindex == 0:
        tempStr = tempStr[startindex+1:]
        startindex = tempStr.find(splitStr)
    return tempStr

if __name__ == '__main__':
    """
    注释获取的subList就是sectionidList 可以用所有的section 去获取诊断题目
    """
    # -------------获取章节id及sectionid--------------------
    # menuIdList = getFatherMenu()
    # subCoupleList = getMenuByFatherMenuId(menuIdList)
    # --------------获取诊断题目，答题，获取诊断结果-------------
    # comprehensiveList = getDiagnoseTopicBySectionId(3, 1)
    # reportedAnswerResults(idList)
    # getDiagnoseResult()
    # getAllDiagnoseTopics(subCoupleList)
    # --------------模型诊断接口（非暴露的业务接口）----------------------
    # getDiagnoseResultByQuestion(comprehensiveList)
    # ---------------获取练习题、详细信息课程详情， 相似题目等-----------
    # knowledgeIdList = getKnowledgeByMenuId(subCoupleList)
    # practiceList = getQuestionByKnowledgeId(knowledgeIdList)
    # coupleBackTopic(practiceList)
    # (errorList, funcList) = getSyncKnowledgeByKnowledgeId(knowledgeIdList)
    # # 获取相似题是从大数据获取 获取课程详情是直接从内容获取
    # print('\n*******************此处分割*************************\n')
    # getCourseDetailById((errorList, funcList), URL_DETAIL)
    # getCourseDetailById((errorList, funcList), URL_SIMILAR)
    # specialTest([])
    test()
    # str = '***H***'
    # print(str)
    # print(leftStrip(str,'*'))
    # print(rightStrip(str,'*'))

