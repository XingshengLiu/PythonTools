# @File  : learningprocessAccuracy_v2.py
# @Author: LiuXingsheng
# @Date  : 2020/6/8
# @Desc  :
import os
import csv
import xlrd
import xlsxwriter

DirPath = r'C:\Users\Administrator\Desktop'
def readStandardData():
    """
    一张表一张表算最好，不要算整体的，程序此处已支持多张表数据全部读出，但是不好分情况统计，最好按7种场景让大数据提供数据
    最后可以把7张表放在一起，大数据的所有数据也放在一起，得出一个整体的准确率
    :return:
    """
    signrecord = []
    signrecordwithmachineId = {}
    data = xlrd.open_workbook(os.path.join(DirPath, 'Z计划学习进度测试结果_标准对照.xlsx'))
    machineIdlist = []
    for sheet in data.sheets():
        sheetrows = sheet.nrows
        sheetcolumns = sheet.ncols
        for row in range(2, sheetrows):
            for column in range(3, sheetcolumns):
                if sheet.cell_value(row, 2):
                    if column == 8:
                        value = sheet.cell_value(row, column).replace('{', '').replace('}', '')
                        signrecord.append(value)
                    else:
                        signrecord.append(sheet.cell_value(row, column))
                else:
                    break
            if signrecord:
                signrecordwithmachineId.update({sheet.cell_value(row, 2): signrecord})
            signrecord = []
            if sheet.cell_value(row, 2):
                machineIdlist.append(sheet.cell_value(row, 2))
    print(signrecordwithmachineId)
    return signrecordwithmachineId, machineIdlist


def getoriginalData_csv_v2():
    singrecorddic = {}
    with open(os.path.join(DirPath, 'data_2020-06-08 09_03_26 PM——new.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    for item in rows[1:]:
        # 顺序及对应字段含义见下表
        # bookId,单元Id,小节Id,知识点Id
        singrecorddic.update({item[0]:[item[3],item[4],item[5],item[6]]})
    return singrecorddic

def formaldata(data):
    return str(data).strip().replace('\'', '')

def calcuaccuracy(stdrecorddic, calrecorddic, machinelist):
    accuracyrecordlist = []
    # 各项正确数量统计记录
    successcount = [0, 0, 0, 0, 0]
    signresultrecord = []
    for machine in machinelist:
        std_machinerecordlist = stdrecorddic[machine]
        try:
            cal_machinerecordlist = calrecorddic[machine]
            if formaldata(std_machinerecordlist[1]) == formaldata(cal_machinerecordlist[0]):
                signresultrecord.append(1)
            else:
                signresultrecord.append(0)
            if formaldata(std_machinerecordlist[2]) == formaldata(cal_machinerecordlist[1]):
                signresultrecord.append(1)
            else:
                signresultrecord.append(0)
            if formaldata(std_machinerecordlist[3]) == formaldata(cal_machinerecordlist[2]):
                signresultrecord.append(1)
            else:
                signresultrecord.append(0)
            if (',' in str(cal_machinerecordlist[3])) and (',' in std_machinerecordlist[5]):
                std_knoledgelist = formaldata(std_machinerecordlist[5]).split(',')
                cal_knoledgelist = cal_machinerecordlist[3].split(',')
                if calcusameornot(std_knoledgelist, cal_knoledgelist):
                    signresultrecord.append(1)
                else:
                    signresultrecord.append(0)
            else:
                if formaldata(cal_machinerecordlist[3]) in formaldata(std_machinerecordlist[5]):
                    signresultrecord.append(1)
                else:
                    signresultrecord.append(0)
            if '0' in str(signresultrecord):
                signresultrecord.append(0)
            else:
                signresultrecord.append(1)
            accuracyrecordlist.append((machine, std_machinerecordlist + cal_machinerecordlist + signresultrecord))
        except KeyError as e:
            # accuracyrecordlist.append((machine, std_machinerecordlist + ['无数据', '无数据', '无数据', '无数据', '无数据'] + [0, 0, 0, 0, 0, 0]))
            print('没有查询出此序列号', e.args)
        for i in range(len(signresultrecord)):
            if signresultrecord[i] == 1:
                successcount[i] += 1
        signresultrecord = []
    print('年级、书本、单元、小节、知识点、学习进度准确率分别为：')
    for item in successcount:
        print(item / len(accuracyrecordlist))
    return accuracyrecordlist


def calcusameornot(std_knoledgelist, cal_knoledgelist):
    flag = 0
    for std in std_knoledgelist:
        for cal in cal_knoledgelist:
            if std == cal:
                flag = 0
                break
            else:
                flag = 1
    return flag

def writecontent(accuracyrecordlist):
    titlelist = [('序列号', '标准年级', '标准书本', '标准单元', '标准节', '标准做题记录', '标准知识点',
                  '大数据书本', '大数据单元', '大数据节', '大数据知识点',
                  '书本准确率', '单元准确率', '节准确率', '知识点准确率', '学习进度准确率')]
    completelist = titlelist + accuracyrecordlist
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, Groupname + '数据源准确率.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(completelist)):
        for column in range(len(completelist[row])):
            if row == 0:
                ws.write(row, column, completelist[row][column])
            else:
                if column >= 1:
                    for i in range(len(completelist[row][column])):
                        ws.write(row, i + 1, completelist[row][column][i])
                else:
                    ws.write(row, column, completelist[row][column])
    workbook.close()


if __name__ == '__main__':
    Groupname = '优化版V2.1'
    stdrecorddic, machinelist =  readStandardData()
    calrecorddic = getoriginalData_csv_v2()
    accuracyrecordlist = calcuaccuracy(stdrecorddic, calrecorddic, machinelist)
    writecontent(accuracyrecordlist)