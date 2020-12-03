# @File  : learningprocessCleanData.py
# @Author: LiuXingsheng
# @Date  : 2020/8/3
# @Desc  : 8月3号 大数据开发提供的整机学习进度数据中，存在相同序列号的数据，此处把相同序列号的数据按照奇偶行分成两部分，计算准确率
import os
import xlrd
import csv
singrecorddic = {}
odlist = []
cplist = []
Dirpath = r'H:\大数据中台项目\标签测试报告\Z计划-个人学习进度标签\搜题\V3.0(内容优化)'
flag = 0
workbook = xlrd.open_workbook(os.path.join(Dirpath,'重复结果.xlsx'))
sheet = workbook.sheets()[0]
rows = sheet.nrows
columns = sheet.ncols
for row in range(rows):
    sgodlist = []
    sgcplist = []
    for colu in range(columns):
        if row % 2 == 0:
            flag = 0
            if sheet.cell(row, colu).ctype == 2:
                sgodlist.append(str(int(sheet.cell_value(row,colu))))
            else:
                sgodlist.append(sheet.cell_value(row, colu))
        else:
            flag = 1
            if sheet.cell(row, colu).ctype == 2:
                sgcplist.append(str(int(sheet.cell_value(row, colu))))
            else:
                sgcplist.append(sheet.cell_value(row, colu))
    if flag:
        cplist.append(sgcplist)
    else:
        odlist.append(sgodlist)


with open(os.path.join(Dirpath,'repeat_1.csv'),'w',newline='',encoding='utf-8')as f1:
    writer = csv.writer(f1)
    for cp in cplist:
        writer.writerow(cp)

with open(os.path.join(Dirpath,'repeat_2.csv'),'w',newline='',encoding='utf-8')as f2:
    writer = csv.writer(f2)
    for od in odlist:
        writer.writerow(od)
