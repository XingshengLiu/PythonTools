# @File  : getAllPicName.py
# @Author: LiuXingsheng
# @Date  : 2019/5/31
# @Desc  : 工具类：1. 获取所有图片名称生成excel 2. 包含导入大数据平台的数据转换函数

import xlsxwriter, os, base64, xlrd
from xlrd import xldate_as_tuple
from datetime import datetime
import csv
import json
import requests
import collections

DIR_PATH = r'H:\内容中台\精准搜题项目\测试集\作业工具月报测试集\opensearch'


def getAllPic():
    picList = []
    filelist = os.listdir(DIR_PATH)
    for file in filelist:
        # if file.endswith('.JPEG') or file.endswith('.jpg') or file.endswith('.bmp') or file.endswith('.png'):
        if file.endswith('.html'):
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
        with open(DIR_PATH + '\\' + 'b64_kousuanpics1.txt', 'a+', encoding='utf-8') as fwrite:
            with open(DIR_PATH + '\\' + pic, 'rb') as f:
                base64str = base64.b64encode(f.read())
                # OCR 4.0 转base64 需求
                # fwrite.write(str(pic) + ',' + str(orlist[2]) + ',' + str(orlist[3]) + ',' + str(pic) +   ',' + str(base64str,encoding='utf-8') + ',' + '\n')
                # 口算图片 转base64 需求 20200709
                fwrite.write(str(base64str,encoding='utf-8') + ',' + '\n')
                fwrite.flush()


def convertonline():
    DirPath = r'C:\Users\Administrator\Desktop\quesitonid对应关系\Z计划整机学习进度_构造测试集\7_名师_快搜_好题'
    resultdata = xlrd.open_workbook(os.path.join(DirPath, 'onlinelesson_7.xlsx'))
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
        with open(os.path.join(DirPath, 'onlinelesson_7_individual.txt'), 'a+', encoding='utf-8') as fwrite:
            fwrite.write(content + '\n')
            fwrite.flush()


def renamePic():
    picList = []
    filelist = os.listdir(DIR_PATH)
    for file in filelist:
        if file.endswith('.JPEG') or file.endswith('.jpg') or file.endswith('.bmp') or file.endswith('.png'):
            # if file.endswith('.html'):
            picList.append(file)
        else:
            pass
    for pic in picList:
        os.rename(os.path.join(DIR_PATH, pic), os.path.join(DIR_PATH, 'material_' + pic))


def findTwoBox():
    jsonList = []
    filelist = os.listdir(DIR_PATH)
    print(len(filelist))
    for file in filelist:
        if file.endswith('.json'):
            # if file.endswith('.html'):
            jsonList.append(file)
        else:
            pass
    for file in jsonList:
        with open(os.path.join(DIR_PATH, file), 'r') as f:
            json_data = json.load(f)
            if json_data['shapes'] == 2:
                print(json)
            else:
                pass


def getCheckSheet():
    originallist = []
    resultdata = xlrd.open_workbook(os.path.join(DIR_PATH, '搜题错误.xlsx'))
    resultsheet = resultdata.sheets()[0]
    rows = resultsheet.nrows
    columns = resultsheet.ncols
    for row in range(1, rows):
        item = []
        for clo in range(columns):
            item.append(resultsheet.cell_value(row, clo))
        if row < 10:
            item.append('00' + str(row) + '.jpg')
            item.append('00' + str(row) + '.html')
        elif 10 <= row < 100:
            item.append('0' + str(row) + '.jpg')
            item.append('0' + str(row) + '.html')
        else:
            item.append(str(row) + '.jpg')
            item.append(str(row) + '.html')
        originallist.append(item)
    titlelist = [['序列号','粗框图','标注Id','返回id','相同Id','第几屏相同','五屏结果','首屏结果','请求耗时','html文档','重命名图','重命名html']]
    cmpltlist = titlelist + originallist
    workbook = xlsxwriter.Workbook(DIR_PATH + '\\' + '整理文件_opensearch错误.xlsx')
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(cmpltlist)):
        for col in range(len(cmpltlist[row])):
            ws.write(row, col, cmpltlist[row][col])
    workbook.close()
    for pic in originallist:
        os.rename(os.path.join(DIR_PATH,pic[1]),os.path.join(DIR_PATH,pic[10]))
        os.rename(os.path.join(DIR_PATH, pic[9]), os.path.join(DIR_PATH, pic[11]))




def main():
    # findTwoBox()
    # getAllPic()
    # renamePic()
    # writebase64_2txt()
    # convertonline()
    getCheckSheet()


if __name__ == '__main__':
    main()
