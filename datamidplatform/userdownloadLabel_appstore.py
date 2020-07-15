# @File  : userdownloadLabel_appstore.py
# @Author: LiuXingsheng
# @Date  : 2020/7/9
# @Desc  : 应用商店-用户下载类型偏好

import os
import csv
import collections
from collections import Counter
import xlsxwriter


DirPath = r'H:\大数据中台项目\标签测试报告\应用商店\下载类偏好'


def test():
    userdatalist = collections.defaultdict(list)
    typedic = collections.defaultdict(list)
    sumcount = collections.defaultdict(list)
    testcount = collections.defaultdict(dict)
    with open(os.path.join(DirPath, '下载偏好测试用例.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for row in datalist[1:]:
        if 'null' in row:
            pass
        else:
            sumcount[row[0]].append((row[2]))
    # print('+++++++++++++++++++++',sumcount)
    # for key in sumcount.keys():
    #     for key1 in sumcount[key]:
    #         testcount[key][key1[0]] = key1[1]
    #     result = Counter(sumcount[key])
    #     d = sorted(result.items(),key=lambda x:x[1],reverse=True)
    #     for item in d:
    #         typedic[key].append(item[0])
    # print(type(typedic),len(typedic))

    # namelist = {'test':'1','yu':'2','yqu':'2'}
    # result = Counter(namelist)
    # d = sorted(result.items(),key=lambda x:x[1],reverse=True)
    # print(d)

    # for row in rows[1:]:
    #     sumcount[row[0]].append((row[2]))
    # print('+++++++++++++++++++++',sumcount)
    for key in sumcount.keys():
        result = Counter(sumcount[key])
        d = sorted(result.items(),key=lambda x:x[1],reverse=True)
        userdatalist[key] = d
    # for key in userdatalist.keys():
    #     print(key, userdatalist[key])
    return userdatalist

    # workbook = xlsxwriter.Workbook(os.path.join(DirPath, '测试数据整理结果.xlsx'))
    # ws = workbook.add_worksheet(u'sheet1')
    # for row in range(len(typelist)):
    #     for column in range(len(typelist[row][1]) + 1):
    #         if column == 0:
    #             ws.write(row, column, str(typelist[row][0]))
    #         else:
    #             for inneritem in range(len(typelist[row][1])):
    #                 ws.write(row, inneritem + 1, str(typelist[row][1][inneritem]))
    # workbook.close()

    # workbook = xlsxwriter.Workbook(os.path.join(DirPath, '下载偏好大数据值.xlsx'))
    # ws = workbook.add_worksheet(u'sheet1')
    # for row in range(len(datalist)):
    #     for column in range(len(datalist[row])):
    #         ws.write(row, column, datalist[row][column])
    # workbook.close()



def radcalcudat():
    bigdataresult = collections.defaultdict(list)
    with open(os.path.join(DirPath, '类型下载偏好值.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for row in datalist[1:]:
        bigdataresult[row[0]].append((row[1]))
    # for key in bigdataresult.keys():
    #     print(key,bigdataresult[key])
    return bigdataresult

def compareResult(userdatalist,bigdataresult):
    comparelist = []
    for key in userdatalist.keys():
        flaglist = []
        comparelist.append((key,userdatalist[key]))
        comparelist.append((key,bigdataresult[key]))
        for i in range(len(userdatalist[key])):
            if str(bigdataresult[key][i]) in str(userdatalist[key][i]):
                flaglist.append(1)
            else:
                flaglist.append(0)
        comparelist.append(('', flaglist))
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '测试结果_0719_v1.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(comparelist)):
        for column in range(len(comparelist[row][1]) + 1):
            if row % 3 == 0:
                ws.write(row, 0, '用户实际数据')
            elif row % 3 == 1:
                ws.write(row, 0, '大数据预测偏好')
            else:
                ws.write(row, 0, '是否正确')
            if column == 1:
                ws.write(row, column, str(comparelist[row][0]))
            else:
                for inneritem in range(len(comparelist[row][1])):
                    ws.write(row, inneritem + 2, str(comparelist[row][1][inneritem]))
    workbook.close()



if __name__ == '__main__':
    userdatalist = test()
    bigdataresult = radcalcudat()
    compareResult(userdatalist,bigdataresult)