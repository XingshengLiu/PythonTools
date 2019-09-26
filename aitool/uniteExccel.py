# @File  : uniteExccel.py
# @Author: LiuXingsheng
# @Date  : 2019/7/17
# @Desc  :

import xlrd, xlsxwriter
import os


class YDBean(object):
    original = ''
    new = ''
    result = ''
    note = ''
    label = ''

    def __init__(self, original, new, result, note, label):
        self.original = original
        self.new = new
        self.result = result
        self.note = note
        self.label = label


class ZYBean(object):
    original = ''
    result = ''
    note = ''

    def __init__(self, original, result, note):
        self.original = original
        self.result = result
        self.note = note


class Newbean(object):
    original = ''
    new = ''
    result = ''
    note = ''
    label = ''

    def __init__(self, original, new,result, note, label):
        self.original = original
        self.new  = new
        self.result = result
        self.note = note
        self.label = label


def getContent(fileName, beanType):
    List = []
    data = xlrd.open_workbook(os.getcwd() + '\\' + fileName + '.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        if beanType == 0:
            ydbean = YDBean(sheet.cell_value(row, 0), sheet.cell_value(row, 1),
                            sheet.cell_value(row, 2), sheet.cell_value(row, 3), sheet.cell_value(row, 4))
            List.append(ydbean)
        else:
            zybean = ZYBean(sheet.cell_value(row, 0), sheet.cell_value(row, 1),
                            sheet.cell_value(row, 2))
            List.append(zybean)
    return List


def wrapper(ydList, zyList):
    newList = []
    for ydbean in ydList:
        for zybean in zyList:
            if ydbean.original == zybean.original:
                newbean = Newbean(zybean.original, ydbean.new,zybean.result, zybean.note, ydbean.label)
                newList.append(newbean)
            else:
                pass
    return newList


def writeExcelContent(fileName, chosenList):
    try:
        column = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + fileName + '.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '文件名')
        ws.write(0, 1, '重命名')
        ws.write(0, 2, '测试结果')
        ws.write(0, 3, '备注')
        ws.write(0, 4, '分类')
        for item in chosenList:
            ws.write(column, 0, item.original)
            ws.write(column, 1, item.new)
            ws.write(column, 2, item.result)
            ws.write(column, 3, item.note)
            ws.write(column, 4, item.label)
            column += 1
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))

def main():
    ydList = getContent('match_1', 0)
    zyList = getContent('ZY', 1)
    newList = wrapper(ydList, zyList)
    writeExcelContent('result', newList)

if __name__ == '__main__':
    main()



