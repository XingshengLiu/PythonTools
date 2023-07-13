# @File  : labelFileTidy.py
# @Author: LiuXingsheng
# @Date  : 2020/12/17
# @Desc  : 标注文件整理更新至标注文件

import os
import xlsxwriter
import xlrd
import collections

FilePath = r'C:\Users\Administrator\Desktop'
MachineIndex = 0
OriginLabelIndex = 2
AddLabelIndex = 28

def readAddExcel(filename):
    """
    读取整理文件,关联序列号和补充的id
    :param filename: html和粗框图对应的整理文件
    :return:
    """
    PicLabelDic = collections.defaultdict(list)
    ContentData = xlrd.open_workbook(os.path.join(FilePath, filename))
    Sheets = ContentData.sheets()
    for sheet in Sheets:
        for row in range(1, sheet.nrows):
            originallabel = (str(sheet.cell_value(row, OriginLabelIndex)).replace('[','').replace(']','').
                             replace('\'','').replace(' ','').strip()).split(',')
            if sheet.cell(row, AddLabelIndex).ctype == 2:
                addlabel = str(int(sheet.cell_value(row, AddLabelIndex))).split(',')
            else:
                if len(sheet.cell_value(row, AddLabelIndex)) == 0:
                    addlabel = []
                else:
                    if str(sheet.cell_value(row, AddLabelIndex)) == '无id':
                        addlabel = []
                    else:
                        addlabel = str(sheet.cell_value(row, AddLabelIndex)).replace(' ','').split(',')
            print('---------------->内容和长度是',addlabel,len(addlabel))
            itemlist = originallabel + addlabel
            PicLabelDic[sheet.cell_value(row, MachineIndex)] = itemlist
    return PicLabelDic

def readOriginalExcelAndRefresh(filename,PicLabelDic):
    """
    根据人工核对整理文件中补充的id，更新原有的标注文件
    :param filename: 原有的标注文件
    :param PicLabelDic: 序列号和补充id的字典
    :return:
    """
    print('---------------------')
    for key in PicLabelDic.keys():
        print(key,PicLabelDic[key])
    AllLabelDic = collections.defaultdict(list)
    ContentData = xlrd.open_workbook(os.path.join(FilePath, filename))
    Sheets = ContentData.sheets()
    for sheet in Sheets:
        for row in range(1, sheet.nrows):
            AllLabelDic[sheet.cell_value(row, 0)].append(sheet.cell_value(row, 1))
            AllLabelDic[sheet.cell_value(row, 0)].append(sheet.cell_value(row, 2))
            AllLabelDic[sheet.cell_value(row, 0)].append(sheet.cell_value(row, 3))
            AllLabelDic[sheet.cell_value(row, 0)].append(sheet.cell_value(row, 4))
    for key in AllLabelDic.keys():
        if key in PicLabelDic.keys():
            AllLabelDic[key][1] = PicLabelDic[key]
    workbook = xlsxwriter.Workbook(os.path.join(FilePath,'20210225更新_' + filename))
    ws = workbook.add_worksheet(u'sheet1')
    row = 1
    ws.write(0, 0, '序列号')
    ws.write(0, 1, '粗框图')
    ws.write(0, 2, '正确题目Id')
    ws.write(0, 3, '手指图')
    ws.write(0, 4, '科目')
    for key in AllLabelDic.keys():
        ws.write(row, 0, str(key))
        ws.write(row, 1, str(AllLabelDic[key][0]))
        ws.write(row, 2, str(AllLabelDic[key][1]))
        ws.write(row, 3, str(AllLabelDic[key][2]))
        ws.write(row, 4, str(AllLabelDic[key][3]))
        row += 1
    workbook.close()

if __name__ == '__main__':
    PicLabelDic = readAddExcel('图搜接入_图搜_专项环境_20210129.xlsx')
    readOriginalExcelAndRefresh('20210224更新_图搜标注Id.xlsx',PicLabelDic)
