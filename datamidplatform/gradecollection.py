# @File  : gradecollection.py
# @Author: LiuXingsheng
# @Date  : 2020/12/22
# @Desc  : it流程部年级数据
import os
from collections import defaultdict
import xlrd
import xlsxwriter

filepath = r'C:\Users\Administrator\Desktop'

def readExcel():
    gradedic = defaultdict(list)
    chosendic = defaultdict(list)
    singlechild = defaultdict(list)
    ContentData = xlrd.open_workbook(os.path.join(filepath,'年级.xlsx'))
    Sheets = ContentData.sheets()
    for sheet in Sheets:
        for row in range(sheet.nrows):
            gradedic[sheet.cell_value(row, 0)].append(sheet.cell_value(row, 1))
    for key in gradedic.keys():
        if len(gradedic[key]) > 1:
            chosendic[key]=gradedic[key]
        else:
            singlechild[key] = gradedic[key]
    print('--------满足要求的数据有',len(chosendic.keys()))
    for key in chosendic.keys():
        print(key,chosendic[key])
    workbook = xlsxwriter.Workbook(os.path.join(
        filepath, '整理年级_1229.xlsx'))
    ws_multi = workbook.add_worksheet(u'多孩')
    ws_single = workbook.add_worksheet(u'单孩')
    row_multi = 1
    row_single = 1
    for key in chosendic.keys():
        ws_multi.write(row_multi, 0, str(key))
        ws_multi.write(row_multi, 1, str(chosendic[key]))
        row_multi += 1
    for key in singlechild.keys():
        ws_single.write(row_single,0,str(key))
        ws_single.write(row_single, 1, str(singlechild[key]))
        row_single += 1
    workbook.close()




if __name__ == '__main__':
    readExcel()
