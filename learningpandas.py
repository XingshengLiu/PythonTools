# @File  : learningpandas.py
# @Author: LiuXingsheng
# @Date  : 2020/5/22
# @Desc  :
import os
import pandas as pd
import xlsxwriter


def test():
    dic1 = {'标题列1': '',
            '标题列2': ''
            }

    contentlist = [('内容', 'id', '数据'), ('测试内容', '123', 'test'), ('输入法', '222', 'test')]
    contentlist1 = [('内容', 'id', '数据'), ('测试内容', '123', 'aaaa'), ('输入法', '222', 'aaaaaa')]
    appendlist = [('内容', 'id', '数据'), ('测试内容', '123', 'aaaa')]
    df = pd.DataFrame(contentlist)
    df1 = pd.DataFrame(contentlist1)
    df.to_excel('pandanstest.xlsx', index=False)
    wiriter = pd.ExcelWriter('pandanstest.xlsx')
    df.to_excel(wiriter, sheet_name='Sheet1')
    df1.to_excel(wiriter, sheet_name='Sheet3')
    wiriter.save()


def write_excel_xlsx(workbook, sheetname, value):
    ws = workbook.add_worksheet(sheetname)
    for i in range(len(value)):
        for j in range(len(value[i])):
            ws.write(i, j, title[i][j])
    # workbook.close()


def writecompletetitle(workbook):
    ws = workbook.add_worksheet('completelist')
    ws.write(0, 0, 'machineId')
    ws.write(0, 1, 'questionId')
    ws.write(0, 2, '年级')
    ws.write(0, 3, '书本Id')
    ws.write(0, 4, '单元Id')
    ws.write(0, 5, '小节Id')
    ws.write(0, 6, '本题知识点Id')
    ws.write(0, 7, '本序列号所有questions')
    ws.write(0, 8, '本序列号学习的所有知识点')
    ws.write(0, 9, '本序列号questions的数量')
    return ws

def getlistlength(contetnlist):
    group1quesitons = []
    for question2 in contetnlist:
        group1quesitons.append(question2[0])
    return len(group1quesitons)
def writeuserrecord_v2_1(userrecord, num):
    questions = []
    knowledges = []
    # 每条做题记录的步长
    i = 1
    # 每组做题记录的步长
    j = 0
    workbook = xlsxwriter.Workbook(os.path.join("", str(10) + '档位_序列号练习题记录_test.xlsx'))
    ws0 = writecompletetitle(workbook)
    for i in range(len(userrecord)):
        # 随机策略一的写方法：@deprecated
        # for question in user[1][0]:
        # 随机策略二的写方法：
        for k in range(len(userrecord[i][1])):
            ws0.write(i, 0, userrecord[i][0])
            ws0.write(i, j + 1, userrecord[i][1][k])
            questions.append(userrecord[i][1][k][0])
            knowledges.append(userrecord[i][1][k][5])
        stepandnum = len(questions)
        ws0.write(j + stepandnum, 0, userrecord[i][0])
        ws0.write(j + stepandnum, 7, str(questions))
        ws0.write(j + stepandnum, 8, str(set(knowledges)))
        ws0.write(j + stepandnum, 9, stepandnum)
        j += stepandnum
        questions = []
        knowledges = []
    title = [['machineId','questionId']]
    if num == 1:
        pass
    elif num == 2:
        for i in range(2):
            write_excel_xlsx(workbook,'group' + str(i + 1),title)
    else:
        for i in range(3):
            write_excel_xlsx(workbook, 'group' + str(i + 1), title)
    group1j = 1
    group2j = 1
    group3j = 1
    for i in range(len(userrecord)):
        if num == 1:
            pass
        elif num == 2:
            test1(workbook,2,userrecord[i])
            for k in range(group1j,len(userrecord[i])):
                write_excel_xlsx(workbook,'gruop_be2',userrecord[i][2])
                write_excel_xlsx(workbook, 'gruop_be3', userrecord[i][3])
            stepandnum1 = getlistlength(userrecord[i][2])
            stepandnum2= getlistlength(userrecord[i][3])
            group1j += stepandnum1
            group2j += stepandnum2
        else:
            for k in range(group1j,len(userrecord[i])):
                write_excel_xlsx(workbook,'gruop_be2',userrecord[i][2])
                write_excel_xlsx(workbook, 'gruop_be3', userrecord[i][3])
                write_excel_xlsx(workbook, 'gruop_be4', userrecord[i][4])
            stepandnum1 = getlistlength(userrecord[i][2])
            stepandnum2= getlistlength(userrecord[i][3])
            stepandnum3 = getlistlength(userrecord[i][4])
            group1j += stepandnum1
            group2j += stepandnum2
            group3j += stepandnum3
    workbook.close()


def test1(workbook,num,resoucelist):
    gruopstep = 1
    for item in range(num):
        for i in range(gruopstep,len(resoucelist)):
            write_excel_xlsx(workbook, 'gruop_be' + str(item), resoucelist[i+2])
        getlistlength(resoucelist[i+2])

if __name__ == '__main__':
    # workbook = xlsxwriter.Workbook(os.path.join(os.getcwd(), str(10) + '档位_序列号练习题记录_test.xlsx'))
    # title = [('标题1', '标题2', '标题3', '标题4'), ('1', '2', '3', '4')]
    # write_excel_xlsx(workbook, '', title)
    test1()
