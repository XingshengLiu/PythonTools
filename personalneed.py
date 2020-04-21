# @File  : personalneed.py
# @Author: LiuXingsheng
# @Date  : 2020/3/7
# @Desc  :


import xlrd
import xlsxwriter
import requests


def judge404():
    urllist = []
    data = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\浏览器预制白名单.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        urllist.append(
            (sheet.cell_value(row, 0), sheet.cell_value(row, 1), sheet.cell_value(row, 2), sheet.cell_value(row, 3)))
    i = 1
    workbook = xlsxwriter.Workbook('审核结果_0321.xlsx')
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


if __name__ == '__main__':
    judge404()
