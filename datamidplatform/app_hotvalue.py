# @File  : app_hotvalue.py
# @Author: LiuXingsheng
# @Date  : 2020/7/28
# @Desc  : 应用商店，整机app热度，分学段热度

import csv
import collections
import os
import time
import xlsxwriter

DirPath = r'H:\大数据中台项目\标签测试报告\应用商店\整机热度\整机'
GradeDirPath = r'H:\大数据中台项目\标签测试报告\应用商店\整机热度\学段'


def readData():
    """
    读取整机APP的csv数据
    :return:
    """
    keycount = collections.defaultdict(list)
    typecount = collections.defaultdict(list)
    with open(os.path.join(DirPath, 'app热度分学段原始数据.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for data in datalist[1:]:
        key = data[0]
        keycount[key].append(data[2:])
    print(keycount)
    for key in keycount.keys():
        countnum = 0
        datenum = 0
        for item in keycount[key]:
            datenum += getTimeStamp(item[0])
            countnum += int(item[1])
            typecount[key] = [datenum, countnum]
    print('整理后的数据', typecount)
    return typecount


def readGradeData():
    keycount = collections.defaultdict(list)
    typecount = collections.defaultdict(list)
    gradecount = collections.defaultdict(list)
    tidycount = collections.defaultdict(list)
    with open(os.path.join(GradeDirPath, 'app热度分学段原始数据.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for data in datalist[1:]:
        key = data[0]
        keycount[key].append(data[2:])
    print('--------------', keycount)
    for key in keycount.keys():
        countnum = 0
        datenum = 0
        for item in keycount[key]:
            datenum += getTimeStamp(item[0])
            countnum += int(item[2])
            typecount[key] = [item[1], datenum, countnum]
    print('学段整理后的数据', typecount)
    for key in keycount.keys():
        for item in keycount[key]:
            gradecount[item[1]].append([item[0], item[2]])
        tidycount[key].append(gradecount)
    print('*************************')
    for key in typecount.keys():
        for typecount[key]

    # print('年级整理后的数据', tidycount)
    return typecount


def readExpectData():
    keycount = collections.defaultdict(list)
    with open(os.path.join(DirPath, 'app热度计算结果.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for data in datalist[1:]:
        key = data[0]
        keycount[key].append(data[1])
    print(keycount)
    return keycount


def compare(userdata, calcudata, kind):
    for key in userdata.keys():
        print(key)
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, kind + '整机热度测试整理_v2_test.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    row = 0
    for key in userdata.keys():
        ws.write(row, 0, str(key))
        ws.write(row, 1, str(userdata[key][0]))
        ws.write(row, 2, str(userdata[key][1]))
        ws.write(row, 3, calcudata[key][0])
        row += 1
    workbook.close()


def getTimeStamp(date):
    timearray = time.strptime(date, '%Y-%m-%d')
    timeStamp = int(time.mktime(timearray))
    return timeStamp


if __name__ == '__main__':
    # userdata = readData()
    # calcudata = readExpectData()
    # compare(userdata, calcudata,'整机app')
    readGradeData()
