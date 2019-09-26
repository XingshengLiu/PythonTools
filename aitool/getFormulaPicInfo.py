# @File  : getFormulaPicInfo.py
# @Author: LiuXingsheng
# @Date  : 2019/6/25
# @Desc  :
import os,xlsxwriter
from os.path import join


def getAllPic():
    picList = []
    for root,dirs,files in os.walk(os.getcwd(),topdown=False):
        for name in files:
            fileName = os.path.join(root,name)
            if fileName.endswith('.jpg'):
                picList.append(fileName)
            else:
                pass
    return picList

def writeContent(picList):
    workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + '标注后的分类信息.xlsx')
    ws = workbook.add_worksheet(u'sheet1')
    ws.write(0, 0, '图片名称')
    column = 1
    for pic in picList:
        ws.write(column, 0, pic)
        column = column + 1
    workbook.close()

def main():
    picList = getAllPic()
    writeContent(picList)


if __name__ == '__main__':
    main()
