# @File  : ergodicTest.py
# @Author: LiuXingsheng
# @Date  : 2018/12/19
# @Desc  : 遍历测试
import requests, demjson, hashlib, time


def str_md5(str):
    m = hashlib.md5()
    m.update(str.encode())
    return m.hexdigest()


def login():
    """
    登录接口
    :return:
    """
    url = "https://api.ztest.cn/user/login"
    params = {'data': {'username': '15813805642', 'password': str_md5('ss123456')}}
    result = requests.post(url=url, json=params)
    print(result.text)
    data = demjson.decode(result.text)
    if not data['errorCode'] == 0:
        print("登录失败")
    return data


def getToken(appId, appSecret):
    """
    获取token接口
    :return:
    """
    url = 'https://api.ztest.cn/user/token'
    now = int(time.time())
    now_format = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))
    param = {'data': {'appId': appId, 'appSecret': appSecret, 'time': now_format}}
    result = requests.post(url=url, json=param)
    data = demjson.decode(result.text)
    print(data)
    if not data['errorCode'] == 0:
        print("获取失败")
    return data


def deviceList(token):
    """
    获取当前在线设备列表
    :param token:
    :return:
    """
    listUrl = 'https://api.ztest.cn/user/device_list'
    param = {'data': {'token': token, 'isOwn': 1}}
    result = requests.post(url=listUrl, json=param)
    listInfo = demjson.decode(result.text)
    if not listInfo['errorCode'] == 0:
        print('获取列表失败')
    print(listInfo)
    return listInfo


def createTask(token, pkg):
    """
    创建任务
    :param token:
    :param pkg:
    :return:
    """
    create_task_url = "https://api.ztest.cn/task/add"
    arg_table = {
        "data": {
            "token": token,
            "appId": 0,  # 预安装应用的id都设置0
            "duration": 20,  # 测试时长，分钟
            "devices": "369",  # 执行测试任务的设备ID，可在极测平台上查看， 多个设备id用逗号分开
            "packageName": pkg  # 要测试的包名
        }
    }
    result = requests.post(url=create_task_url, json=arg_table)
    data = demjson.decode(result.text)
    if not data["errorCode"] == 0:
        print("创建任务失败")
    print("创建任务：" + str(result.text))
    return data


def report(token, taskId):
    reportUrl = "https://api.ztest.cn/report/detail"
    param = {'data': {'token': token, 'taskId': taskId}}
    result = requests.post(url=reportUrl, json=param)
    data = demjson.decode(result.text)
    if not data['errorCode'] == 0:
        print('任务创建失败')
    print('上报任务：' + result.text)
    return data


def main():
    data = login()
    tokenInfo = getToken(data['data']['appId'], data['data']['appSecret'])
    taskInfo = createTask(tokenInfo['data']['token'], 'com.eebbk.synchinese')

    # # report(tokenInfo['data']['token'], taskInfo['data']['taskId'])
    # deviceList('4D61B9523F627642E9CF899D8E2AF651')


if __name__ == '__main__':
    main()
