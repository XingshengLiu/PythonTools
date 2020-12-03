# @File  : locationLabel.py
# @Author: LiuXingsheng
# @Date  : 2020/11/20
# @Desc  :
import xlsxwriter
import csv
import collections
import os
import re



DIR_PATH = r'H:\大数据中台项目\标签测试报告\地理位置标签_v2'

def getMachineLocation():
    machinedic = collections.defaultdict(list)
    with open(os.path.join(DIR_PATH, '样机列表 11月19日.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        machinelist = [row for row in reader]
    for machine in machinelist[1:10002]:
        machinedic[machine[0]].append(machine[1])
        machinedic[machine[0]].append(machine[7])
    workbook = xlsxwriter.Workbook(DIR_PATH + '\\' + '样机位置信息.xlsx')
    ws = workbook.add_worksheet(u'sheet1')
    row = 0
    for key in machinedic.keys():
        ws.write(row, 0, key)
        ws.write(row, 1, machinedic[key][0])
        ws.write(row, 2, machinedic[key][1])
        row += 1
    workbook.close()

def getTest():
    formual = r'([\u4e00-\u9fa5]{2,5}?((?<province>[^省]+省|.+自治区)|上海|北京|天津|重庆){0,1}([\u4e00-\u9fa5]{2,7}(?<city>[^市]+市|.+自治州){0,1}([\u4e00-\u9fa5]{2,7}(?<county>[^县]+县|.+区|.+镇|.+局){0,1}([\u4e00-\u9fa5]{2,7}?(?:村|镇|街道)){1}'
    pattern = re.compile(formual)
    strtest='山东省富民县富民县永定街新华书店步步高专柜'
    m = pattern.search(strtest)
    print(m)

if __name__ == '__main__':
    # getMachineLocation()
    getTest()