# @File  : questionlike_label.py
# @Author: LiuXingsheng
# @Date  : 2020/10/10
# @Desc  : 习题点赞标签
import os
import xlrd
import xlsxwriter
import collections

filepath = r'H:\大数据中台项目\标签测试报告\习题反馈标签\习题反馈提测数据'

def readLikeExcel():
    question_machinelist = collections.defaultdict(list)
    question_countdic = {}
    contentdata = xlrd.open_workbook(os.path.join(filepath, '习题收藏点赞点踩数据原始数据.xlsx'))
    sheets = contentdata.sheets()
    for sheet in sheets:
        for row in range(1, sheet.nrows):
            # 点赞标签需对ishelpful进行1的判断,反馈次数标签无需进行判断
            # if sheet.cell_value(row, 3) == 1:
            question_machinelist[sheet.cell_value(row, 2)].append(sheet.cell_value(row, 11))
            # else:
            #     pass
    for key in question_machinelist.keys():
        question_countdic[key] = len(question_machinelist[key])
    print(question_countdic,len(question_countdic))
    return question_countdic

def readOriginalData():
    question_simplecountdict = {}
    questionlist = []
    contentdata = xlrd.open_workbook(os.path.join(filepath, '习题反馈图片数据原始数据.xlsx'))
    sheets = contentdata.sheets()
    for sheet in sheets:
        for row in range(1, sheet.nrows):
            questionlist.append(str(int(sheet.cell_value(row, 1))))
    questionset = set(questionlist)
    for question in questionset:
        question_simplecountdict[question] = questionlist.count(question)
    print(question_simplecountdict)
    return question_simplecountdict



if __name__ == '__main__':
    wholedict = {}
    question_countdic = readLikeExcel()
    question_simplecountdict = readOriginalData()
    print(type(question_simplecountdict.keys()))
    for key in question_simplecountdict.keys():
        if question_countdic.get(key):
            wholedict[key] = question_countdic[key] + question_simplecountdict[key]
        else:
            wholedict[key] = question_simplecountdict[key]
    for key_1 in question_countdic.keys():
        if wholedict.get(key_1):
            pass
        else:
            wholedict[key_1] = question_countdic[key_1]
    workbook = xlsxwriter.Workbook(os.path.join(filepath, '整合反馈数据.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    row = 0
    for key in wholedict.keys():
        ws.write(row, 0, key)
        ws.write(row, 1, wholedict[key])
        row += 1
    workbook.close()