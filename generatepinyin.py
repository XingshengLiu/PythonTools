# @File  : generatepinyin.py
# @Author: LiuXingsheng
# @Date  : 2020/6/15
# @Desc  :


from xpinyin import Pinyin
import xlrd
import xlsxwriter
contentlist = []
workbook = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\hanzi.xlsx')
sheet = workbook.sheets()[0]
rows = sheet.nrows
for row in range(rows):
    hanzi = sheet.cell_value(row, 0)
    p = Pinyin()
    strpinyin = p.get_pinyin(hanzi,tone_marks='marks')
    contentlist.append((hanzi,strpinyin))
workbook = xlsxwriter.Workbook(r'C:\Users\Administrator\Desktop' + '\\拼音.xlsx')
ws = workbook.add_worksheet(u'Sheet1')
for i in range(len(contentlist)):
    ws.write(i, 0, contentlist[i][0])
    ws.write(i, 1, contentlist[i][1])
workbook.close()
