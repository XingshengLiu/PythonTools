# @File  : picsearch_labelfile.py
# @Author: LiuXingsheng
# @Date  : 2021/1/29
# @Desc  : 图搜标注整理文件

import xlrd
import xlsxwriter
import collections
import os

MachineIndex = 0
OriginLabelIndex = 3
AddLabelIndex = 14
FilePath = r"C:\Users\Administrator\Desktop"

def readAddExcel(filename):
    PicLabelDic = collections.defaultdict(list)
    ContentData = xlrd.open_workbook(os.path.join(FilePath, filename))
    Sheets = ContentData.sheets()
    for sheet in Sheets:
        for row in range(1, sheet.nrows):
            flaglist = []
            labellist = []
            returnqids = (str(sheet.cell_value(row, OriginLabelIndex)).replace('[', '').replace(']', '').
                             replace('\'', '').replace(' ', '').strip()).split(',')
            for col in range(13,18):
                if str(sheet.cell_value(row, col)) == '1.0':
                    flaglist.append(1)
                else:
                    flaglist.append(0)
            for item in range(len(flaglist)):
                if flaglist[item]:
                    labellist.append(returnqids[item])
                else:
                    pass
            PicLabelDic[str(sheet.cell_value(row, MachineIndex))] = labellist
    # for key in PicLabelDic.keys():
    #     print(key,PicLabelDic[key])
    return PicLabelDic


if __name__ == '__main__':
    labeldic = collections.defaultdict(list)
    picdic = readAddExcel('整理文件_接入图搜数据结果.xlsx')
    nopicdic = readAddExcel('整理文件_无图搜数据结果.xlsx')
    workbook = xlsxwriter.Workbook(os.path.join(FilePath,'图搜标注文件.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    ws.write(0, 0, '序列号')
    ws.write(0, 2, '标注id')
    row = 1
    for key in picdic.keys():
        labeldic[key] = picdic[key] + nopicdic[key]
        ws.write(row, 0, str(key))
        ws.write(row, 2, str(labeldic[key]))
        row += 1
    workbook.close()


