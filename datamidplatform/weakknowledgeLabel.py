# @File  : weakknowledgeLabel.py
# @Author: LiuXingsheng
# @Date  : 2020/7/16
# @Desc  : 薄弱知识点偏好
import os
import csv
from collections import Counter
import collections
import xlrd
import xlsxwriter

DirPath = r'H:\大数据中台项目\标签测试报告\薄弱知识点'

def getUserDataFromExcel():
    userdata = []
    data = xlrd.open_workbook(os.path.join(DirPath, '薄弱知识点数据源.xlsx'))
    sheet = data.sheets()[2]
    sheetrows = sheet.nrows
    for row in range(1, sheetrows):
        userdata.append([sheet.cell_value(row, 0), int(sheet.cell_value(row, 1))])
    return userdata

def preProcessData(userdata):
    nulllist = []
    print('学科知识点对应关系',userdata)
    matchdic = collections.defaultdict(list)
    with open(os.path.join(DirPath, '版本知识点_学科知识点对应关系.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for row in datalist:
        matchdic[row[2]].append(row[1])
    print(matchdic)
    for user in userdata:
        if len(matchdic[str(user[1])]) == 0:
            nulllist.append(user)
            pass
        else:
            user[1] = matchdic[str(user[1])][0]
    for nullnum in nulllist:
        userdata.remove(nullnum)
    print('版本知识点对应关系',userdata)
    return userdata



def readUserData(userdata):
    userordereddata = collections.defaultdict(list)
    usercount = collections.defaultdict(list)
    for user in userdata:
        usercount[user[0]].append(user[1])
    print(usercount)
    # newusercount = sorted(usercount.items(),key=lambda item:item[1],reverse=True)
    # print(newusercount)
    for key in usercount.keys():
        result = Counter(usercount[key])
        d = sorted(result.items(),key=lambda x:x[1],reverse= True)
        userordereddata[key] = d
    print(userordereddata)
    return userordereddata

def readCalData():
    bigdataconfidencelist =collections.defaultdict(list)
    with open(os.path.join(DirPath, '薄弱知识点大数据置信度.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for data in datalist:
        itemlist = []
        for item in data[1:]:
            itemlist.append(item)
        bigdataconfidencelist[data[0]] = itemlist
    print(bigdataconfidencelist)
    return bigdataconfidencelist


def compareResult(userordereddata,bigdataresult):
    comparelist = []
    for key in userordereddata.keys():
        flaglist = []
        comparelist.append((key,userordereddata[key]))
        comparelist.append((key, bigdataresult[key]))
        for i in range(len(userordereddata[key])):
            if str(userordereddata[key][i][0]) in str(bigdataresult[key][i]):
                flaglist.append(1)
            else:
                flaglist.append(0)
        comparelist.append(('',flaglist))
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '薄弱知识点测试结果_0716_v1.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(comparelist)):
        for column in range(len(comparelist[row][1]) + 1):
            if row % 3 == 0:
                ws.write(row, 0, '用户实际数据')
            elif row % 3 == 1:
                ws.write(row, 0, '大数据预测置信度')
            else:
                ws.write(row, 0, '是否正确')
            if column == 1:
                ws.write(row, column, str(comparelist[row][0]))
            else:
                for inneritem in range(len(comparelist[row][1])):
                    ws.write(row, inneritem + 2, str(comparelist[row][1][inneritem]))
    workbook.close()



if __name__ == '__main__':
    userdata = getUserDataFromExcel()
    userdata = preProcessData(userdata)
    userordereddata = readUserData(userdata)
    bigdataconfidencelist = readCalData()
    compareResult(userordereddata,bigdataconfidencelist)
