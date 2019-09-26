# @File  : SearchAndAsk.py
# @Author: LiuXingsheng
# @Date  : 2019/3/19
# @Desc  : 一点一问相关接口

import requests, demjson

# REQUESTDOMAIN = 'http://test.eebbk.net'
# REQUESTDOMAIN = 'http://ite.eebbk.net'
REQUESTDOMAIN = 'http://pointquestion.eebbk.net'

def getheaders():
    return {'machineId':'700H38300018B','accountId':'4051922','apkPackageName':'com.eebbk.askhomework','apkVersionCode':'1',
            'deviceModel':'S3 Pro','deviceOSVersion':'V1.0.0_180409'}

def getAnswerLockInfo(modulename, machineId):
    url = REQUESTDOMAIN + '/pointquestion-app/app/answerLockInfo/getAnswerLockInfo'
    param = {'model': modulename, 'machineId': machineId}
    result = requests.get(url=url, params=param,headers=getheaders())
    content = demjson.decode(result.text)
    print(result.text)
    return content['data']['isOpen']


def insertOrUpdateAnswerLockInfo(moduleName, machineId, switchStatus, times):
    url = REQUESTDOMAIN + '/pointquestion-app/app/answerLockInfo/insertOrUpdateAnswerLockInfo'
    param = {'model': moduleName, 'machineId': machineId, 'isOpen': switchStatus, 'askTimesLimit': times}
    result = requests.post(url=url, data=param,headers=getheaders())
    # print(result.text)


def getAnswerLockWarning(moduleName):
    url = REQUESTDOMAIN + '/pointquestion-app/app/answerLockWarning/getAnswerLockWarning'
    param = {'model': moduleName}
    result = requests.get(url=url, params=param,headers=getheaders())
    print(result.text)

# 首次调用时需要先调用插入更新接口
# def main():
#     insertOrUpdateAnswerLockInfo('文理科搜题','700H38300018B',1,'13')


def answerLockSuit():
    """
    一点一问答案锁测试用例
    :return:
    """
    newswitch = 10
    calModule = '计算器'
    searchModule = '文理科搜题'
    machineId = '700H38300018B'
    modulelist = []
    modulelist.append(calModule)
    modulelist.append(searchModule)
    for item in modulelist:
        print('修改前: ')
        switch = getAnswerLockInfo(item, machineId)
        if switch == 1:
            newswitch = 0
        else:
            newswitch = 1
        insertOrUpdateAnswerLockInfo(item, machineId, newswitch, 13)
        print('修改后: ')
        getAnswerLockInfo(item, machineId)
    # 阈值测试
    print('------------------阈值测试-------------------------')
    for item in modulelist:
        getAnswerLockWarning(item)


def main():
    answerLockSuit()


if __name__ == '__main__':
    main()
