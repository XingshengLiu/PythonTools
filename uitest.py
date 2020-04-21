# @File  : uitest.py
# @Author: LiuXingsheng
# @Date  : 2019/1/16
# @Desc  :

import requests, demjson
import xlrd, xlsxwriter

desired_caps = {}
DIR_PATH = r'G:\JmeterPressureScript\5.0OCR'


# desired_caps['platformName'] = 'Android'
# desired_caps['platformVersion'] = '4.4.4'
# desired_caps['deviceName'] = 'MI 3C'
# desired_caps['appPackage'] = 'com.eebbk.theonetest'
# desired_caps['appActivity'] = '.MainActivity'
#
# driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
# test = [2, 3, 1]
#
#
# def findnumber(arr, k):
#     print(arr[0])
#     if k in arr:
#         return 'YES'
#     else:
#         return 'NO'
#
#
# def sort(arr):
#     for i in range(len(arr)):
#         print('i={0}'.format(i))
#         for j in range(i, len(arr)):
#             print('j={0}'.format(j))
#             if arr[i] > arr[j]:
#                 arr[i],arr[j] = arr[j],arr[i]
#         print(arr)
#     return arr
#
#
# if __name__ == '__main__':
#     value = findnumber(test, 2)
#     print(value)
#     print(sort(test))


def findNumber(arr, k):
    if str(k) in str(arr):
        return 'YES'
    else:
        return 'NO'


def oddNumbers(l, r):
    arr = []
    for i in range(l, r):
        print(i)
        if (i % 2) != 0:
            arr.append(i)
    return arr


def splitest():
    isFind = False
    find = 0
    ids = '12792962'
    signList = ids.split('#')
    piName = 'STANDARD20190513070229CLICK_0_1030_1091_3120_4160_523_554.JPEG'
    picnameList = piName.split('.')
    ordinateList = picnameList[0].split('_')
    print('x ordinate is : {0}, y ordinate is : {1}'.format(ordinateList[-2], ordinateList[-1]))
    file = {'file': open(piName, 'rb')}
    result = requests.request(method='POST', url='http://172.28.1.229:7027/ai-search/api/search', files=file,
                              params={'x': str(ordinateList[-2]), 'y': str(ordinateList[-1]), 'zipType': 'ai'})
    print(result.text)
    dataObject = demjson.decode(result.text)
    if dataObject['data'] is not None:
        print(dataObject['data']['questionListId'])
        for item in signList:
            for itemnew in dataObject['data']['questionListId']:
                print('itemnew :{0} item :{1}'.format(itemnew, item))
                find += 1
                if itemnew == item:
                    print('第几个找到的：', find)
                    isFind = True
                    break
            find = 0
            if isFind:
                break
            else:
                pass


def looptest():
    for i in range(5):
        for j in range(3):
            print('i is：{0}, j is {1}'.format(i, j))
            if j == 1:
                break


def splitordinate():
    data = xlrd.open_workbook(DIR_PATH + '\\' + '图片名.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        picname = sheet.cell_value(row, 0)
        ordinatelist = picname.split('#')[3].split('_')
        print(picname, ordinatelist[0], ordinatelist[1])


def splitocrv4ordinate():
    piclist = []
    suffix = r'/usr/jmeter/5.0ocr/picresources/'
    data = xlrd.open_workbook(DIR_PATH + '\\' + '图片名.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        picname = sheet.cell_value(row, 0)
        print(picname)
        abspicname = suffix + picname + '@'
        ordinate = picname.split('_')
        piclist.append((abspicname + ordinate[2] + '@' + ordinate[3] + '@' + picname))
    i = 1
    workbook = xlsxwriter.Workbook(DIR_PATH + '\\' + '5.0处理文件名.xlsx')
    ws = workbook.add_worksheet(u'sheet1')
    for item in piclist:
        ws.write(i, 0, item)
        i = i + 1
    workbook.close()


def testdir():
    import os
    path = r'D:\apktool'
    listfile = os.listdir(path)
    print(listfile)


if __name__ == '__main__':
    # print(oddNumbers(1,10))
    # fptr = open('test.txt', 'w')
    #
    # arr_count = int(input().strip())
    # print(arr_count)
    #
    # arr = []
    #
    # for _ in range(arr_count):
    #     arr_item = int(input().strip())
    #     arr.append(arr_item)
    #
    #
    # k = int(input().strip())
    #
    # res = findNumber(arr, k)
    #
    # fptr.write(res + '\n')
    #
    # fptr.close()
    # splitest()
    # looptest()
    # splitordinate()
    # testdir()
    splitocrv4ordinate()
