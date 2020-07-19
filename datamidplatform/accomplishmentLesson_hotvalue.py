# @File  : accomplishmentLesson_hotvalue.py
# @Author: LiuXingsheng
# @Date  : 2020/7/14
# @Desc  : 名师辅导班素养课热度测试
import os
import csv
import collections
import xlsxwriter
import json

DirPath = r'H:\大数据中台项目\标签测试报告\名师素养课'


def readData():
    """
    样式csv数据转存excel，方便查看数据及统计各维度数据
    :return:
    """
    with open(os.path.join(DirPath, '书法.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '素养课用户播放数据_书法.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(datalist)):
        for column in range(len(datalist[row])):
            ws.write(row, column, datalist[row][column])
    workbook.close()


def countData():
    """
    统计用户数据，查看各素养课视频播放次数，降序排列后写入excel
    :return:
    """
    thirdcount = collections.defaultdict(list)
    coursecount = collections.defaultdict(list)
    thirdlevel = []
    setlevel = set()
    courseId = []
    with open(os.path.join(DirPath, '书法.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        for row in rows[1:]:
            courseId.append((row[11], row[0]))
            thirdlevel.append(row[11])
            setlevel.add(row[11])
    print('总数是', len(thirdlevel))
    typelist = list(setlevel)
    for name in typelist:
        thirdcount[name] = thirdlevel.count(name)
    for cp in courseId:
        coursecount[cp] = courseId.count(cp)
    newthirdcount = sorted(thirdcount.items(), key=lambda item: item[1], reverse=True)
    newcoursecount = sorted(coursecount.items(), key=lambda item: item[1], reverse=True)
    print('--------', newthirdcount)
    print('--------', newcoursecount)
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '用户数据整理结果.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(newthirdcount)):
        for column in range(len(newthirdcount[row])):
            ws.write(row, column, str(newthirdcount[row][column]))
    row = len(newthirdcount)
    i = 0
    for row in range(row, row + len(newcoursecount)):
        for column in range(len(newcoursecount[i])):
            ws.write(row, column, str(newcoursecount[i][column]))
        i += 1
    workbook.close()


def readBDdata():
    """
    统计大数据计算出的素养课热度值，计算的值写在json中，先解析后降序排列写入文件
    :return:
    """
    musiclist = []
    musiccourselist = []
    handlist = []
    handcourselist = []
    with open(os.path.join(DirPath, '素养课结果输出'), 'r', encoding='utf-8') as f:
        data = f.read()
    objdata = json.loads(data)
    for item in objdata['data']:
        if item['secondLevelTag'] == '书法':
            for handitem in item['thirdLevelInfo']:
                handlist.append((handitem['tagName'], handitem['hotValue']))
                for course in handitem['courseInfo']:
                    handcourselist.append((handitem['tagName'], course['courseid'], course['hotValue']))
        elif item['secondLevelTag'] == '器乐':
            for handitem in item['thirdLevelInfo']:
                musiclist.append((handitem['tagName'], handitem['hotValue']))
                for course in handitem['courseInfo']:
                    musiccourselist.append((handitem['tagName'], course['courseid'], course['hotValue']))
        else:
            pass
    print('书法三级标签', handlist)
    newhandlist = sorted(handlist, key=lambda item: item[1], reverse=True)
    print('书法三级标签排序', newhandlist)
    print('书法课程标签', handcourselist)
    newhandcourselist = sorted(handcourselist, key=lambda item: item[2], reverse=True)
    print('书法课程标签排序', newhandcourselist)
    print('----------')
    print('器乐三级标签', musiclist)
    newmusiclist = sorted(musiclist, key=lambda item: item[1], reverse=True)
    print('器乐三级标签排序', newmusiclist)
    print('器乐课程标签', musiccourselist)
    newmusiccourselist = sorted(musiccourselist, key=lambda item: item[2], reverse=True)
    print('器乐课程标签排序', newmusiccourselist)

    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '算法数据整理结果_1.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(newmusiclist)):
        for column in range(len(newmusiclist[row])):
            ws.write(row, column, newmusiclist[row][column])
    row = len(newmusiclist)
    i = 0
    for row in range(row, row + len(newmusiccourselist)):
        for column in range(len(newmusiccourselist[i])):
            ws.write(row, column, newmusiccourselist[i][column])
        i += 1
    row = len(newmusiclist) + len(newmusiccourselist)
    i = 0
    for row in range(row, row + len(newhandlist)):
        for column in range(len(newhandlist[i])):
            ws.write(row, column, newhandlist[i][column])
        i += 1
    row = len(newmusiclist) + len(newmusiccourselist) + len(newhandlist)
    i = 0
    for row in range(row, row + len(newhandcourselist)):
        for column in range(len(newhandcourselist[i])):
            ws.write(row, column, newhandcourselist[i][column])
        i += 1
    workbook.close()


def teststr():
    list = [1,2,3,4]
    print(list[:2])
    for i in range(1,1):
        print('%%%',i)
    # strs = ["c", "c"]
    # strs = ["flower","flow","flight"]
    # strs = ["dog","racecar","car"]
    # strs = ["a", "b"]
    strs = []
    # strs = ['']
    strs = ['c','c']
    if not strs:
        print('xxxxxxxx')
        return ""
    str0 = min(strs)
    str1 = max(strs)
    for i in range(len(str0)):
        if str0[i] != str1[i]:
            print('11111',str0[:i])
            return str0[:i]
    print('222222',str0)
    return str0


if __name__ == '__main__':
    # readData()
    # countData()
    # readBDdata()
    teststr()
    test = ['']
    if test:
        print(True)
    else:
        print(False)
    print(len(['']))
    strs = ["dog", "racecar", "car"]
    print(min(strs))
    print(max(strs))
