# @File  : getAllFileName.py
# @Author: LiuXingsheng
# @Date  : 2019/10/9
# @Desc  :
import os
import xlsxwriter

DIR = r'\\172.28.1.23\ai数据素材\AI测试素材库\未标注素材\准备标注素材\公式'


def getPicDir(dir):
    dirList = []
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            path = os.path.join(root, dir)
            print(path)
            dirList.append(path)
    return dirList


if __name__ == '__main__':
    wholeFileList = []
    dirList = getPicDir(DIR)
    for item in dirList:
        fileList = os.listdir(item)
        wholeFileList.append((item, fileList))
    for item in wholeFileList:
        row = 1
        workbook = xlsxwriter.Workbook(str(item[0]) + '.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '文件名')
        ws.write(0, 1, '标注文本')
        for file in item[1]:
            ws.write(row, 0, str(file))
            row += 1
        workbook.close()