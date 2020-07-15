# @File  : getAllPicName.py
# @Author: LiuXingsheng
# @Date  : 2019/5/31
# @Desc  : 工具类：1. 获取所有图片名称生成excel 2. 包含导入大数据平台的数据转换函数

import xlsxwriter, os, base64,xlrd
from xlrd import xldate_as_tuple
from datetime import datetime
import csv


DIR_PATH = r'H:\业务中台\手写笔迹\0714素材\50_part1\导出数据\path'


def getAllPic():
    picList = []
    filelist = os.listdir(DIR_PATH)
    for file in filelist:
        # if file.endswith('.JPEG') or file.endswith('.jpg') or file.endswith('.bmp') or file.endswith('.png'):
        if file.endswith('.txt'):
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


def writebase64_2txt():
    """
    需求：
    ocr5.0 压测中发现bealshell preprocessor 会造成吞吐下降
    需要把图片转换为base64 写入文件中直接读取
    本次测试需求，把4.0的测试素材转成base64 ，用5.0的接口去验证，是因为渠道期望5.0能够支持手写图片
    :return:
    """
    picList = []
    filelist = os.listdir(DIR_PATH)
    for file in filelist:
        if file.endswith('.JPEG') or file.endswith('.jpg') or file.endswith('.bmp') or file.endswith('.png'):
            picList.append(file)
        else:
            pass
    for pic in picList:
        # OCR 4.0 转base64 需求 用于分割图片名称和坐标点
        # orlist = pic.split('_')
        with open(DIR_PATH + '\\' + 'b64_kousuanpics1.txt','a+',encoding='utf-8') as fwrite:
            with open(DIR_PATH + '\\' + pic, 'rb') as f:
                base64str = base64.b64encode(f.read())
                # OCR 4.0 转base64 需求
                # fwrite.write(str(pic) + ',' + str(orlist[2]) + ',' + str(orlist[3]) + ',' + str(pic) +   ',' + str(base64str,encoding='utf-8') + ',' + '\n')
                # 口算图片 转base64 需求 20200709
                fwrite.write(str(base64str,encoding='utf-8') + ',' + '\n')
                fwrite.flush()

def convertonline():
    DirPath = r'C:\Users\Administrator\Desktop\quesitonid对应关系\Z计划个人学习进度_构造测试集_内容V2\6_名师_快搜'
    resultdata = xlrd.open_workbook(os.path.join(DirPath,'onlinelesson_6.xlsx'))
    resultsheet = resultdata.sheets()[0]
    rows = resultsheet.nrows
    columns = resultsheet.ncols
    for row in range(1, rows):
        content = ''
        for i in range(columns):
            if resultsheet.cell(row, i).ctype == 3:
                date = datetime(*xldate_as_tuple(resultsheet.cell_value(row, i), 0))
                content += str(date.strftime("%Y-%m-%d %H:%M:%S")) + '\001'
            else:
                content += str(resultsheet.cell_value(row, i)) + '\001'
        with open(os.path.join(DirPath,'onlinelesson_6_individual.txt'),'a+',encoding='utf-8') as fwrite:
            fwrite.write(content + '\n')
            fwrite.flush()


def main():
    getAllPic()
    # writebase64_2txt()
    # convertonline()

if __name__ == '__main__':
    main()
