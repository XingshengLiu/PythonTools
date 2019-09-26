# @File  : ocr_exactframeTest.py
# @Author: LiuXingsheng
# @Date  : 2019/8/21
# @Desc  :

import requests, demjson, xlrd,xlsxwriter,os
import AppstoreUniqueTool.appstoretool


class PicBean(object):
    picName = ''
    ids = ''
    searchids = ''
    result = ''

    def __init__(self, picName, ids, result='False'):
        self.picName = picName
        self.ids = ids
        self.result = result


def getExcelContent():
    beanList = []
    data = xlrd.open_workbook(r'')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        picBean = PicBean(sheet.cell_value(row, 0), sheet.cell_value(row, 1))
        beanList.append(picBean)
    return beanList


def ocrExactFrameTest(beanList):
    isFind = True
    for item in beanList:
        idList = item.ids.split('#')
        file = {'file': open(item.picName, 'rb')}
        result = requests.request(method='POST', url='', params={}, files=file)
        print(result.text)
        dataObject = demjson.decode(result.text)
        if dataObject['data'] is not None:
            for id in idList:
                for searchid in dataObject['data']['存储的id字段']:
                    item.searchids = dataObject['data']['存储的id字段']
                    if searchid == id:
                        isFind = True
                        item.result = 'True'
                        break
                if isFind:
                    break
                else:
                    pass
    return beanList

def writeContent2Excel(beanlist,fileName):
    try:
        column = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + fileName + '.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '图片名')
        ws.write(0, 1, '标注id')
        ws.write(0, 2, '搜索id')
        ws.write(0, 3, '结果')
        for item in beanlist:
            ws.write(column, 0, item.picname)
            ws.write(column, 1, item.trueText)
            ws.write(column, 2, item.recogText)
            ws.write(column, 3, item.result)
            ws.write(column, 4, item.suject)
            ws.write(column, 5, item.scene)
            column += 1
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))
