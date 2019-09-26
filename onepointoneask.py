# @File  : onepointoneask.py
# @Author: LiuXingsheng
# @Date  : 2019/1/7
# @Desc  : 语音收集demo 已发布的项目
import requests, time, xlsxwriter, os

# DOMAIN = 'http://test.eebbk.net'
Item = '/voice-material-warehouse'
DOMAIN = 'http://ite.eebbk.net'
FormalDomain = 'http://pointquestion.eebbk.net'


def getheaders():
    return {'machineId': '700H38300018B', 'accountId': '4051922', 'apkPackageName': 'com.eebbk.askhomework',
            'apkVersionCode': '1',
            'deviceModel': 'S3 Pro', 'deviceOSVersion': 'V1.0.0_180409'}


def uploadFeedbackData():
    url = DOMAIN + Item + '/api/feedback/uploadFeedbackData'
    requestPram = {
        'voiceJosnContent': '''[{"machineType":"S3 Pro", "machineId":"700H38300018B", "appVersion":"2.0.0.0", "searchKey":"key", "intention":"生字", "recognitionContent":"天空", "skipStructure":"生字", "voiceUrl":"" ,"feedbackContent":"用户反馈内容","feedbackImg":"","phoneNumber":"123456"}]'''}
    result = requests.request(method='POST', url=url, params=requestPram)
    print(result.text)


def uploadFeedbackData1():
    url = DOMAIN + Item + '/api/feedback/uploadFeedbackData1'
    requestPram = {
        'voiceJosnContent': '''{"machineType":"S3 Pro", "machineId":"700H38300018B", "appVersion":"2.0.0.0", "searchKey":"key", "intention":"生字", "recognitionContent":"天空", "skipStructure":"生字", "voiceUrl":"" ,"feedbackContent":"用户反馈内容","feedbackImg":"","phoneNumber":"18850521234","module":"小布问作业","photographImg":""}''',
        'reasonKeys': '识别不准'}
    result = requests.request(method='POST', url=url, params=requestPram)
    print(result.text)


def uploadSearchEffectAndFeedbackData():
    url = DOMAIN + Item + '/api/feedback/uploadSearchEffectAndFeedbackData'
    requestPram = {
        'voiceJosnContent': '''{"machineType":"S3 Pro", "machineId":"700H38300018B", "appVersion":"2.0.0.0", "searchKey":"key", "intention":"生字", "recognitionContent":"天空", "skipStructure":"生字", "voiceUrl":"" ,"feedbackContent":"用户反馈内容","feedbackImg":"","phoneNumber":"18850521234","module":"小布问作业","photographImg":""}''',
        'reasonKeys': '识别不准', 'type': 'askHomework', 'isHelpful': '1'}
    result = requests.request(method='POST', url=url, params=requestPram)
    print(result.text)


def getFeedbackReasons():
    url = DOMAIN + Item + '/api/feedbackReason/getFeedbackReasons'
    requestPram = {
        'type': 'askHomework'}
    result = requests.request(method='GET', url=url, params=requestPram)
    print(result.text)


def uploadPointQuestionVoiceBaseData():
    url = DOMAIN + Item + '/api/voiceMaterial/uploadPointQuestionVoiceBaseData'
    requestParam = {
        'voiceJosnContent': '''[{"beforeVoiceUrl":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2019/01/07/700H384000DBR/100615461_bc02fd76ad6e8b9d.pcm","appVersion":"3.0.0.0","hasResult":1,"intention":"字的读音","machineId":"H3000S0000435","machineType":"S3 Pro","photographImg":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2018/12/29/H3000S0000435/142013121_905039b72fc3748f.jpg","pointXY":"","recognitionContent":"这个字怎么写","resultImg":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2018/12/29/H3000S0000435/142013121_0349c6870560579c.png","sbcRecordId":"7d4c0ab986818e9239dc0fe52ed42d12","searchKey":"","skipStructure":"point_and_ask_word_list","voiceUrl":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2018/12/29/H3000S0000435/142013121_58666f29ef8c5c1e.pcm"}]'''}
    result = requests.request(method='POST', url=url, params=requestParam)
    print(result.text)


