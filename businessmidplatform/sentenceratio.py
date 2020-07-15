# @File  : sentenceratio.py
# @Author: LiuXingsheng
# @Date  : 2020/7/1
# @Desc  : 业务中台-预研，手写笔迹识别 长句相似度
import os
import difflib
import xlrd
import xlsxwriter

DirPath = r'H:\业务中台\手写笔迹\测试结果\短句补充素材'
Title = 'hw'

def readData():
    alllist = []
    singrecord = []
    data = xlrd.open_workbook(os.path.join(DirPath, '20200701170312_hw.xlsx'))
    sheet = data.sheets()[0]
    sheetrows = sheet.nrows
    for row in range(1, sheetrows):
        singrecord.append(sheet.cell_value(row, 0))
        singrecord.append(sheet.cell_value(row, 1))
        singrecord.append(sheet.cell_value(row, 2))
        singrecord.append(sheet.cell_value(row, 3))
        singrecord.append(sheet.cell_value(row, 4))
        singrecord.append(sheet.cell_value(row, 5))
        singrecord.append(sheet.cell_value(row, 6))
        singrecord.append(sheet.cell_value(row, 7))
        singrecord.append(difflib.SequenceMatcher(None, sheet.cell_value(row, 2), sheet.cell_value(row, 5)).quick_ratio())
        alllist.append(singrecord)
        singrecord = []
    return alllist


def writeData(alllist):
    for item in alllist:
        difflib.SequenceMatcher(None, item[2], item[5]).quick_ratio()
    titlelist = [('序号', '内容类型', '标注内容', '书写类型', '笔记文件路径', '识别内容', '识别时间', '是否正确','相似度')]
    comlist = titlelist + alllist
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, Title + '长句准确率.xlsx'))
    ws = workbook.add_worksheet('sheet1')
    for row in range(len(comlist)):
        for column in range(len(comlist[row])):
            ws.write(row, column, comlist[row][column])
    workbook.close()


if __name__ == '__main__':
    datalist = readData()
    writeData(datalist)
