# @File  : coursepackage_hotvalue.py
# @Author: LiuXingsheng
# @Date  : 2020/8/11
# @Desc  : 同步课程包&同步课程热度标签测试
import os
import csv
import time
import collections
from datamidplatform.app_hotvalue import getTimeStamp
import xlsxwriter

DirPath = r'H:\大数据中台项目\标签测试报告\素养课视频热度\素养课视频课程热度提测'

# DateDic = {'31': 1596124800, '1': 1596211200, '2': 1596297600, '3': 1596384000, '4': 1596470400, '5': 1596556800,
#            '6': 1596643200, '7': 1596729600}
DateDic = {}
# decaylist = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65]
# decaylist = [0.1,0.2, 0.3, 0.4, 0.5, 0.75, 0.9, 1]
decaylist = [0.25, 0.3, 0.37, 0.45, 0.55, 0.67, 0.82, 1]


def readUserData():
    coursepkgset = set()
    coursepkgdic = collections.defaultdict(list)
    ultralist = collections.defaultdict(list)
    with open(os.path.join(DirPath, '素养课原始数据.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        userlist = [row for row in reader]
    for user in userlist[1:]:
        if user[1] == 'null':
            pass
        else:
            coursepkgset.add(user[0])
            timestamp = getTimeStamp(str(user[3]))
            coursepkgdic[user[0]].append([int(user[1]) / int(user[2]), timestamp])
    for course in list(coursepkgset):
        avgratiolist = []
        counter = [0, 0, 0, 0, 0, 0, 0, 0]
        ratiosumcounter = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for siglerecord in coursepkgdic[course]:
            countnum(siglerecord[1], counter, siglerecord[0], ratiosumcounter)
        for i in range(len(counter)):
            if counter[i]:
                avgratiolist.append(ratiosumcounter[i] / counter[i])
            else:
                avgratiolist.append(0)
        ultralist[course].append(avgratiolist)
        ultralist[course].append(counter)
        ultralist[course].append([sum(counter)])
    for key in ultralist.keys():
        print(key,ultralist[key])
    return ultralist


def calcuhotvalue(ultralist):
    ultimatelist = collections.defaultdict(list)
    for key in ultralist.keys():
        ratiolist = ultralist[key][0]
        playtimeslist = ultralist[key][1]
        length = len(playtimeslist)
        ratiosum = 0
        playsum = 0
        for i in range(length):
            # 此处的播放占比不进行衰减，直接进行相加
            # ratiosum += ratiolist[i] * decaylist[i]
            ratiosum += ratiolist[i]
            playsum += playtimeslist[i] * decaylist[i]
        # ultimatelist[key] = [ratiosum, playsum]  # 计算热度V1:平均播放占比求和
        daynum = length - (ultralist[key][1].count(0))  # 计算热度V2:播放占比求和求平均
        ultimatelist[key] = [(ratiosum / daynum), playsum]
    return ultimatelist


def readCalcudata():
    calculdic = collections.defaultdict(list)
    with open(os.path.join(DirPath, '素养课热度结果.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        calculist = [row for row in reader]
    for item in calculist[1:]:
        if 'E' in item[6]:
            calculdic[item[0]].append(0)
        else:
            calculdic[item[0]].append(float(item[6]))
    return calculdic


def compare(ultimatelist, calculdic):
    cmpltdic = collections.defaultdict(list)
    for key in ultimatelist.keys():
        cmpltdic[key].append(ultimatelist[key])
        cmpltdic[key].append(calculdic[key])
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '素养课视频热度测试.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    row = 0
    for key in cmpltdic.keys():
        ws.write(row, 0, key)
        ws.write(row, 1, cmpltdic[key][0][0])
        ws.write(row, 2, cmpltdic[key][0][1])
        ws.write(row, 3, cmpltdic[key][1][0])
        row += 1
    workbook.close()

    # for key in list(sigset.keys()):
    #     for type in list(sigset[key]):
    #         counter = [0, 0, 0, 0, 0, 0, 0, 0]
    #         typedate = 0
    #         typecount = typecountdic[key].count(type)
    #         for sigcp in apptypedic[key]:
    #             if sigcp[0] == type:
    #                 typedate += sigcp[1]
    #                 countnum(sigcp[1], counter)
    #             else:
    #                 pass
    #         ultralist[key].append([type, counter[0], counter[1], counter[2], counter[3],
    #              counter[4], counter[5], counter[6],counter[7],typecount, typedate])
    # print(ultralist)
    # return ultralist


def countnum(date, counter, ratio, ratiocounter):
    if date == DateDic['05']:
        counter[0] += 1
        ratiocounter[0] += ratio
    elif date == DateDic['06']:
        counter[1] += 1
        ratiocounter[1] += ratio
    elif date == DateDic['07']:
        counter[2] += 1
        ratiocounter[2] += ratio
    elif date == DateDic['08']:
        counter[3] += 1
        ratiocounter[3] += ratio
    elif date == DateDic['09']:
        counter[4] += 1
        ratiocounter[4] += ratio
    elif date == DateDic['10']:
        counter[5] += 1
        ratiocounter[5] += ratio
    elif date == DateDic['11']:
        counter[6] += 1
        ratiocounter[6] += ratio
    elif date == DateDic['12']:
        counter[7] += 1
        ratiocounter[7] += ratio
    else:
        print(date)


def getDateTimeStamp(daysnum, startdate):
    startstamp = getTimeStamp(startdate)
    DateDic[startdate[-2:]] = startstamp
    for i in range(daysnum - 1):
        startstamp += 24 * 3600
        timeArray = time.localtime(startstamp)
        formalTime = time.strftime("%Y-%m-%d", timeArray)
        DateDic[formalTime[-2:]] = startstamp
    # print(DateDic)
    return DateDic


if __name__ == '__main__':
    getDateTimeStamp(8, '2020-08-05')
    ultralist = readUserData()
    calculist = readCalcudata()
    ultimatelist = calcuhotvalue(ultralist)
    compare(ultimatelist, calculist)
