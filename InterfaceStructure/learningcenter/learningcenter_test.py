# @File  : learningcenter_test.py
# @Author: LiuXingsheng
# @Date  : 2020/4/27
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import learningcenter_testUrlSet
import requests
import demjson
from collections import Counter

manager = domainManager.DomainManager()
manager.setDomainType(constants.TestDomainType_Asia)
manager.setItemName(constants.learningcenter)


def getlearningcenterHeader():
    return {'machineId': '700S593001AE5', 'apkPackageName': 'test', 'apkVersionCode': '1000000', 'deviceModel': 'V100',
            'deviceOSVersion': 'V1.0.0_180409'}


def getUrl(path):
    url = manager.getDomain() + learningcenter_testUrlSet.learningcenterUrlSet[path]
    print(url)
    return url


def getBookList():
    booklist = []
    nulllist = []
    url = getUrl('getBookList')
    result = requests.get(url=url, params={'accountId': '4051922'}, headers=getlearningcenterHeader())
    if result.status_code == 200:
        objdata = demjson.decode(result.text)
        if 'data' in objdata:
            for item in objdata['data']:
                if 'bookInfo' in item and 'taskInfo' in item:
                    booklist.append(item['bookInfo']['id'])
                else:
                    nulllist.append('无book 或 taskInfo返回')
    else:
        print('请求出错')
    print('获取的书本列表',booklist,'异常书本列表',nulllist)
    return booklist


def getUserHomeTask(booklist):
    nulllist = []
    taskiddaylist = []
    daylearntasklist = []
    url = getUrl('getUserHomeTask')
    for book in booklist:
        result = requests.get(url=url, params={'accountId': '4051922', 'bookId': book},
                              headers=getlearningcenterHeader())
        if result.status_code == 200:
            objdata = demjson.decode(result.text)
            if 'data' in result.text:
                if 'dayTasks' in result.text and 'unitTaskInfo' in result.text:
                    for item in objdata['data']['dayTasks']:
                        # 天任务id
                        taskiddaylist.append(item['id'])
                        for item1 in item['learnTasks']:
                            # 天学习任务id
                            daylearntasklist.append(item1['id'])
                else:
                    nulllist.append(book)
        else:
            print('请求出错')
    repeat_1 = dict(Counter(taskiddaylist))
    print('天任务重复taskid', {key: value for key, value in repeat_1.items() if value > 1})
    repeat_2 = dict(Counter(daylearntasklist))
    print('天学习任务重复taskid', {key: value for key, value in repeat_2.items() if value > 1})
    print('无 dayTasks 或 unitTaskInfo',nulllist)


def getUserLearningRoute(booklist):
    nulllist = []
    nullnamelist = []
    url = getUrl('getUserLearningRoute')
    for book in booklist:
        result = requests.get(url=url, params={'accountId': '4051922', 'bookId': book},
                              headers=getlearningcenterHeader())
        if result.status_code == 200:
            objdata = demjson.decode(result.text)
            if 'data' in objdata:
                for item in objdata['data']:
                    if 'userRouteUnitInfoVo' in item and 'userRouteUnitInfoVo' in item:
                        if item['userRouteUnitInfoVo']['name']:
                            pass
                        else:
                            nullnamelist.append(item['userRouteUnitInfoVo']['id'])
                        if item['userRouteUnitTaskVo']['unitTaskId']:
                            pass
                        else:
                            nulllist.append(item['userRouteUnitTaskVo']['id'])
                    else:
                        nulllist.append('无 userRouteUnitInfoVo 或 userRouteUnitInfoVo 返回')
        else:
            print('请求出错')
    print('单元名为空的', nullnamelist, 'userRouteUnitTaskVo中单元任务id为空的', nulllist)


if __name__ == '__main__':
    booklist = getBookList()
    getUserHomeTask(booklist)
    getUserLearningRoute(booklist)
