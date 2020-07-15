# @File  : personalneed.py
# @Author: LiuXingsheng
# @Date  : 2020/3/7
# @Desc  :


import re

import chardet
import requests
import xlrd
import xlsxwriter
from bs4 import BeautifulSoup
import demjson


def judge404():
    urllist = []
    data = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\tb_gi_blackwhite_judge.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        urllist.append(
            (sheet.cell_value(row, 0), sheet.cell_value(row, 1), sheet.cell_value(row, 2), sheet.cell_value(row, 3)))
    i = 1
    workbook = xlsxwriter.Workbook('审核结果_0506.xlsx')
    ws = workbook.add_worksheet(u'sheet1')
    ws.write(0, 0, 'id')
    ws.write(0, 1, 'webName')
    ws.write(0, 2, 'weburl')
    ws.write(0, 3, 'domain')
    ws.write(0, 4, '是否正常访问')
    ws.write(0, 5, '状态码')
    for urlitem in urllist:
        print(i)
        ws.write(i, 0, urlitem[0])
        ws.write(i, 1, urlitem[1])
        ws.write(i, 2, urlitem[2])
        ws.write(i, 3, urlitem[3])
        try:
            if str(urlitem[2]).startswith('https') or str(urlitem[2]).startswith('http'):
                result = requests.post(url=urlitem[2], timeout=5)
                if result.status_code == 405:
                    result = requests.get(url=urlitem[2], timeout=5)
                ws.write(i, 5, result.status_code)
                if result.status_code == requests.status_codes.codes.ok:
                    ws.write(i, 4, 'True')
                else:
                    ws.write(i, 4, 'False')
            else:
                ws.write(i, 4, 'Fasle 未说明http或https协议')
        except Exception:
            ws.write(i, 4, 'False')
            ws.write(i, 5, '请求异常')
        i += 1
    workbook.close()


def getmaxcount():
    numList = [-1, -2, -3]
    sum = -100000000
    turnsum = 0
    for item in numList:
        turnsum = turnsum + item
        sum = max(sum, turnsum)
        if turnsum < 0:
            turnsum = 0
    print(sum)


def test():
    urllist = ['http://www.xuexifangfa.com/', 'http://his.hengqian.com/', 'http://www.lsfyw.net/',
               'http://pol.hengqian.com/']
    for item in urllist:
        result = requests.get(item)
        print(result.status_code)
        if result.status_code == 200 and 'title' in result.text:
            # chardet.detect(result.content) 为字典 示例返回数据 {'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}
            print(type(chardet.detect(result.content)), chardet.detect(result.content))
            print(result.apparent_epymysqlncoding)
            if 'GB' in chardet.detect(result.content)['encoding']:
                result.encoding = 'GBK'
            # print(result.content)
            # pick_charset(result.content)
            # print(result.encoding)
            soup = BeautifulSoup(markup=result.text, features='lxml')
            print(soup.title.text)
        else:
            print(item, result.status_code, '不能访问')


def pick_charset(html):
    """
    从文本中提取 meta charset
    :param html:
    :return:
    """
    charset = None
    m = re.compile('<meta .*(http-equiv="?Content-Type"?.*)?charset="?([a-zA-Z0-9_-]+)"?', re.I).search(html)
    if m and m.lastindex == 2:
        charset = m.group(2).lower()
    return charset


def test_timesplit():
    Type = 'in'
    url = 'http://s1.eebbk.net/v2/kernel/getOtaUpdateInfoAuto/S3_Pro/V1.5.0_191022/4?machineId=700H38400163D&state=1'
    for i in range(50):
        result = requests.get(url)
        if result.status_code == 200:
            objdata = demjson.decode(result.text)
            if 'data' in result.text:
                if Type == 'in':
                    if objdata['data']['recommendTime'] < 1800:
                        print('再次请求时间在30分钟离散时间之内: ', objdata['data']['recommendTime'])

                    else:
                        print('本次离散在30分钟范围之外: ', objdata['data']['recommendTime'])
                else:
                    if (objdata['data']['recommendTime'] - 2400) < 604800:
                        print('再次请求时间在7天离散时间之内: ',objdata['data']['recommendTime'])
                    else:
                        print('本次离散在7天范围之外: ', objdata['data']['recommendTime'])



if __name__ == '__main__':
    # judge404()
    # test()
    test_timesplit()
