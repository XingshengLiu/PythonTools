# @File  : ordinatesplit.py
# @Author: LiuXingsheng
# @Date  : 2020/1/8
# @Desc  :
import os
import xlsxwriter


def getAllOrdinate():
    sourceList = []
    with open(r'C:\Users\Administrator\Desktop\pic.txt', 'r')as f:
        piclist = f.readlines()
    for item in piclist:
        itemlist = str(item).split('_')
        sourceList.append(
            ('/home/visitor/EAS/eas_samples/4.0/' + str(item).replace('\n', ''), itemlist[-4], itemlist[-3],str(item).replace('\n', '')))
    print(sourceList)
    workbook = xlsxwriter.Workbook(r'E:\PyGitHub\PythonTools\aitool\ailib' + '\source.xlsx')
    ws_detail = workbook.add_worksheet(u'sheet1')
    i = 1
    for source in sourceList:
        ws_detail.write(i, 0, source[0])
        ws_detail.write(i, 1, source[1])
        ws_detail.write(i, 2, source[2])
        ws_detail.write(i, 3, source[3])
        i += 1
    workbook.close()


if __name__ == '__main__':
    getAllOrdinate()

