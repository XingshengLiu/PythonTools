# @File  : appstoretool.py
# @Author: LiuXingsheng
# @Date  : 2019/8/6
# @Desc  : 商店专项测试工具

import requests, demjson, xlrd, os, xlsxwriter
from AppstoreUniqueTool.appbean import ApkObject


def readContent():
    apkNameList = []
    filelist = os.listdir(os.getcwd())
    for file in filelist:
        if file.endswith('.xlsx'):
            temp = file
            break
        else:
            continue
    data = xlrd.open_workbook(os.getcwd() + '\\' + temp)
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(rows):
        apkBean = ApkObject(sheet.cell_value(row, 0).strip(), " ", " ")
        apkNameList.append(apkBean)
    return apkNameList


def writecontent(cmpltNameList):
    column = 1
    try:
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + '搜索结果统计.xlsx')
        titleform = workbook.add_format(setTitleProperty())
        contentform = workbook.add_format(setContentProperty())
        ws = workbook.add_worksheet(u'sheet1')
        ws.set_column("A:C",30)
        ws.write(0, 0, '应用名称', titleform)
        ws.write(0, 1, '搜索结果', titleform)
        ws.write(0, 2, '结果(True 为成功，False 为失败)', titleform)
        for bean in cmpltNameList:
            ws.write(column, 0, bean.origianlApkName,contentform)
            ws.write(column, 1, bean.searchApkName,contentform)
            ws.write(column, 2, bean.result,contentform)
            column = column + 1
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))


def setTitleProperty():
    return {
        'font_size': 11,  # 字体大小
        'font_color': '#FFFFFF',
        'bold': True,  # 是否加粗
        'align': 'center',  # 水平对齐方式
        'valign': 'vcenter',  # 垂直对齐方式
        'font_name': u'微软雅黑',
        'text_wrap': False,  # 是否自动换行
        'fg_color': '#00B0F0'
    }


def setContentProperty():
    return {
        'font_size': 11,  # 字体大小
        'font_color': '#000000',
        'bold': False,  # 是否加粗
        'align': 'center',  # 水平对齐方式
        'valign': 'vcenter',  # 垂直对齐方式
        'font_name': u'微软雅黑',
        'text_wrap': False,  # 是否自动换行
    }


def getAPkByKeyWords(apkNameList):
    url = 'http://h600s.eebbk.net/app/apkInfoApiOk100//businessLike/getAPkByKeyWords'
    for item in apkNameList:
        param = {'oppoBzSdk': '280', 'deviceModel': 'S3', 'machineId': '700S376000FA4',
                 'apkName': str(item.origianlApkName),
                 'gradeId': '3',
                 'deviceOSVersion': 'V1.3.3_180608'}
        result = requests.post(url=url, params=param)
        resultobj = demjson.decode(result.text)
        if resultobj['data'] is not None:
            apkList = resultobj['data']['apks']
            print('输入应用名: {0}, 返回应用名: {1}'.format(item.origianlApkName, apkList[0]['apkName']))
            item.searchApkName = str(apkList[0]['apkName'].strip())
            if item.searchApkName == item.origianlApkName:
                item.result = 'True'
            else:
                item.result = 'False'
    return apkNameList


if __name__ == '__main__':
    apkNameList = readContent()
    cmpltList = getAPkByKeyWords(apkNameList)
    writecontent(cmpltList)

