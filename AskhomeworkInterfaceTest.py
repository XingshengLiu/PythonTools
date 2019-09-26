# @File  : AskhomeworkInterfaceTest.py
# @Author: LiuXingsheng
# @Date  : 2019/3/16
# @Desc  :
import requests, demjson

# REQUESTDOMAIN = 'http://test.eebbk.net/ask-homework'
# REQUESTDOMAIN = 'http://ite.eebbk.net/ask-homework'
REQUESTDOMAIN = 'http://askhomework.eebbk.net'

def getMachineAnswerSwitch(machienId):
    """
    获取答案锁
    :param machienId:
    :return:
    """
    url = REQUESTDOMAIN + '/service/answerswitch/getMachineAnswerSwitch'
    params = {'machineId': machienId}
    result = requests.get(url=url, params=params, headers=getHeaders(machienId))
    print(result.text)
    content = demjson.decode(result.text)
    if 'answerSwitch' in result.text:
        switch = content['data']['answerSwitch']
        if switch == 0:
            newSwitch = 1
        else:
            newSwitch = 0
        return (True, switch, newSwitch, machienId)
    else:
        print('请求错误')
        return False


def uploadMachineAnswerSwitch(tupleresponse):
    """
    修改答案锁并查看是否修改成功
    :param tupleresponse:
    :return:
    """
    status = tupleresponse[0]
    originalswitch = tupleresponse[1]
    newswitch = tupleresponse[2]
    machineId = tupleresponse[3]
    url = REQUESTDOMAIN + '/service/answerswitch/uploadMachineAnswerSwitch'
    params = {'machineId': machineId, 'switchValue': newswitch}
    if status == True:
        # 此处的修改答案锁开关无需判断取值，只需查看后一次的查询接口是否和之前的状态只发生变化
        requests.post(url=url, data=params, headers=getHeaders(machineId))
        tuplecheck = getMachineAnswerSwitch(machineId)
        if not tupleresponse:
            print('修改状态失败')
        else:
            # 对比修改答案的前后，两个开关状态不一致即可，0或者是1
            if tuplecheck[1] != originalswitch:
                print('修改成功')
            else:
                print('修改失败')
    else:
        print('获取状态失败')


def getHeaders(machineId):
    return {'machineId': machineId, 'accountId': '4051922', 'apkPackageName': 'com.eebbk.askhomework',
            'apkVersionCode': '1.0.0', 'deviceModel': 'H20', 'deviceOSVersion': 'V1.0.0_180409'}


def main():
    machineId = '700H38300018B'
    tupleresoinse = getMachineAnswerSwitch(machineId)
    uploadMachineAnswerSwitch(tupleresoinse)


if __name__ == '__main__':
    main()
