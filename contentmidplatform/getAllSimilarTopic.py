# @File  : getAllSimilarTopic.py
# @Author: LiuXingsheng
# @Date  : 2020/11/17
# @Desc  : 获取所有相似题
import os
import json
import requests
import xlrd
import xlsxwriter
import collections
FilePath = r'H:\内容中台\精准搜题项目\测试集\作业工具月报测试集\6月html'

def getLabelContent():
    datadiclist = collections.defaultdict(list)
    ContentData = xlrd.open_workbook(os.path.join(FilePath, '错误记录.xlsx'))
    Sheets = ContentData.sheets()
    for sheet in Sheets:
        for row in range(1, sheet.nrows):
            datadiclist[sheet.cell_value(row,0)].append(sheet.cell_value(row,1))
            datadiclist[sheet.cell_value(row, 0)].append(sheet.cell_value(row, 2))
            datadiclist[sheet.cell_value(row, 0)].append(sheet.cell_value(row, 3))
            datadiclist[sheet.cell_value(row, 0)].append(sheet.cell_value(row, 4))
    return datadiclist

def getAllSimilarTopic(datadiclist):
    alldiclist = collections.defaultdict(list)
    url = 'http://testaliyun.eebbk.net/ai-search/api/searchSimilarByQuestionId'
    for key in datadiclist.keys():
            topicidlist = []
            ids = datadiclist[key][1].replace('\'', '"')
            idsobj = json.loads(ids)
            for id in idsobj:
                result = requests.get(url=url,params={'questionId':str(id)})
                print(result.text)
                if result.status_code == requests.status_codes.codes.ok:
                    objdata = json.loads(result.text)
                    if objdata['data']:
                        for topicid in objdata['data']:
                            topicidlist.append(str(topicid['questionId']))
                    else:
                        pass
            alldiclist[key].append(datadiclist[key][0])
            alldiclist[key].append(list(set(topicidlist)))
            alldiclist[key].append(datadiclist[key][2])
            alldiclist[key].append(datadiclist[key][3])
    return alldiclist

def write(alldiclist):
    workbook = xlsxwriter.Workbook(os.path.join(FilePath,'整理文件_6月.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    row = 1
    for key in alldiclist.keys():
        ws.write(row, 0, str(key))
        ws.write(row, 1, str(alldiclist[key][0]))
        ws.write(row, 2, str(alldiclist[key][1]))
        ws.write(row, 3, str(alldiclist[key][2]))
        ws.write(row, 4, str(alldiclist[key][3]))
        row += 1
    workbook.close()

if __name__ == '__main__':
    datadiclist = getLabelContent()
    alldiclist = getAllSimilarTopic(datadiclist)
    write(alldiclist)
