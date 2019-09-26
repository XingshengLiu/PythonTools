# @File  : nlpTest.py
# @Author: LiuXingsheng
# @Date  : 2019/8/28
# @Desc  :
import xlrd, xlsxwriter, requests, demjson


class NlpBean():
    sentence = ''
    original = ''
    search = ''
    result = ''

    def __init__(self, sentence, original):
        self.sentence = sentence
        self.original = original


def getExcelContent():
    beanList = []
    data = xlrd.open_workbook(r'E:\PyGitHub\PythonTools\aitool\ask.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        picBean = NlpBean(sheet.cell_value(row, 0), sheet.cell_value(row, 1))
        beanList.append(picBean)
    return beanList


def getTestInterface():
    beanlist = getExcelContent()
    for item in beanlist:
        url = 'https://test.eebbk.net/nlp-app/app/nlpDispense/getSemanticInfo'
        result = requests.get(url=url, params={'sentence': item.sentence})
        dataobject = demjson.decode(result.text)
        if dataobject['data'] is not None:
            print(demjson.decode(dataobject['data']['semantic'][0])['intentName'])


def getFormalInterface():
    url = 'https://ai-nlp.eebbk.net/nlp-app/app/nlpDispense/getSemanticInfo'
    beanlist = getExcelContent()
    for item in beanlist:
        result = requests.get(url=url, params={'sentence': item.sentence})
        dataobject = demjson.decode(result.text)
        if dataobject['data'] is not None:
            print(dataobject['data']['semantic'][''])

if __name__ == '__main__':
    getTestInterface()
    # getFormalInterface()