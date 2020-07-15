# @File  : learningprocessvideores.py
# @Author: LiuXingsheng
# @Date  : 2020/6/4
# @Desc  : 名师视频学习进度测 （精度由最开始出版社、年级、单元、小节、课时、知识点，变为 出版社、年级、单元、小节、课时）

import csv
import os
import random
import xlsxwriter
import xlrd
import collections
from collections import Counter

COUNT = 10000
EXPECTED_SEED = 10
DirPath = r'C:\Users\Administrator\Desktop'


def getstardard():
    """
    读取标准数据
    :return:
    """
    standardlist = []
    chapterlist = []
    samechap_sec = []
    tidylist = []
    with open(os.path.join(DirPath, 'videodata.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        # 顺序分别为id,出版社,年级，章，节，课时
        for item in rows:
            standardlist.append((item[0], item[1], item[2], item[3], item[4], item[5]))
            chapterlist.append((item[3], item[4]))
    chapterlist = list(set(chapterlist))
    print(len(standardlist), len(chapterlist))
    for chapter in chapterlist[::-1]:
        for item in standardlist:
            if item[3] == chapter[0] and item[4] == chapter[1]:
                samechap_sec.append(item)
        tidylist.append(samechap_sec)
        samechap_sec = []
        chapterlist.remove(chapter)
    if len(tidylist) == len(chapterlist):
        print(True, len(tidylist))
    else:
        print('长度不同', len(tidylist), len(chapterlist))
    # with open('tidydata_new.csv', 'w', encoding='utf-8') as f:
    #     writer = csv.writer(f)
    #     for item in tidylist:
    #         writer.writerow(item)
    # return standardlist,list(set(chapterlist))
    # 测试代码
    # counter = Counter(chapterlist)
    # count_4 = 0
    # count_3 = 0
    # count_2 = 0
    # count_1 = 0
    # count = 0
    # for key, value in counter.items():
    #     if value > 40:
    #         count_4 += 1
    #     if value > 30 and value < 40:
    #         count_3 += 1
    #     if value > 20 and value < 30:
    #         count_2 += 1
    #     if value >10 and value < 20:
    #         count_1 += 1
    #     if value < 10:
    #         count += 1
    # print(count_4,count_3,count_2,count_1,count)


def generandommachineId():
    bigletterlist = []
    numlist = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    littleletterlist = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h',
                        'g', 'f', 'e', 'd', 'c', 'b', 'a']
    for letter in littleletterlist:
        bigletterlist.append(str.upper(letter))
    return "".join(random.sample(littleletterlist + bigletterlist + numlist, 13))


def generatedta():
    userrecord = []
    totalrecord = []
    knoledgelist = []
    with open(os.path.join(DirPath, 'tidydata_new.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    for i in range(COUNT):
        chosenchapter_sec = random.choice(rows)
        while len(chosenchapter_sec) < EXPECTED_SEED:
            chosenchapter_sec = random.choice(rows)
        seed = random.randint(EXPECTED_SEED - 9, EXPECTED_SEED)
        machine = generandommachineId()
        user = random.sample(chosenchapter_sec, seed)
        for i in user:
            i = i.replace('(', "").replace(')', '').replace('\'', '')
            recordlist = i.split(',')
            totalrecord.append((machine, i))
        userrecord.append((machine, recordlist[1], recordlist[2], recordlist[3], recordlist[4], recordlist[5]))

    # 调试打印代码
    # for user in userrecord:
    #     print(user, type(user))
    # print('-----------------')
    # for total in totalrecord:
    #     print(total, type(total))
    totalrecordlist = []
    titlelist = [('序列号', '视频Id', '出版社', '年级', '章', '节', '课时')]
    for total in totalrecord:
        sing = total[1].split(',')
        complsing = [total[0]] + sing
        totalrecordlist.append(complsing)
    contentlist = titlelist + totalrecordlist
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, str(EXPECTED_SEED) + '插入数据.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(contentlist)):
        for column in range(len(contentlist[row])):
            ws.write(row, column, contentlist[row][column])
    workbook.close()
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, str(EXPECTED_SEED) + '对比标准数据.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    stdtitlelist = [('序列号', '出版社', '年级', '章', '节', '课时')]
    standard = stdtitlelist + userrecord
    for row in range(len(standard)):
        for column in range(len(standard[row])):
            ws.write(row, column, str(standard[row][column]).strip())
    workbook.close()


def test():
    data = [1, 2, 3]
    for i in data[::-1]:
        data.remove(i)
    print(data)


def calcuaccuracy():
    stdwholist = []
    stdlist = []
    calwholist = []
    callist = []
    signresultrecord = []
    completelist = []
    successcount = [0, 0, 0, 0, 0,0]
    stddata = xlrd.open_workbook(os.path.join(DirPath, '10对比标准数据.xlsx'))
    stdsheet = stddata.sheets()[0]
    sheetrows = stdsheet.nrows
    sheetcolumns = stdsheet.ncols
    for row_std in range(1, sheetrows):
        for clo_std in range(sheetcolumns):
            stdlist.append(stdsheet.cell_value(row_std, clo_std))
        stdwholist.append(stdlist)
        stdlist = []
    caldata = xlrd.open_workbook(os.path.join(DirPath, 'result.xlsx'))
    calsheet = caldata.sheets()[0]
    calsheetrows = calsheet.nrows
    calsheetcolumns = calsheet.ncols
    for row_cal in range(1, calsheetrows):
        for clo_cal in range(calsheetcolumns):
            if calsheet.cell(row_cal, clo_cal).ctype == 2:
                callist.append(str(int(calsheet.cell_value(row_cal, clo_cal))))
            else:
                callist.append(calsheet.cell_value(row_cal, clo_cal))
        calwholist.append(callist)
        callist = []
    for std in stdwholist:
        flag = 0
        for cal in calwholist[::-1]:
            if str(std[0]) == str(cal[0]):
                flag = 1
                # 出版社
                if std[1] == cal[4]:
                    signresultrecord.append(1)
                else:
                    signresultrecord.append(0)
                # 年级
                if std[2] == cal[1]:
                    signresultrecord.append(1)
                else:
                    signresultrecord.append(0)
                # 章
                if std[3] == cal[5]:
                    signresultrecord.append(1)
                else:
                    signresultrecord.append(0)
                # 节
                if std[4] == cal[6]:
                    signresultrecord.append(1)
                else:
                    signresultrecord.append(0)
                # 课时
                if std[5] == cal[7]:
                    signresultrecord.append(1)
                else:
                    signresultrecord.append(0)
                if 0 in signresultrecord:
                    signresultrecord.append(0)
                else:
                    signresultrecord.append(1)
            else:
                pass
            if flag:
                completelist.append((std + [cal[4], cal[1], cal[5], cal[6], cal[7]] + signresultrecord))
                for i in range(len(signresultrecord)):
                    if signresultrecord[i] == 1:
                        successcount[i] += 1
                signresultrecord = []
                break
            else:
                pass
    print('出版社、年级、单元、小节、课时、进度准确率分别为：')
    print(successcount)
    for item in successcount:
        print(item/len(stdwholist))
    return completelist

def writecontent(completelist):
    titlelist = [('序列号', '标准出版社', '标准年级','标准单元', '标准节', '标准课时',
                  '大数据出版社', '大数据年级','大数据单元', '大数据节', '大数据课时',
                  '出版社准确率','年级准确率', '单元准确率', '节准确率', '知课时准确率','进度准确率')]
    alllist = titlelist + completelist
    workbook = xlsxwriter.Workbook(os.path.join(DirPath,'短视频学习进度准确率.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(alllist)):
        for column in range(len(alllist[row])):
            ws.write(row,column,alllist[row][column])
    workbook.close()

def test1():
    nums = [2,7,11,15]
    target = 9
    hashmap = {}
    for i, num in enumerate(nums):
        if hashmap.get(target - num) is not None:
            print(hashmap.get(target - num))
            return i, hashmap[target - num]
        hashmap[num] = i


def addTwoNumbers(l1,l2):
    dic1 = {}
    dic2 = {}
    len1 = len(l1)
    len2 = len(l2)
    resultdic = {}
    tempvalue = 0
    for i, num in enumerate(l1[::-1]):
        dic1[i] = num
    for i, num in enumerate(l2[::-1]):
        dic2[i] = num
    if len1 == len2:
        for i in range(len1):
            result = dic1[i] + dic2[i] + tempvalue
            gewei = result % 10
            shiwei = int(result / 10)
            resultdic[i] = gewei
            tempvalue = shiwei
            if i == len1 - 1 and shiwei != 0:
                resultdic[i + 1] = shiwei
    return resultdic
def test122():
    nums1 =[4,9,5]
    nums2 = [9,4,9,8,4]
    newnumlist = []
    nmap = {}
    for i, j in enumerate(nums1):
        nmap[j] = i
    print(nmap)
    for num in nums2:
        try:
            if nmap[num] is not None:
                newnumlist.append(num)
        except Exception:
            print(num)
            pass
    print(newnumlist)
    return list(set(newnumlist))
if __name__ == '__main__':
    # getstardard()
    # generatedta()
    # test()
    # completelist = calcuaccuracy()
    # writecontent(completelist)
    # print(test1())
    # numlist = [1,2,3]
    # for i,num in enumerate(numlist[::-1]):
    #     print(i,num)
    # print(addTwoNumbers([2,4,3],[5,6,4]))
    print(test122())
