# @File  : learningprocessshortvideo.py
# @Author: LiuXingsheng
# @Date  : 2020/7/7
# @Desc  : 名师短视频学习进度(内容更新后，重新测试，根据长视频id和短视频id的对应关系，利用长视频id生成的学习进度进行测试)
import os
import random
import csv
import json
import xlsxwriter
import xlrd
import demjson

from learningprocessvideores import generandommachineId

# 生成的用户记录数量
COUNT = 5000

DirPath = r'C:\Users\Administrator\Desktop'


def getRealtionshipBetweenSLvideos():
    """
    此方法无需再次调用了，相关的数据已经整理好了,具体的整理方法见excel中sheet的名称
    :return:
    """
    relationshiplist = []
    with open(os.path.join(DirPath, '短视频关联关系_1.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        # 顺序分别为id,出版社,年级，章，节，课时
        for item in rows[1:]:
            relationshiplist.append((item[0], item[8]))
    alllist = [('短视频id', '长视频id')] + relationshiplist
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '短视频id_长视频id对应关系.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(alllist)):
        for column in range(len(alllist[row])):
            ws.write(row, column, alllist[row][column])
    workbook.close()


def getTidydata():
    datalist = []
    samechap_sec = []
    tidylist = []
    chapterlist = []
    with open(os.path.join(DirPath, '长短视频id关联对应学习进度.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    for item in rows[1:]:
        # 长视频id, 出版社，年级，章，节，课时，课程包id，短视频id
        datalist.append((item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7]))
        chapterlist.append((item[3], item[4]))
    chapterlist = list(set(chapterlist))
    for chapter in chapterlist[::-1]:
        for item in datalist:
            if item[3] == chapter[0] and item[4] == chapter[1]:
                samechap_sec.append(item)
        tidylist.append(samechap_sec)
        samechap_sec = []
        chapterlist.remove(chapter)

    # 此数据用来记录，可读取使用，可不使用
    # with open(os.path.join(DirPath,'short_longvideoid.csv'), 'w', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     for item in tidylist:
    #         writer.writerow(item)
    return tidylist


def generateBDuploadData(tidylist):
    # 插入数据库的列表
    insertrecord = []
    # 对比结果的列表
    testcomparerecord = []
    for i in range(COUNT):
        chosenchapter_sec = random.choice(tidylist)
        machineId = generandommachineId()
        for item in chosenchapter_sec:
            extend = {'videoName': 'This is test video data', 'index': '4', 'videoId': item[7], 'algorithmFlag': '-1'}
            str_json = json.dumps(extend)
            insertrecord.append(
                (machineId, item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], str(str_json)))
        # 序列号 长视频id, 出版社，年级，章，节，课时，课程包id，短视频id
        testcomparerecord.append((machineId, chosenchapter_sec[0][0], chosenchapter_sec[0][1],
                                  chosenchapter_sec[0][2], chosenchapter_sec[0][3],
                                  chosenchapter_sec[0][4], chosenchapter_sec[0][5],
                                  chosenchapter_sec[0][6], chosenchapter_sec[0][7]))
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '短视频插入数据.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(insertrecord)):
        for column in range(len(insertrecord[row])):
            ws.write(row, column, insertrecord[row][column])
    workbook.close()
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '短视频对比测试数据.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(testcomparerecord)):
        for column in range(len(testcomparerecord[row])):
            ws.write(row, column, testcomparerecord[row][column])
    workbook.close()


def readCalcudata():
    singlelist = []
    machineidlist = []
    caclulist = {}
    stdsinglelist = []
    stdlist = {}
    signresultrecord = []
    successcount = [0, 0, 0, 0, 0, 0]
    with open(os.path.join(DirPath, 'output(1).txt'), 'r', encoding='utf-8') as f:
        data = f.read()
        objdata = json.loads(data)
    for item in objdata:
        # 此处的videoId 为长视频id
        caclulist.update({item['machineId']: [
            str(item['pressId']), str(item['gradeId']), str(item['chapterId']), str(item['sectionId']), str(item['lessonId']), str(item['videoId'])]})

    data = xlrd.open_workbook(os.path.join(DirPath, '短视频对比测试数据.xlsx'))
    sheet = data.sheets()[0]
    sheetrows = sheet.nrows
    sheetcolumns = sheet.ncols
    for row in range(1, sheetrows):
        machineidlist.append(sheet.cell_value(row, 0))
        for col in range(1, sheetcolumns):
            stdsinglelist.append(sheet.cell_value(row, col))
        stdlist.update({sheet.cell_value(row, 0): stdsinglelist})
        stdsinglelist = []
    for machine in machineidlist:
        if caclulist.get(machine):
            # 出版社
            if stdlist[machine][1] == caclulist[machine][0]:
                signresultrecord.append(1)
            else:
                signresultrecord.append(0)
            # 年级
            if stdlist[machine][2] == caclulist[machine][1]:
                signresultrecord.append(1)
            else:
                signresultrecord.append(0)
            # 章
            if stdlist[machine][3] == caclulist[machine][2]:
                signresultrecord.append(1)
            else:
                signresultrecord.append(0)
            # 节
            if stdlist[machine][4] == caclulist[machine][3]:
                signresultrecord.append(1)
            else:
                signresultrecord.append(0)
            # 课时
            if stdlist[machine][5] == caclulist[machine][4]:
                signresultrecord.append(1)
            else:
                signresultrecord.append(0)
            # 学习进度
            if 0 in signresultrecord:
                signresultrecord.append(0)
            else:
                signresultrecord.append(1)
            singlelist.append([machine] + stdlist[machine] + caclulist[machine] + signresultrecord)
        else:
            singlelist.append([machine] + stdlist[machine] + ['x', 'x', 'x', 'x', 'x', 'x'] + [0, 0, 0, 0, 0, 0])
        for i in range(len(signresultrecord)):
            if signresultrecord[i] == 1:
                successcount[i] += 1
        signresultrecord = []
    print('出版社、年级、单元、小节、课时、进度准确率分别为：')
    for item in successcount:
        print(item/len(machineidlist))
    alllist = [['序列号', '长视频Id', '出版社', '年级', '章', '节', '课时', '课程包Id', '短视频Id', '大数据出版社', '大数据年级', '大数据章', '大数据节',
                '大数据课时', '大数据长视频Id','出版社是否正确','年级是否正确','章是否正确','节是否正确','课时是否正确','学习进度是否正确']] + singlelist
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '短视频个人学习进度准确率.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(alllist)):
        for column in range(len(alllist[row])):
            ws.write(row, column, alllist[row][column])
    workbook.close()


if __name__ == '__main__':
    # getRealtionshipBetweenSLvideos()
    # alllist = getTidydata()
    # generateBDuploadData(alllist)
    readCalcudata()
