# @File  : apptype_favour.py
# @Author: LiuXingsheng
# @Date  : 2020/8/1
# @Desc  : 用户应用类型偏好
import os
import csv
import collections
from datamidplatform.app_hotvalue import getTimeStamp
import xlsxwriter

DirPath = r'H:\大数据中台项目\标签测试报告\应用商店\应用类别偏好'
# 数据结构：123：[{'标签'：‘名人’,'时间和':'123456'，‘次数’：‘5’},{'标签'：‘大家’,'时间和':'1234567'，‘次数’：‘6’}]
# 数据结构 123：[[123,标签],[123,标签]]

DateDic = {'23': 1595433600, '24': 1595520000, '25': 1595606400, '26': 1595692800, '27': 1595779200, '28': 1595865600,
           '29': 1595952000,
           '30': 1596038400}


def readUserData():
    apptypedic = collections.defaultdict(list)
    typecountdic = collections.defaultdict(list)
    sigset = collections.defaultdict(set)
    with open(os.path.join(DirPath, '用户应用类型偏好-用户数据PM.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        userlist = [row for row in reader]
    for user in userlist[1:]:
        timestamp = getTimeStamp(str(user[2]))
        apptypedic[user[1]].append([user[4], timestamp])
        typecountdic[user[1]].append(user[4])
        sigset[user[1]].add(user[4])
    # print(apptypedic)
    # print(typecountdic)
    # print(sigset)
    ultralist = collections.defaultdict(list)
    for key in list(sigset.keys()):
        for type in list(sigset[key]):
            counter = [0, 0, 0, 0, 0, 0, 0, 0]
            typedate = 0
            typecount = typecountdic[key].count(type)
            for sigcp in apptypedic[key]:
                if sigcp[0] == type:
                    typedate += sigcp[1]
                    countnum(sigcp[1], counter)
                else:
                    pass
            ultralist[key].append([type, counter[0], counter[1], counter[2], counter[3],
                 counter[4], counter[5], counter[6],counter[7],typecount, typedate])
    print(ultralist)
    return ultralist


def countnum(date, counter):
    if date == DateDic['23']:
        counter[0] += 1
    elif date == DateDic['24']:
        counter[1] += 1
    elif date == DateDic['25']:
        counter[2] += 1
    elif date == DateDic['26']:
        counter[3] += 1
    elif date == DateDic['27']:
        counter[4] += 1
    elif date == DateDic['28']:
        counter[5] += 1
    elif date == DateDic['29']:
        counter[6] += 1
    elif date == DateDic['30']:
        counter[7] += 1
    else:
        print(date)


def readCaldata():
    bddic = collections.defaultdict(list)
    with open(os.path.join(DirPath, '用户应用类型偏好-计算结果PM.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for data in datalist[1:]:
        bddic[data[0]].append([data[1], data[2]])
    print(bddic)
    return bddic


def comparejoin(ultralist, bddic):
    finaldic = collections.defaultdict(list)
    for key in ultralist.keys():
        caclist = bddic[key]
        for item in ultralist[key]:
            for cal in caclist:
                if item[0] == cal[0]:
                    finaldic[key].append(item + [cal[1]])
                else:
                    pass
    print(finaldic)
    return finaldic


def writeFile(finaldic):
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '类型偏好准确率_日期展开.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    columnindex = 0
    for key in finaldic.keys():
        itemlist = finaldic[key]
        for row in range(len(itemlist)):
            for column in range(12):
                if row == 0:
                    if (columnindex + column) % 12 == 0:
                        ws.write(row, columnindex + column, '类别_' + key)
                    elif (columnindex + column) % 12 == 1:
                        ws.write(row, columnindex + column, '23日次数')
                    elif (columnindex + column) % 12 == 2:
                        ws.write(row, columnindex + column, '24日次数')
                    elif (columnindex + column) % 12 == 3:
                        ws.write(row, columnindex + column, '25日次数')
                    elif (columnindex + column) % 12 == 4:
                        ws.write(row, columnindex + column, '26日次数')
                    elif (columnindex + column) % 12 == 5:
                        ws.write(row, columnindex + column, '27日次数')
                    elif (columnindex + column) % 12 == 6:
                        ws.write(row, columnindex + column, '28日次数')
                    elif (columnindex + column) % 12 == 7:
                        ws.write(row, columnindex + column, '29日次数')
                    elif (columnindex + column) % 12 == 8:
                        ws.write(row, columnindex + column, '30日次数')
                    elif (columnindex + column) % 12 == 9:
                        ws.write(row, columnindex + column, '总次数')
                    elif (columnindex + column) % 12 == 10:
                        ws.write(row, columnindex + column, '日期求和')
                    elif (columnindex + column) % 12 == 11:
                        ws.write(row, columnindex + column, '偏好值')
                    else:
                        pass
                else:
                    if column == 10:
                        ws.write(row, columnindex + column, int(float(itemlist[row][column]) / 10000000))
                    elif column == 11:
                        ws.write(row, columnindex + column, float(itemlist[row][column]))
                    else:
                        ws.write(row, columnindex + column, itemlist[row][column])
        columnindex += 12
    workbook.close()


if __name__ == '__main__':
    ultralist = readUserData()
    bddic = readCaldata()
    finaldic = comparejoin(ultralist, bddic)
    writeFile(finaldic)