def uploadPointQuestionVoiceBaseData_test():
    url = DOMAIN + Item + '/api/voiceMaterial/uploadPointQuestionVoiceBaseData'
    requestParams = '[{"beforeVoiceUrl":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2019/01/07/700H384000DBR/100615461_bc02fd76ad6e8b9d.pcm","appVersion":"3.0.0.0","hasResult":1,"intention":"字的读音","machineId":"H3000S0000435","machineType":"S3 Pro","photographImg":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2018/12/29/H3000S0000435/142013121_905039b72fc3748f.jpg","pointXY":"","recognitionContent":"这个字怎么写","resultImg":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2018/12/29/H3000S0000435/142013121_0349c6870560579c.png","sbcRecordId":"7d4c0ab986818e9239dc0fe52ed42d12","searchKey":"","skipStructure":"point_and_ask_word_list","voiceUrl":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2018/12/29/H3000S0000435/142013121_58666f29ef8c5c1e.pcm"}]'


def quick():
    url = 'http://socialexercise.eebbk.net/examination/cover/patchCheckUserCover'
    params = {'content': '100'}
    cookie = {'BBK_ROUTE_FLAG': 'social-exercise'}
    result = requests.post(url=url, cookies=cookie, params=params)
    print(result.text)


def quick_english():
    url = 'http://englishlisten.eebbk.net/english/englishCover/patchCheckUserCover'
    params = {'content': '100'}
    cookie = {'BBK_ROUTE_FLAG': 'englishlisten'}
    result = requests.post(url=url, cookies=cookie, params=params)
    print(result.text)


def testInterface():
    url = 'http://223.223.186.115:8085/Ise/cloudAtlas/retrieve_image_bbk'
    param = {'db_uid': 'ise_bbk_001', 'db_seckey': 'bbk_001', 'ws': '', 'pt_x': '100', 'pt_y': '100',
             'img_stream': open('reg/p013.jpg', 'rb')}
    result = requests.post(url=url, data=param)
    print(result.text)


class ReturnContent(object):
    content = ''
    gradeId = ''
    quesitnId = ''


def searchKnowledgePoint():
    url = FormalDomain + '/pointquestion-app/app/topicProcess/searchKnowledgePoint'
    gradeIdList = ['16', '17', '18', '19', '20']
    resultList = []
    with open('quesId.txt', 'r') as f:
        id = f.read()
    quesidList = id.split('\n')
    for grade in gradeIdList:
        for quesId in quesidList:
            contentBean = ReturnContent()
            result = requests.get(url=url,
                                  params={'accountId': 'test', 'gradeId': str(grade), 'questionId': str(quesId)},
                                  headers=getheaders())
            contentBean.content = result.text
            contentBean.gradeId = grade
            contentBean.quesitnId = quesId
            resultList.append(contentBean)
    workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + '点播测试结果.xlsx')
    ws = workbook.add_worksheet(u'sheet1')
    ws.write(0, 0, 'gradeId')
    ws.write(0, 1, 'questionId')
    ws.write(0, 2, '返回内容')
    column = 1
    for item in resultList:
        ws.write(column, 0, item.gradeId)
        ws.write(column, 1, item.quesitnId)
        ws.write(column, 2, item.content)
        column += 1
    workbook.close()


def judgeHealth():
    url = 'http://test.eebbk.net/find-eroticism/api/eroticism/judgeImage'
    param = {'resourceId': '12',
             'imageUrl': 'http://android-englishtalk.eebbk.net/englishtalk/2019/06/03/700S38203EFBJ/125952411_58bcce2ecfa0984d.jpg',
             'packageName': 'tes33t'}
    result = requests.post(url=url, params=param)
    print(result.text)


def main():
    # for i in range(500):
    #     quick()
    #     quick_english()
    #     time.sleep(45)
    # uploadFeedbackData()
    # uploadFeedbackData1()
    # uploadSearchEffectAndFeedbackData()
    # getFeedbackReasons()
    # uploadPointQuestionVoiceBaseData()
    # testInterface()
    searchKnowledgePoint()
    # judgeHealth()


if __name__ == '__main__':
    main()
