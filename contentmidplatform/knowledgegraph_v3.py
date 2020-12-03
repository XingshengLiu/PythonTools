# @File  : knowledgegraph_v3.py
# @Author: LiuXingsheng
# @Date  : 2020/9/25
# @Desc  : 知识图谱v3
import requests
import xlrd
import xlsxwriter
import os
import demjson
Dirpath = r'C:\Users\Administrator\Desktop'

def readExcel():
    datalist = []
    contentdata = xlrd.open_workbook(os.path.join(Dirpath, 'testset.xlsx'))
    sheet = contentdata.sheets()[0]
    for row in range(sheet.nrows):
        datalist.append(sheet.cell_value(row, 0))
    return datalist

def getanswers(datalist):
    print(len(datalist))
    resultlist = []
    url = 'http://172.28.1.53:8888/v1/calculation'
    for data in datalist:
        result = requests.get(url=url,params={'query':data},headers={"Content-Type": "application/x-www-form-urlencoded"})
        if result.status_code == requests.codes.ok:
            if 'answer' in result.text and 'matched_prototype_question' in result.text:
                objdata = demjson.decode(result.text)
                print(objdata)
                resultlist.append([data,objdata['answer'],objdata['matched_prototype_question']])
            else:
                resultlist.append([data, '未返回answer字段','无对应类型'])
        else:
            resultlist.append([data, '请求错误', '请求错误'])
    workbook = xlsxwriter.Workbook(os.path.join(Dirpath, '知识图谱v0.3测试结果_0927_v3.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(resultlist)):
        for column in range(len(resultlist[row])):
            ws.write(row, column, resultlist[row][column])
    workbook.close()

if __name__ == '__main__':
    datalist = readExcel()
    getanswers(datalist)