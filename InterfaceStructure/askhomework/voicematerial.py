# @File  : voicematerial.py
# @Author: LiuXingsheng
# @Date  : 2019/12/24
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import askhomewor_testUrlSet
from InterfaceStructure.resources import requestheaders
import requests

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.voice_material)


def test_uploadPointQuestionVoiceBaseData():
    url = manager.getDomain() + askhomewor_testUrlSet.VoiceUrlSet['uploadPointQuestionVoiceBaseData']
    print(url)
    result = requests.post(url=url, params={
        'voiceJosnContent':
            '[{"machineType":"S3 Pro",  "machineId":"700S3S8910F44Z",  "appVersion":"2.2.8.8",  "searchKey":"秋天", '
            ' "intention":"词语主题",  "recognitionContent":"识别描写秋天的词语文本",  "skipStructure":"word_type",  '
            '"voiceUrl":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2019/04/11/700S5910005BU/111342006_c4b21d053cf1b767.pcm", '
            ' "photographImg":"32412214124",  "beforeVoiceUrl":"2141421421",  "pointXY":"1399,1543",  "ocrContent":"hahahaha", '
            ' "segmentation":"秋天",  "command":"pointAsk",  "searchMethod":"语音输入搜索",  "questionId":"368",  '
            '"questionPicUrl":"http://file.eebbk.net/server-test/cloudIDN/test/2019/03/01/153047285_bd29cff2e6d7a575.png",  '
            '"systemVersion":"1.X.X.4",  "jumpWorkHelp":"Y",  "topicType":"题意理解",  "nlpType":"SBC","asrType":"SBC"}]'},
                           headers=requestheaders.askhomework_header)
    print(result.text)


def test_uploadVoiceBaseData():
    url = manager.getDomain() + askhomewor_testUrlSet.VoiceUrlSet['uploadVoiceBaseData']
    print(url)
    result = requests.post(url=url, params={
        'voiceJosnContent': '[{"machineType":"S3 Pro", "machineId":"700S3S8910F44Z", "appVersion":"2.2.8.8", "searchKey":"秋天",'
                            ' "intention":"词语主题", "recognitionContent":"识别描写秋天的词语文本", "skipStructure":"word_type", '
                            '"voiceUrl":"http://dailyspokenenglish-dn.eebbk.net/askhomework/2019/04/11/700S5910005BU/111342006_c4b21d053cf1b767.pcm", '
                            '"command":"pointAsk", "searchMethod":"语音输入搜索", "systemVersion":"1.X.X.X", '
                            '"nlpType":"智能语义类型NLP(SBS)","asrType":"VIVO"}]'}, headers=requestheaders.askhomework_header)
    print(result.text)


if __name__ == '__main__':
    test_uploadPointQuestionVoiceBaseData()
    test_uploadVoiceBaseData()
