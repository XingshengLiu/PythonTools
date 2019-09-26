# @File  : getAllPicName.py
# @Author: LiuXingsheng
# @Date  : 2019/5/31
# @Desc  : 获取所有图片名称生成excel

import xlsxwriter, os

DIR_PATH = r'\\172.28.1.23\ai数据素材\AI测试素材库\已标注素材\图像\OCR\印刷体\英文印刷体\第二季度OCR英文素材_1\纸张不平整'


def getAllPic():
    picList = []
    filelist = os.listdir(DIR_PATH)
    for file in filelist:
        if file.endswith('.JPEG') or file.endswith('.jpg') or file.endswith('.bmp'):
            picList.append(file)
        else:
            pass
    workbook = xlsxwriter.Workbook(DIR_PATH + '\\' + '图片名.xlsx')
    ws = workbook.add_worksheet(u'sheet1')
    ws.write(0, 0, '图片名称')
    column = 1
    for pic in picList:
        ws.write(column, 0, pic)
        column = column + 1
    workbook.close()


def main():
    getAllPic()


if __name__ == '__main__':
    main()
