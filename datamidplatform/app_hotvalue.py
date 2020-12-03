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
    """
    读取学段app的csv数据
    :return:
    """
    keycount = collections.defaultdict(list)
    typecount = collections.defaultdict(list)
    with open(os.path.join(GradeDirPath, 'app热度分学段原始数据.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for data in datalist[1:]:
        key = (data[0],data[3])
        keycount[key].append([data[2],data[4]])
    print('--------------', keycount)
    for key in keycount.keys():
        countnum = 0
        datenum = 0
        for item in keycount[key]:
            datenum += getTimeStamp(item[0])
            countnum += int(item[1])
            typecount[key] = [datenum, countnum]
    print('学段整理后的数据', typecount)
    return typecount


def readExpectData(dirpath,file,type):
    """
    读取大数据计算的热度结果
    :param dirpath: 不同类型的数据源路径
    :param file: 数据源文件名
    :param type: 整机APP热度还是学段APP热度
    :return:
    """
    keycount = collections.defaultdict(list)
    with open(os.path.join(dirpath, file), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    if type == 'APP':
        for data in datalist[1:]:
            key = data[0]
            keycount[key].append(data[1])
    else:
        for data in datalist[1:]:
            key = (data[0],data[2])
            keycount[key].append(data[1])
    print('学段计算数据整理后结果',keycount)
    return keycount


def compare(userdata, calcudata, kind,dirpath):
    """
    比较合并用户数据和计算数据
    :param userdata: 用户数据整理结果
    :param calcudata: 大数据计算数据整理结果
    :param kind: 整机app热度还是学段热度
    :param dirpath: 文件生成的路径
    :return:
    """
    workbook = xlsxwriter.Workbook(os.path.join(dirpath, kind + '整机热度测试整理_v3_test.xlsx'))
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
    # calcudata = readExpectData(DirPath,'app热度计算结果.csv','APP')
    # compare(userdata, calcudata,'整机app',DirPath)
    print('------------------')
    userdatagrade = readGradeData()
    calcudatagrade = readExpectData(GradeDirPath,'app热度分学段计算结果.csv','Grade')
    compare(userdatagrade, calcudatagrade,'学段APP',GradeDirPath)

