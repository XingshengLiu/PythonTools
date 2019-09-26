# @File  : combineExcel.py
# @Author: LiuXingsheng
# @Date  : 2019/9/20
# @Desc  :
import os
import xlrd
import xlsxwriter

DIR_Path = r'\\172.28.1.23\ai数据素材\AI测试素材库\已标注素材\图像\OCR\印刷体\英文印刷体\第二季度OCR英文素材_1\excel汇总'


class Bean(object):
    def __init__(self, picName, type):
        self.picName = picName
        self.type = type


def getExcelList():
    excelList = []
    fileList = os.listdir(DIR_Path)
    for file in fileList:
        if file.endswith('.xlsx'):
            excelList.append(file)
    return excelList


def combineContent(excellist):
    contentbeanList = []
    for file in excellist:
        data = xlrd.open_workbook(DIR_Path + '\\' + str(file))
        sheet = data.sheets()[0]
        rows = sheet.nrows
        for row in range(1, rows):
            bean = Bean(sheet.cell_value(row, 0),sheet.cell_value(row, 1))
            contentbeanList.append(bean)
    return contentbeanList

def writeContent(contentbeanList):
    try:
        column = 1
        workbook = xlsxwriter.Workbook(DIR_Path + '\\' + '整合' + '.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '文件名')
        ws.write(0, 1, '类型')
        for item in contentbeanList:
            ws.write(column, 0, item.picName)
            ws.write(column, 1, item.type)
            column += 1
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))

if __name__ == '__main__':
    print(DIR_Path)
    excelList = getExcelList()
    contentList = combineContent(excelList)
    writeContent(contentList)