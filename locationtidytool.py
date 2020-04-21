# @File  : locationtidytool.py
# @Author: LiuXingsheng
# @Date  : 2020/3/23
# @Desc  : 地理位置标签准确率测试

import xlrd
import demjson
from datatidytool import write2excel

CalcuPath = r'H:\大数据中台项目\标签测试报告\地理位置标签\家教机地理位置标签渠道数据源数据1k条_验证集_查询数据' + '_3.25.xlsx'
CorrectPath = r'H:\大数据中台项目\标签测试报告\地理位置标签\家教机地理位置标签渠道数据源数据1k条_标准数据_验证集' + '_处理后_3.25.xlsx'
ResultPath = r'H:\大数据中台项目\标签测试报告\地理位置标签\家教机地理位置标签渠道数据源数据1k条_验证集_测试结果' + '_3.25.xlsx'


def readCalcudata():
    calcudatadic = {}
    data = xlrd.open_workbook(CalcuPath)
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        locationstr = sheet.cell_value(row, 1)
        locationlist = getlocation(locationstr)
        calcudatadic.update({sheet.cell_value(row, 0): locationlist})
    return calcudatadic


def readCorrectdata():
    correctdict = {}
    machineList = []
    data = xlrd.open_workbook(CorrectPath)
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        machineList.append(sheet.cell_value(row, 0))
        province = getformalprovince(sheet.cell_value(row, 1))
        correctdict.update(
            {str(sheet.cell_value(row, 0)): province + str(sheet.cell_value(row, 2)) + str(
                sheet.cell_value(row, 3))})
    return correctdict, machineList


def getformalprovince(province):
    provincedic = {'湖南': '湖南省', '浙江': '浙江省', '新疆': '新疆维吾尔自治区', '江苏': '江苏省', '海南': '海南省', '黑龙江': '黑龙江省', '广东': '广东省',
                   '河北': '河北省', '四川': '四川省', '山西': '山西省', '甘肃': '甘肃省', '福建': '福建省', '陕西': '陕西省', '云南': '云南省',
                   '湖北': '湖北省',
                   '辽宁': '辽宁省', '内蒙古': '内蒙古自治区',
                   '吉林': '吉林省', '安徽': '安徽省', '广西': '广西壮族自治区', '宁夏': '宁夏回族自治区', '青海': '青海省', '西藏': '西藏自治区', '河南': '河南省',
                   '贵州': '贵州省', '山东': '山东省', '江西':'江西省','重庆': '重庆市','上海':'上海市'}
    return provincedic[province]


def compare(correctcp, calcudatadic):
    rightnumlist = []
    wrongnumlist = []
    nullnumlist = []
    machinelist = correctcp[1]
    correctdict = correctcp[0]
    for machine in machinelist:
        try:
            if correctdict[machine] in calcudatadic[machine]:
                rightnumlist.append((machine, correctdict[machine], calcudatadic[machine]))
            else:
                wrongnumlist.append((machine, correctdict[machine], calcudatadic[machine]))
        except KeyError as e:
            print('错误的值是', e.args)
            nullnumlist.append((machine, correctdict[machine], '无标签数据'))
    print('正确个数：{0} 错误个数：{1},无标签个数：{2} \n准确率：{3} 错误率：{4}'.format(len(rightnumlist),
                                                                 len(wrongnumlist), len(nullnumlist),
                                                                 (len(rightnumlist) / (
                                                                         len(rightnumlist) + len(wrongnumlist))),
                                                                 (len(wrongnumlist) / (
                                                                         len(rightnumlist) + len(wrongnumlist)))))
    write2excel(rightnumlist, wrongnumlist, ResultPath)


def getlocation(locationStr):
    locationlist = []
    if len(locationStr) < 5:
        return locationlist
    else:
        objdata = demjson.decode(locationStr)
        for item in objdata:
            locationlist.append(item['province'] + item['city'] + item['district'])
        return locationlist


def test():
    strtest = 'a'
    strlist = ['a']
    if strtest in strlist:
        print(True)
    else:
        print(False)


if __name__ == '__main__':
    calcudatadic = readCalcudata()
    correctcp = readCorrectdata()
    compare(correctcp, calcudatadic)
