# @File  : datatidytool.py
# @Author: LiuXingsheng
# @Date  : 2020/3/9
# @Desc  : 年级标签准确率测试 修改三处数据 1. Type 修改为对应类型 2. 修改标签数据测试文件标题 3. 修改标签测试结果文件标题


import xlrd
import xlsxwriter

Type = 'Grade'
Path = r'H:\大数据中台项目\标签测试报告\年级标签\系统管理部数据\系统管理部年级标签1w数据_验证集' + '.xlsx'
Pathresult = r'H:\大数据中台项目\标签测试报告\年级标签\系统管理部数据\系统管理部年级标签1w数据_验证集_加入机型统计' + '_4.10测试结果.xlsx'


def readandcompare():
    specialrightcount = 0
    specialwrongcount = 0
    correctdict = {}
    calcudict = {}
    machineList = []
    correctList = []
    wrongList = []
    nullList = []
    notalivablelist = []
    data = xlrd.open_workbook(Path)
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        machineList.append(sheet.cell_value(row, 0).replace(' ', ''))
        correctdict.update({str(sheet.cell_value(row, 0).replace(' ', '')): str(sheet.cell_value(row, 1))})
        calcudict.update({str(sheet.cell_value(row, 2)).strip(): str(sheet.cell_value(row, 3))})
    for machine in machineList:
        model = machine[2:4]
        correctdatalist = normalizeCorrectGrade(str(correctdict[machine].replace(' ', '')))
        if len(correctdatalist) == 1 and ('高中' in correctdatalist or '无保卡数据' in correctdatalist):
            notalivablelist.append(machine)
        else:
            try:
                calcudatalist = normalizeCalculateGrade(calcudict[machine])
                if set(calcudatalist) & set(correctdatalist):
                    correctList.append((machine, correctdatalist, calcudatalist, model))
                    if model == 'S5':
                        if len(correctdatalist) == 1 and (
                                '7' in correctdatalist or '8' in correctdatalist or '9' in correctdatalist):
                            pass
                        else:
                            specialrightcount += 1
                    else:
                        pass
                else:
                    wrongList.append((machine, correctdatalist, calcudatalist, model))
                    if model == 'S5':
                        if len(correctdatalist) == 1 and (
                                '7' in correctdatalist or '8' in correctdatalist or '9' in correctdatalist):
                            pass
                        else:
                            specialwrongcount += 1
                    else:
                        pass
            except KeyError as e:
                print(e.args)
                nullList.append((machine, correctdatalist, '无标签数据'))
    print('S5 正确个数 {0} 错误个数 {1}'.format(specialrightcount, specialwrongcount))
    print('正确个数：{0} 错误个数：{1},无标签个数：{2} \n'
          '准确率：{3} 错误率：{4} S5机型 不包含初中、高中准确率{5}'.format(len(correctList),
                                                       len(wrongList), len(nullList),
                                                       (len(correctList) / (
                                                               len(correctList) + len(
                                                           wrongList))),
                                                       (len(wrongList) / (
                                                               len(correctList) + len(
                                                           wrongList))),
                                                       specialrightcount / (
                                                               specialwrongcount + specialrightcount)))
    print('无效数据共', len(notalivablelist))
    return correctList, wrongList


def test():
    label = ['5', '1']
    test = ['1', '2', '3', '4']
    for item in label:
        if item in test:
            print(True)
        else:
            print(False)
    if (set(label) & set(test)):
        print(True)
    else:
        print(False)


def normalizeCorrectGrade(grade):
    grademultinumlist = []
    gradesignlenumlist = []
    if Type == 'Grade':
        if not grade:
            gradesignlenumlist.append('无保卡数据')
            return gradesignlenumlist
        if grade == '高中':
            gradesignlenumlist.append('高中')
            return gradesignlenumlist
        if ',' in grade:
            gradenamelist = grade.split(',')
            for gradename in gradenamelist:
                grademultinumlist.append(gradedic[gradename])
            return grademultinumlist
        else:
            gradesignlenumlist.append(gradedic[grade])
            return gradesignlenumlist
            # if grade == '一年级' or grade == '1年级':
            #     return 1
            # elif grade == '二年级' or grade == '2年级':
            #     return 2
            # elif grade == '三年级' or grade == '3年级':
            #     return 3
            # elif grade == '四年级' or grade == '4年级':
            #     return 4
            # elif grade == '五年级' or grade == '5年级':
            #     return 5
            # elif grade == '六年级' or grade == '6年级':
            #     return 6
            # elif grade == '七年级' or grade == '7年级' or grade == '初一':
            #     return 7
            # elif grade == '八年级' or grade == '8年级' or grade == '初二':
            #     return 8
            # elif grade == '九年级' or grade == '9年级' or grade == '初三':
            #     return 9
            # elif grade == '高一':
            #     return 10
            # elif grade == '高二':
            #     return 11
            # elif grade == '高三':
            #     return 12
    else:
        return grade


def normalizeCalculateGrade(grade):
    if ',' in grade:
        return grade.split(',')
    else:
        return grade


def write2excel(corectlist, wronglist, pathresult):
    workbook = xlsxwriter.Workbook(pathresult)
    ws = workbook.add_worksheet(u'统计结果')
    titleform = workbook.add_format(setTitleProperty())
    wrongcontent = workbook.add_format(setWrongProperty())
    correctcontent = workbook.add_format(setContentProperty())
    ws.set_column("A:D", 30)
    ws.write(0, 0, '序列号', titleform)
    ws.write(0, 1, '正确数据', titleform)
    ws.write(0, 2, '标签数据', titleform)
    ws.write(0, 3, '机型', titleform)
    i = 1
    for citem in corectlist:
        ws.write(i, 0, citem[0], correctcontent)
        ws.write(i, 1, str(citem[1]), correctcontent)
        ws.write(i, 2, str(citem[2]), correctcontent)
        ws.write(i, 3, str(citem[3]), correctcontent)
        i += 1
    for witem in wronglist:
        ws.write(i, 0, witem[0], correctcontent)
        ws.write(i, 1, str(witem[1]), correctcontent)
        ws.write(i, 2, str(witem[2]), wrongcontent)
        ws.write(i, 3, str(witem[3]), correctcontent)
        i += 1
    workbook.close()


def setContentProperty():
    return {
        'font_size': 11,
        'font_color': '#000000',
        'bold': False,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': u'微软雅黑',
        'text_wrap': False,
    }


def setWrongProperty():
    return {
        'font_size': 11,
        'font_color': '#FE315D',
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': u'微软雅黑',
        'text_wrap': False,
    }


def setTitleProperty():
    return {
        'font_size': 11,
        'font_color': '#FFFFFF',
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': u'微软雅黑',
        'text_wrap': False,
        'fg_color': '#00B0F0'
    }


gradedic = {'一年级': '1', '二年级': '2', '三年级': '3', '四年级': '4',
            '五年级': '5', '六年级': '6', '七年级': '7', '八年级': '8', '九年级': '9', '高中': '高中', '学龄前': '13'}

if __name__ == '__main__':
    corectlist, wronglist = readandcompare()
    write2excel(corectlist, wronglist, Pathresult)
    # test()
