# @File  : upperMachineid.py
# @Author: LiuXingsheng
# @Date  : 2020/3/24
# @Desc  : 采集的序列号转化为大写
import xlrd
import xlsxwriter

CalcuPath = r'H:\大数据中台项目\标签测试报告\地理位置标签\家教机地理位置标签渠道数据源数据1k条_标准数据_验证集' + '_3.25.xlsx'
ProcessedPath = r'H:\大数据中台项目\标签测试报告\地理位置标签\家教机地理位置标签渠道数据源数据1k条_标准数据_验证集_处理后' + '_3.25.xlsx'
Type = 'nosql'


def preprocessData():
    locationlist = []
    data = xlrd.open_workbook(CalcuPath)
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        if Type == 'sql':
            machineId = '\'' + sheet.cell_value(row, 0).upper() + '\','
        else:
            machineId = sheet.cell_value(row, 0).upper()
        locationlist.append((machineId, sheet.cell_value(row, 1), sheet.cell_value(row, 2), sheet.cell_value(row, 3)))
    return locationlist


def write2file(locationlist):
    workbook = xlsxwriter.Workbook(ProcessedPath)
    ws = workbook.add_worksheet(u'统计结果')
    i = 1
    for item in locationlist:
        ws.write(i, 0, item[0])
        ws.write(i, 1, item[1])
        ws.write(i, 2, item[2])
        ws.write(i, 3, item[3])
        i += 1
    workbook.close()


if __name__ == '__main__':
    datalist = preprocessData()
    write2file(datalist)
