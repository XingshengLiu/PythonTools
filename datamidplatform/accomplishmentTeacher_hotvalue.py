# @File  : accomplishmentTeacher_hotvalue.py
# @Author: LiuXingsheng
# @Date  : 2020/7/17
# @Desc  : 素养课名师热度
import os
import csv
import collections
import xlsxwriter

DirPath= r'H:\大数据中台项目\标签测试报告\素养课名师热度'

def readSourceData():
    teachercollectionlist = collections.defaultdict(dict)
    datacollectionlist = collections.defaultdict(dict)
    hotvaluecollectionlist = collections.defaultdict(dict)
    datadic = {}
    with open(os.path.join(DirPath, 't_teacher.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        teacherlist = [row for row in reader]
    for teacher in teacherlist[1:]:
        teachercollectionlist[teacher[1]] = teacher[0]
    # print(teachercollectionlist)
    with open(os.path.join(DirPath, '素养课名师原始数据.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for teacher in datalist[1:]:
        datacollectionlist[teacher[0]] = teacher[1:]
    # print(datacollectionlist)
    with open(os.path.join(DirPath, '素养课名师热度结果.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        hotlist = [row for row in reader]
    for hotvalue in hotlist[1:]:
        hotvaluecollectionlist[hotvalue[0]] = hotvalue[3]
    print(hotvaluecollectionlist)
    for key in datacollectionlist.keys():
        datadic.update({str(teachercollectionlist[key]) : datacollectionlist[key] + [hotvaluecollectionlist[teachercollectionlist[key]]]})
    print(len(datadic))
    print(datadic)
    return datadic

def writeContent(datadic):
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '素养课名师热度测试结果_all.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    i= 0
    for k,v in datadic.items():
        ws.write(i,0,k)
        for inneritem in range(len(v)):
            ws.write(i,inneritem + 1,v[inneritem])
        i += 1
    workbook.close()


if __name__ == '__main__':
    datadic = readSourceData()
    writeContent(datadic)