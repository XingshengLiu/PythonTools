# @File  : accask.py
# @Author: LiuXingsheng
# @Date  : 2020/8/14
# @Desc  : 精准问答测试
import json
import os
import requests
import xlrd
import xlsxwriter

path = r'H:\内容中台\知识图谱项目\用户数据测试集\精准问答'
url = 'http://112.47.35.7:8002/ask-homework/qa/kbqa_math'  # 知识问答测试环境


def kbqa_online(query):
    data_obj = {'query': query}
    r = requests.post(url, json.dumps(data_obj))
    try:
        res = r.json()
        print(res)
        return res
    except:
        print(r.text)
        return ''


def readLabel():
    sentencelist = []
    filepath = os.path.join(path, '100构造测试集_v2.xlsx')
    contentdata = xlrd.open_workbook(filepath)
    sheets = contentdata.sheets()
    for sheet in sheets:
        for row in range(1, sheet.nrows):
            sentencelist.append([sheet.cell_value(row, 0), sheet.cell_value(row, 1),
                                 sheet.cell_value(row, 2),sheet.cell_value(row, 3)])
    return sentencelist


def compare(sentencelist):
    print(len(sentencelist))
    count = 0
    resultlist = []

    for sentence in sentencelist:
        res = kbqa_online(sentence[0])
        count += 1
        print(count)
        try:
            if res != '' and ('entity' in res) and ('property' in res) and ('answer' in res):
                if sentence[1] == res['entity']['value'] and sentence[2] == res['property']:
                    if ('text' in res['answer']) and (sentence[3] == res['answer']['text']):
                        resultlist.append(
                            [res['query'], res['entity']['value'], res['property'], res['answer']['text'], sentence[3],
                             '1', '1'])
                    else:
                        if 'text' in res['answer']:
                            resultlist.append(
                                [res['query'], res['entity']['value'], res['property'], res['answer']['text'], sentence[3],
                                 '1', '0'])
                        else:
                            resultlist.append(
                                [res['query'], res['entity']['value'], res['property'], '答案为空', sentence[3],
                                 '1', '0'])
                else:
                    if 'text' in res['answer']:
                        resultlist.append(
                            [res['query'], res['entity']['value'], res['property'], res['answer']['text'], sentence[3], '0',
                             '0'])
                    else:
                        resultlist.append(
                            [res['query'], res['entity']['value'], res['property'], '答案为空', sentence[3], '0',
                             '0'])
            else:
                resultlist.append([sentence[0], '未返回', '未返回', '未返回', sentence[3], '0','0'])
        except:
            print('异常')
            resultlist.append([sentence[0], '未知错误', '未知错误', '未知错误', sentence[3], '0', '0'])
    return resultlist


def writeContent(resultlist):
    workbook = xlsxwriter.Workbook(os.path.join(path, '100构造测试结果_v2new.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(resultlist)):
        for column in range(len(resultlist[row])):
            ws.write(row, column, str(resultlist[row][column]))
    workbook.close()


if __name__ == '__main__':
    sentencelist = readLabel()
    resultlist = compare(sentencelist)
    writeContent(resultlist)
