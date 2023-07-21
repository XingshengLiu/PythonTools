# @File  : synscript.py
# @Author: LiuXingsheng
# @Date  : 2023/7/13
# @Desc  :

import requests
import json
from pymysql import connect
import pymysql
import datetime
import collections
import schedule
import configparser



def getDBCon():
    cf = configparser.ConfigParser()
    cf.read(r'cfg.ini', encoding='utf-8')
    return connect(
        host=cf.get('database', 'host'),
        port=cf.getint('database', 'port'),
        user=cf.get('database', 'user'),
        password=cf.get('database', 'password'),
        db=cf.get('database', 'db'),
        charset=cf.get('database', 'charset')
    )


def getConst():
    global WeeklyType
    global RecordType
    global QuestionAppList
    cf = configparser.ConfigParser()
    cf.read(r'cfg.ini', encoding='utf-8')
    WeeklyType = cf.getint("inserttype", "WeeklyType")
    RecordType = cf.getint("inserttype", "RecordType")
    QuestionAppList = cf.get("badcase", "QuestionAppList").split(',')


def getCoveragedApp():
    coveragedapplist = []
    res = requests.get("http://172.28.2.27:8899/appServiceInfo/getAllApp")
    if res.status_code == 200:
        objdata = json.loads(res.text)
        coveragedapplist = objdata['data']
    else:
        print('getAppApp error,info is-->', res)
    return coveragedapplist


def getUsedApp():
    usedapplist = collections.defaultdict(set)
    url = 'http://172.28.2.27:8899/appCoverageReport/queryCoverageReport'
    res = requests.post(url=url,
                        json={"startIndex": 0, "pageSize": 50, "app": None, "workerList": None, "version": None})
    print(res.text)
    if res.status_code == 200 and 'reports' in res.text:
        objdata = json.loads(res.text)
        for report in objdata['data']['reports']:
            # -1 说明该版本未能正常接入，还在调试，版本不统计
            if report['lineCoverage'] != -1:
                usedapplist[report['jenkinsTaskName']].add(report['buildNum'].replace('J', ''))
            else:
                pass
    else:
        print('queryCoverageReport接口报错', res.text)
    return usedapplist


def getTestingAppFromDevops(startDate, endDate):
    testedAppList = collections.defaultdict(list)
    token = getToken()
    if 'null_token' in token:
        print('获取toke 失败')
    else:
        url = 'https://xtc-devsecops.okii.com/api/common/open/versionGroupAppTests/6254d39556c3dc14690125d6'
        header = {'Authorization': 'Bearer ' + token}
        res = requests.post(url=url, headers=header,
                            json={'startDate': startDate, 'endDate': endDate, 'groupName': ['商店版本']})
        if res.status_code == 200:
            objdata = json.loads(res.text)
            infolist = objdata['data']
            if len(infolist) != 0:
                for appinfo in infolist[0]['versions']:
                    for version in appinfo['proposedTests']:
                        testedAppList[version['jenkinsTaskName']].append(version['jenkinsBuildNumber'])
            else:
                print('获取提测应用列表失败，长度为空', res.text)
        else:
            print('获取提测应用列表失败', res.text)
    return testedAppList


def getToken():
    url = 'https://sso.okii.com/auth/realms/SSO/protocol/openid-connect/token'
    res = requests.post(url=url, data={'client_id': 'DevSecOpsFeedBackEnd',
                                       'client_secret': '5f2b47db-3756-4852-a075-1a1bda0ba475',
                                       'redirect_url': 'xtc-devsecops.okii.com', 'grant_type': 'password',
                                       'username': 'xtc-robot', 'password': 'robot'})
    if res.status_code == 200 and 'access_token' in res.text:
        objdata = json.loads(res.text)
        return objdata['access_token']
    else:
        return 'null_token'


def insertCoverageUsedData(insertType, record):
    con = getDBCon()
    if (insertType == WeeklyType):
        sql = 'update t_usedrate_weekly set should_use=%s,actually_used=%s,used_rate=%s,create_time=%s where id=1'
    else:
        sql = 'insert into t_usedrate_record(should_use,actually_used,used_rate,create_time)values(%s,%s,%s,%s)'
    try:
        with con.cursor() as cursor:
            count = cursor.execute(sql, record)
            con.commit()
            print('insertTyp {0},对应表插入的数据条数为{1}'.format(insertType, count))
    except pymysql.Error:
        print('error', pymysql.Error)
        # con.rollback()
    finally:
        con.close()


def insertTestedRecord(recordlist):
    con = getDBCon()
    insersql = 'insert into t_testedapp_record()values()'
    try:
        with con.cursor() as cursor:
            cursor.executemany(insersql, recordlist)
            con.commit()
    except:
        print('error', pymysql.Error)
    finally:
        con.close()


def caltimegap(nowtimeobj):
    timegap = datetime.timedelta(days=7)
    days7obj = nowtimeobj - timegap
    days7str = days7obj.strftime('%Y-%m-%d')
    nowstrday = nowtimeobj.strftime('%Y-%m-%d')
    print('今天{0}7天前{1}'.format(nowstrday, days7str))
    return days7str, nowstrday


def mergeResult(nowtimeobj):
    shouldusecount = 0
    actualusecount = 0
    startdate, enddate = caltimegap(nowtimeobj)
    testedAppList = getTestingAppFromDevops(startdate, enddate)
    # print(testedAppList)
    usedAppList = getUsedApp()
    # print(usedAppList)
    for testedApp in usedAppList.keys():
        if testedApp in QuestionAppList:
            pass
        else:
            for covApp in testedAppList.keys():
                if testedApp == covApp:
                    # print('有使用的app是', testedApp, '实测version', usedAppList[testedApp], '应测version',
                    #       testedAppList[covApp], '交集', usedAppList[testedApp] & set(testedAppList[covApp]))
                    actualusecount += len(list(usedAppList[testedApp] & set(testedAppList[covApp])))
                    shouldusecount += len(usedAppList[testedApp])
                else:
                    pass
    print('应测和实测的数量', shouldusecount, actualusecount)
    return shouldusecount, actualusecount


def doscheduleJob():
    getConst()
    now = datetime.datetime.now()
    nowstr = now.strftime('%Y-%m-%d %H:%M:%S')
    shouldusecount, actualusecount = mergeResult(now)
    rate = round(actualusecount / shouldusecount, 2)
    insertCoverageUsedData(WeeklyType, [shouldusecount, actualusecount, rate, nowstr])
    insertCoverageUsedData(RecordType, [shouldusecount, actualusecount, rate, nowstr])


if __name__ == '__main__':
    # doscheduleJob()
    schedule.every().monday.at("01:00").do(doscheduleJob)
    while True:
        schedule.run_pending()