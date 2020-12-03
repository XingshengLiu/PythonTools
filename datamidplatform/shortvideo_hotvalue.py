# @File  : shortvideo_hotvalue.py
# @Author: LiuXingsheng
# @Date  : 2020/8/26
# @Desc  : 热度计算第二版
import os
from collections import defaultdict

import xlrd
import xlsxwriter

from datamidplatform.app_hotvalue import getTimeStamp
from datamidplatform.coursepackage_hotvalue import getDateTimeStamp
DateDic = {}
Dirpath = r'H:\大数据中台项目\标签测试报告\短视频热度\短视频热度标签项目'

decaylist = [0.1,0.15,0.2,0.25, 0.3, 0.37, 0.45, 0.55, 0.67, 0.82, 1]

def readUserData():
    videoset = set()
    videodic = defaultdict(list)
    ultralist = defaultdict(list)
    contentdata = xlrd.open_workbook(os.path.join(Dirpath, '刘生伟-短视频源数据.xlsx'))
    sheet = contentdata.sheets()[0]
    for row in range(1, sheet.nrows):
        videoset.add(str(sheet.cell_value(row, 1)))
        videodic[str(sheet.cell_value(row, 1))].append(getTimeStamp(sheet.cell_value(row, 3)))
    for video in list(videoset):
        counter = [0 for i in range(11)]
        for siglerecord in videodic[video]:
            countnum(siglerecord,counter)
        ultralist[video].append(counter)
        ultralist[video].append(calcuHotvalue(counter))
    # for key in ultralist.keys():
    #     print(key,ultralist[key])
    return ultralist

def calcuHotvalue(counter):
    hotvalue = 0
    for i in range(len(counter)):
        hotvalue += counter[i] * decaylist[i]
    return hotvalue

def readCalcuData():
    typelist = []
    typeset = set()
    videohotvaluedic = defaultdict(list)
    contentdata = xlrd.open_workbook(os.path.join(Dirpath, 'shengwei_viedo_hot_heat(2).xlsx'))
    sheet = contentdata.sheets()[0]
    for row in range(1, sheet.nrows):
        typeset.add(str(sheet.cell_value(row, 3)))
        videohotvaluedic[str(int(sheet.cell_value(row, 0)))].append(str(sheet.cell_value(row, 3)))
        videohotvaluedic[str(int(sheet.cell_value(row, 0)))].append(float(sheet.cell_value(row, 1)))
    for videotpe in list(typeset):
        hotdic = {}
        for key in videohotvaluedic.keys():
            if videohotvaluedic[key][0] == videotpe:
                hotdic[key] = videohotvaluedic[key][1]
        typelist.append(hotdic)
    # for item in typelist:
    #     print(item)
    return typelist

def compare(typelist,ultralist):
    allresultlist = []
    for singletype in typelist:
        typeresultlist = []
        for key in singletype.keys():
            typeresultlist.append([key,singletype[key],'',key,ultralist[key][0],ultralist[key][1]])
        allresultlist.append(typeresultlist)
    return allresultlist

def writecontent(allresultlist):
    for item in allresultlist:
        print(item)
    workbook = xlsxwriter.Workbook(os.path.join(Dirpath, '短视频热度测试.xlsx'))
    index = 1
    for item in allresultlist:
        ws = workbook.add_worksheet('sheet' + str(index))
        for row in range(len(item)):
            for column in range(len(item[row])):
                if column == 4:
                    for i in range(11):
                        ws.write(row, column + i, item[row][column][i])
                elif column == 5:
                    ws.write(row, 15, item[row][column])
                else:
                    ws.write(row, column, item[row][column])
        index += 1
    workbook.close()








def countnum(date, counter):
    if date == DateDic['12']:
        counter[0] += 1
    elif date == DateDic['13']:
        counter[1] += 1
    elif date == DateDic['14']:
        counter[2] += 1
    elif date == DateDic['15']:
        counter[3] += 1
    elif date == DateDic['16']:
        counter[4] += 1
    elif date == DateDic['17']:
        counter[5] += 1
    elif date == DateDic['18']:
        counter[6] += 1
    elif date == DateDic['19']:
        counter[7] += 1
    elif date == DateDic['20']:
        counter[8] += 1
    elif date == DateDic['21']:
        counter[9] += 1
    elif date == DateDic['22']:
        counter[10] += 1
    else:
        print(date)

if __name__ == '__main__':
    DateDic = getDateTimeStamp(11,'2020-08-12')
    ultralist = readUserData()
    typelist = readCalcuData()
    allresultlist = compare(typelist,ultralist)
    writecontent(allresultlist)



