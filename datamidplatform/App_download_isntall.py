# @File  : App_download_isntall.py
# @Author: LiuXingsheng
# @Date  : 2021/1/25
# @Desc  : APP安装&下载标签

import os
import xlrd
from collections import defaultdict
from aitool.copyfile import writecontent
DirPath = r'H:\大数据中台项目\标签测试报告\APP卸载\app卸载测试'
def readExcel(filename, colindex):
    datadiclist = defaultdict(set)
    filepath = os.path.join(DirPath, filename + '.xlsx')
    contentdata = xlrd.open_workbook(filepath)
    sheet = contentdata.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        if colindex == 1:
            appidlist = sheet.cell_value(row, colindex).split(',')
            datadiclist[sheet.cell_value(row, 0)] = set(appidlist)
        else:
            datadiclist[sheet.cell_value(row, 0)].add(sheet.cell_value(row, colindex))
    return datadiclist


if __name__ == '__main__':
    resultdiclist = []
    originaldata = readExcel('卸载数据测试源数据', 3)
    calcudata = readExcel('卸载数据测试结果', 1)
    for key in originaldata.keys():
        if originaldata[key] == calcudata[key]:
            resultdiclist.append([key, str(originaldata[key]), str(calcudata[key]),'正确'])
        else:
            resultdiclist.append([key, str(originaldata[key]), str(calcudata[key]), '错误'])
    writecontent(DirPath,  'app卸载标签测试结果', resultdiclist)