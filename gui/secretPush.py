# @File  : secretPush.py
# @Author: LiuXingsheng
# @Date  : 2019/5/28
# @Desc  :
import requests, time


def sendRobotSceret(accountId, machineId, secretContent, secretType, times, clock):
    """
    推送密语
    :param accountId: 账号Id
    :param machineId: 机器序列号
    :param secretContent: 推送的密语内容
    :param secretType: 1-文本、2-表情、3-爱的约定、4-语音
    :param times: 发送次数
    :param clock: 请求间隔（秒）
    :return:
    """
    url = 'https://api-develop.robot.okii.com/robot/api/secretSend/sendSecret'
    param = {'accountId': str(accountId), 'machineId': str(machineId), 'secretContent': str(secretContent),
             'secretType': str(secretType)}
    header = {'phoneModel': 'iphone X', 'phoneSysver': 'IOS 12.1'}
    for i in range(int(times)):
        time.sleep(int(clock))
        result = requests.post(url=url, params=param, headers=header)
        print(result.status_code)
        print(result.text)
    print('请求完成')


def main():
    sendRobotSceret('7433440', 'f467bf34ff85afa5', '测试发送的内容', '1', 5, 1)
    # sendRobotSceret('7433440', 'f467bf34ff85afa5', '测试发送的内容', '1', 5, 1)


if __name__ == '__main__':
    main()
