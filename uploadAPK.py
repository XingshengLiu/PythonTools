# @File  : uploadAPK.py
# @Author: LiuXingsheng
# @Date  : 2018/12/27
# @Desc  :
import requests

domain = 'http://test.eebbk.net/voice-material-warehouse'


def uploadAPK():
    url = 'http://172.28.3.75:9002/uapi/uploadapp/upload'
    param = {'apiKey': '0E52ACD565355804A0AB368602E53F1C',
             'data': {'fileupload': '@/bbkstf/XTC_buildFile/app/pad/Parentsupport.apk'}}
    result = requests.post(url=url, data=param)
    print(result.text)


# uploadAPK()


def uploadFeedbackData():
    url = domain + '/api/feedback/uploadFeedbackData'
    params = {'voiceJosnContent': ''''[{'machineType': 'S3 Pro', 'machineId': '700H38300018B', 'appVersion': 'V2.1.0', 'searchKey': 'ah-1',
               'intention': '生字',
               'recognitionContent': '天空', 'skipStructure': '生字', 'voiceUrl': '语意URL', 'feedbackContent': '不好用',
               'feedbackImg': 'url://img',
               'phoneNumber': '13456', 'module': 'askhomework', 'photographImg': 'img//'}]'''}
    # params = {''''[{'machineType': 'S3 Pro', 'machineId': '700H38300018B', 'appVersion': 'V2.1.0', 'searchKey': 'ah-1',
    #            'intention': '生字',
    #            'recognitionContent': '天空', 'skipStructure': '生字', 'voiceUrl': '语意URL', 'feedbackContent': '不好用',
    #            'feedbackImg': 'url://img',
    #            'phoneNumber': '13456', 'module': 'askhomework', 'photographImg': 'img//'}]'''}
    result = requests.post(url=url, params=params)
    # result = requests.post(url=url, data=params, headers={'Content-Type': 'application/json'})

    print(result.text)
    print(result.status_code)


def main():
    uploadFeedbackData()


if __name__ == '__main__':
    main()
