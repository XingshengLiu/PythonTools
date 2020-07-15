# @File  : learningprocessAreaAccuracy.py
# @Author: LiuXingsheng
# @Date  : 2020/5/28
# @Desc  :
import os
import xlrd
import xlsxwriter

DirPath = r'C:\Users\Administrator\Desktop'
def readStandardData():
    startdandardic = {}
    singrecord = []
    data = xlrd.open_workbook(os.path.join(DirPath, '地区学习进度标准结果.xlsx'))
    sheet = data.sheets()[0]
    sheetrows = sheet.nrows
    sheetcolumns = sheet.ncols
    for row in range(1,sheetrows):
        for clo in range(1,sheetcolumns):
            singrecord.append(sheet.cell_value(row, clo))
        if singrecord:
            startdandardic.update({sheet.cell_value(row, 0):singrecord})
        singrecord = []
    return startdandardic

def getColumnIndex(table, columnlist):
    columndic = {}
    for i in range(table.ncols):
        for column in columnlist:
            if (table.cell_value(0, i) == column):
                columndic.update({column: i})
    return columndic

def readresultData():
    grade = ''
    singrecorddic = {}
    resultlist = []
    columnlist = ['年级', '书本', '单元', '小节', '知识点']
    data = xlrd.open_workbook(os.path.join(DirPath, 'arearesult.xlsx'))
    sheet = data.sheets()[0]
    columndic = getColumnIndex(sheet, columnlist)
    print(columndic)
    for row in range(1, sheet.nrows):
        for column in columnlist:
            if ',' in str(sheet.cell_value(row, columndic[column])):
                resultlist.append(str(sheet.cell_value(row, columndic[column])))
            if sheet.cell(row, columndic[column]).ctype == 2 and column != '年级':
                resultlist.append(int(sheet.cell_value(row, columndic[column])))
            if column == '年级':
                grade = int(sheet.cell_value(row, columndic[column]))
        singrecorddic.update({grade: resultlist})
        resultlist = []
    print(singrecorddic)
    return singrecorddic

def formaldata(data):
    return str(data).strip().replace('\'', '')

def calcuareaaccuracy(stdrecorddic,calrecorddic):
    print(calrecorddic)
    completelist = []
    signresultrecord = []
    successcount = [0, 0, 0, 0, 0]
    gradelist = ['14','15','16','17','18','19']
    for grade in gradelist:
        std_list = stdrecorddic[grade]
        cal_list = calrecorddic[int(grade)]
        if formaldata(std_list[0]) == formaldata(cal_list[0]):
            signresultrecord.append(1)
        else:
            signresultrecord.append(0)
        if formaldata(std_list[1]) == formaldata(cal_list[1]):
            signresultrecord.append(1)
        else:
            signresultrecord.append(0)
        if formaldata(std_list[2]) == formaldata(cal_list[2]):
            signresultrecord.append(1)
        else:
            signresultrecord.append(0)
        if formaldata(cal_list[3]) in formaldata(std_list[4]):
            signresultrecord.append(1)
        else:
            signresultrecord.append(0)
        if '0' in str(signresultrecord):
            signresultrecord.append(0)
        else:
            signresultrecord.append(1)
        completelist.append((grade,std_list + cal_list + signresultrecord))
        print(len(signresultrecord))
        for i in range(len(signresultrecord)):
            if signresultrecord[i] == 1:
                successcount[i] += 1
        signresultrecord = []
    print('年级、书本、单元、小节、知识点、学习进度准确率分别为：')
    for item in successcount:
        print(item / len(gradelist))
    return completelist

def writecontent(completelist):
    titlelist = [('标准年级', '标准书本', '标准单元', '标准节', '标准做题记录', '标准知识点',
                  '大数据书本', '大数据单元', '大数据节', '大数据知识点',
                  '书本准确率', '单元准确率', '节准确率', '知识点准确率', '学习进度准确率')]
    alllist = titlelist +completelist
    workbook = xlsxwriter.Workbook(os.path.join(DirPath,'区域学习进度准确率.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(alllist)):
        for column in range(len(alllist[row])):
            if row == 0:
                ws.write(row, column, alllist[row][column])
            else:
                if column >= 1:
                    for i in range(len(alllist[row][column])):
                        ws.write(row, i+1, alllist[row][column][i])
                else:
                    ws.write(row, column, alllist[row][column])
    workbook.close()

if __name__ == '__main__':
    stdrecorddic = readStandardData()
    calrecorddic = readresultData()
    acculist = calcuareaaccuracy(stdrecorddic,calrecorddic)
    writecontent(acculist)