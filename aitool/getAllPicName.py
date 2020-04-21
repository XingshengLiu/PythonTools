# @File  : getAllPicName.py
# @Author: LiuXingsheng
# @Date  : 2019/5/31
# @Desc  : 获取所有图片名称生成excel

import xlsxwriter, os

DIR_PATH = r'\\IT212339\test_data_for_v5\part1'


def getAllPic():
    picList = []
    filelist = os.listdir(DIR_PATH)
    for file in filelist:
        if file.endswith('.JPEG') or file.endswith('.jpg') or file.endswith('.bmp')or file.endswith('.png'):
            picList.append(file)
        else:
            pass
    workbook = xlsxwriter.Workbook(r'G:\JmeterPressureScript\5.0OCR' + '\\' + '图片名.xlsx')
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
