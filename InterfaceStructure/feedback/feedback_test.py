# @File  : feedback_test.py
# @Author: LiuXingsheng
# @Date  : 2020/4/15
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import feedback_testUrlSet
import requests
import xlrd

manager = domainManager.DomainManager()
manager.setDomainType(constants.TestDomainType_Asia)
manager.setItemName(constants.feedback)
DIR_PATH = r'C:\Users\Administrator\Desktop\fb_customquestion.xls'


def getalldata():
    datalist = []
    data = xlrd.open_workbook(DIR_PATH + '\\' + '图片名.xlsx')
    sheet = data.sheets()[0]
    for row in range(1, sheet.nrows):
        datalist.append((sheet.cell_value(row, 1), sheet.cell_value(row, 2), sheet.cell_value(row, 3),
                         sheet.cell_value(row, 4), sheet.cell_value(row, 5)))
    return datalist

def selectCustomQuestion(datalist):
    url = manager.getDomain() + feedback_testUrlSet.FeedbackUrlSet['selectCustomQuestion']
    print(url)
    for data in datalist:
        requests.get(url=url, params={'':'','':'','':'','':'','':''})
