# @File  : app_store_test.py
# @Author: LiuXingsheng
# @Date  : 2020/2/14
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import appstore_testUrlSet
import requests
import demjson
import xlsxwriter
import xlrd
import os

Path = r'D:\appstoremachineid'
manager = domainManager.DomainManager()
manager.setDomainType(constants.TestDomainType_Asia)
manager.setItemName(constants.app_store_api_pad)


def test_getAllmachineid():
    machineidlist = []
    filelist = os.listdir(Path)
    for item in filelist:
        data = xlrd.open_workbook(os.path.join(Path, str(item)))
        test = data.sheets()[0]
        rows = test.nrows
        for row in range(1, rows):
            machineId = test.cell_value(row, 0)
            machineidlist.append(machineId)
    return machineidlist


def getFreeTimeUpdateGroup(machineidList):
    resultlist = []
    count = 0
    url = manager.getDomain() + appstore_testUrlSet.AppstoreUrlSet['getFreeTimeUpdateGroup']
    for machineid in machineidList:
        print('计数为：', count)
        count += 1
        result = requests.post(url=url, params={'machineId': str(machineid)})
        if result.status_code != requests.codes.ok:
            print('服务器错误')
        else:
            data = demjson.decode(result.text)
            if data:
                resultlist.append((machineid, data['data']))
    column = 1
    workbook = xlsxwriter.Workbook(os.path.join(os.getcwd(), 'groupInfo.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    ws.write(0, 0, '序列号')
    ws.write(0, 1, '分组id')
    for item in resultlist:
        ws.write(column, 0, str(item[0]))
        ws.write(column, 1, str(item[1]))
        column = column + 1
    workbook.close()


def freeTimeUpdate():
    url = manager.getDomain() + appstore_testUrlSet.AppstoreUrlSet['freeTimeUpdate']
    param = {'machineId': '700K57A0005EW','apkPackageNameAndApkVersionCode':'','gradeId':'3'}
        # ,'deviceModel':'S3 Pro','deviceOsVersion':'V1.0.0','apkPackageNameAndApkVersionCode':'1.0.0','validate':'2',
        #      'gradeId':'3'}
    print(url)
    result = requests.post(url=url, params=param)
    print(result.text)


if __name__ == '__main__':
    # idList = getAllmachineid()
    # getFreeTimeUpdateGroup(idList)
    freeTimeUpdate()
