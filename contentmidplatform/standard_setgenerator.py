# @File  : standard_setgenerator.py
# @Author: LiuXingsheng
# @Date  : 2020/7/29
# @Desc  : 精准问答100%测试集生成
import os
import csv
import collections
import xlrd
import xlsxwriter

Dirpath = r'H:\内容中台\构造100%测试集'
PreFix = '前缀'
Suffix = '后缀'
Pre_Suffix = '前后缀组合'
# prefixconcepcp = ['概念', '公式', '特点', '表示方法', '性质', '画法', '度量']
# prefixexamplecp = ['举例', '例题', '知识视频讲解']
# prefixpurecp = ['纯知识点']
prefixdic = {'概念组前缀': ['概念', '公式', '特点', '表示方法', '性质', '画法', '度量'], '举例组前缀': ['举例', '例题', '知识视频讲解'],
             '纯知识点组前缀': ['纯知识点']}
suffixdic = {'纯知识点组后缀': ['纯知识点'], '概念组后缀': ['概念', '公式', '特点', '表示方法', '性质'], '画法组后缀': ['画法', '度量'],
             '举例组后缀': ['举例', '例题'], '知识讲解组后缀': ['知识视频讲解']}
# suffixconcepcp = ['概念', '公式', '特点', '表示方法', '性质']
# suffixteachercp = ['知识视频讲解']
# suffixexamplecp = ['举例', '例题']
# suffixpurecp = ['纯知识点']
# suffixdrawcp = ['画法', '度量']
pre_suffixdic = {'前后缀组合': ['概念', '公式', '表示方法', '例题', '性质', '纯知识点', '画法', '度量']}


# pre_suffixcp = ['概念', '公式','表示方法','例题','性质','纯知识点','画法', '度量']


def readThreeMetaData():
    typecollection = collections.defaultdict(list)
    data = xlrd.open_workbook(os.path.join(Dirpath, '三元组.xlsx'))
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        sentence = sheet.cell_value(row, 0)
        # intent = sheet.cell_value(row, 1)
        intent = 'testintent'
        if sentence.endswith('概念'):
            typecollection['概念'].append([sentence, intent])
        elif sentence.endswith('举例'):
            typecollection['举例'].append([sentence, intent])
        elif sentence.endswith('公式'):
            typecollection['公式'].append([sentence, intent])
        elif sentence.endswith('特点'):
            typecollection['特点'].append([sentence, intent])
        elif sentence.endswith('例题'):
            typecollection['例题'].append([sentence, intent])
        elif sentence.endswith('知识视频讲解'):
            typecollection['知识视频讲解'].append([sentence, intent])
        elif sentence.endswith('表示方法'):
            typecollection['表示方法'].append([sentence, intent])
        elif sentence.endswith('性质'):
            typecollection['性质'].append([sentence, intent])
        elif sentence.endswith('画法'):
            typecollection['画法'].append([sentence, intent])
        elif sentence.endswith('度量'):
            typecollection['度量'].append([sentence, intent])
        else:
            typecollection['纯知识点'].append([sentence, intent])
    return typecollection


def generatePrefixSentence(typecollection):
    """
    废弃方法，已重构精简
    :param typecollection:
    :return:
    """
    newsentencelist = []
    for key in typecollection.keys():
        if key in prefixconcepcp:
            with open(os.path.join(Dirpath, '概念组前缀.csv'), encoding='utf-8') as f:
                reader = csv.reader(f)
                prefixdatalist = [row for row in reader]
            for item in typecollection[key]:
                for pre in prefixdatalist:
                    print(type(pre), pre, type(item[0]))
                    newsentence = clearStr(pre) + item[0]
                    newsentencelist.append((newsentence, item[1]))
        if key in prefixexamplecp:
            with open(os.path.join(Dirpath, '举例组前缀.csv'), encoding='utf-8') as f:
                reader = csv.reader(f)
                prefixdatalist = [row for row in reader]
            for item in typecollection[key]:
                for pre in prefixdatalist:
                    newsentence = clearStr(pre) + item[0]
                    newsentencelist.append((newsentence, item[1]))
        if key in prefixpurecp:
            with open(os.path.join(Dirpath, '纯知识点组前缀.csv'), encoding='utf-8') as f:
                reader = csv.reader(f)
                prefixdatalist = [row for row in reader]
            for item in typecollection[key]:
                for pre in prefixdatalist:
                    newsentence = clearStr(pre) + item[0]
                    newsentencelist.append((newsentence, item[1]))
    workbook = xlsxwriter.Workbook(os.path.join(Dirpath, '前缀生成句子.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(newsentencelist)):
        for column in range(len(newsentencelist[row])):
            ws.write(row, column, newsentencelist[row][column])
    workbook.close()


def clearStr(data):
    return str(data).replace('\'', '').replace('[', '').replace(']', '')


def generateSentence(cptype, datadic, typecollection):
    targetlist = []
    filelist = os.listdir(Dirpath)
    for file in filelist:
        if file.endswith(cptype + '.csv'):
            targetlist.append(file)
        else:
            pass
    if cptype == PreFix:
        newsentencelist = joinSentence(targetlist, datadic, typecollection, connectPrefixSentence)
    elif cptype == Suffix:
        newsentencelist = joinSentence(targetlist, datadic, typecollection, connectSuffixSentence)
    else:
        newsentencelist = joinSentence(targetlist, datadic, typecollection, connectPreSufCPSentence)
    writefile(newsentencelist, cptype)


def joinSentence(targetlist, datadic, typecollection, func):
    newsentencelist = []
    for key in typecollection.keys():
        for file in targetlist:
            if key in datadic[file[:-4]]:
                with open(os.path.join(Dirpath, file), encoding='utf-8') as f:
                    reader = csv.reader(f)
                    ffixdatalist = [row for row in reader]
                print('-------', ffixdatalist)
                for item in typecollection[key]:
                    for pre in ffixdatalist:
                        newsentence = func(clearStr(pre), item[0])
                        newsentencelist.append((newsentence, item[1]))
    return newsentencelist


def connectPrefixSentence(ffix, content):
    return ffix + content

def connectSuffixSentence(ffix, content):
    return content + ffix


def connectPreSufCPSentence(ffix, content):
    return ffix.replace(', ', content)


def writefile(newsentencelist, cptype):
    workbook = xlsxwriter.Workbook(os.path.join(Dirpath, cptype + '生成句子_newVersion.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(newsentencelist)):
        for column in range(len(newsentencelist[row])):
            ws.write(row, column, newsentencelist[row][column])
    workbook.close()


if __name__ == '__main__':
    typecollection = readThreeMetaData()
    # generateSentence(PreFix, prefixdic, typecollection)
    # generateSentence(Suffix, suffixdic, typecollection)
    generateSentence(Pre_Suffix, pre_suffixdic, typecollection)
