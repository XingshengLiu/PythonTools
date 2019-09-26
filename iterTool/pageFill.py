# @File  : pageFill.py
# @Author: LiuXingsheng
# @Date  : 2019/5/6
# @Desc  :
import os, xlsxwriter, demjson, math


class PageBean(object):
    picname = ''
    pageno = ''
    originalfingercoX = ''
    originalfingercoY = ''
    expectfingercoX = ''
    expectfingercoY = ''
    correctnum = ''
    returncoX = ''
    returncoY = ''
    returnnum = ''
    distance = ''


class FailBean(object):
    allmes = ''
    jsonstr = ''


def getAllTxtfile():
    txtfileList = []
    fileList = os.listdir(os.getcwd())
    for file in fileList:
        if file.endswith('.txt') and (file.startswith('json')) is not True:
            txtfileList.append(file)
        else:
            pass
    return txtfileList


def wrapperExpectedbean(txtfileList):
    pageList = []
    for file in txtfileList:
        nameList = file.split('#')
        page = PageBean()
        page.picname = file.replace('.txt', '.jpg')
        page.pageno = nameList[1]
        with open(file, 'rb')as f:
            data = f.read()
        originalCorList = str(data, encoding='utf-8').split(',')
        page.originalfingercoX = str(originalCorList[0])
        page.originalfingercoY = str(originalCorList[1])
        page.expectfingercoX = str(originalCorList[2])
        page.expectfingercoY = str(originalCorList[3])
        page.correctnum = str(originalCorList[4])
        pageList.append(page)
    return pageList


def readjsonfile():
    objectList = []
    with open('json.txt', encoding='utf-8')as f:
        data = f.read()
    datastr = data.split('File: ')
    for item in datastr:
        failbean = FailBean()
        if 'test' in item:
            failbean.allmes = item
            # print(item[item.index('{'):len(item)])
            failbean.jsonstr = item[item.index('{'):len(item)]
            objectList.append(failbean)
        else:
            pass
    return objectList


def compareAndwrapper(pageList, objectList):
    for page in pageList:
        for obj in objectList:
            if page.picname in obj.allmes:
                result = demjson.decode(obj.jsonstr)
                print(result['data'])
                if result['data'] is None:
                    page.returncoX = 'NULL'
                    page.returncoY = 'NULL'
                    page.returnnum = 'NULL'
                    page.distance = 'NULL'
                else:
                    page.returnnum = result['data']['outlineMainOrder']
                    page.returncoX = str(result['data']['pictureSearchResultVo']['dx'])
                    page.returncoY = str(result['data']['pictureSearchResultVo']['dy'])
                    page.distance = calculateDistance(page.expectfingercoX, page.expectfingercoY,
                                                      page.returncoX, page.returncoY)
                break
            else:
                pass
    return pageList


def calculateDistance(ox, oy, nx, ny):
    return math.sqrt(math.pow(int(ox) - int(nx), 2) + math.pow(int(oy) - int(ny), 2))


def writeExcelContent(fileName, chosenList):
    try:
        column = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + fileName + '.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '文件名')
        ws.write(0, 1, '页码')
        ws.write(0, 2, '原图手指坐标X')
        ws.write(0, 3, '原图手指坐标Y')
        ws.write(0, 4, '期待坐标X')
        ws.write(0, 5, '期待坐标Y')
        ws.write(0, 6, '正确勾勒号')
        ws.write(0, 7, '返回坐标X')
        ws.write(0, 8, '返回坐标Y')
        ws.write(0, 9, '返回勾勒号')
        ws.write(0, 10, '距离')
        for item in chosenList:
            ws.write(column, 0, item.picname)
            ws.write(column, 1, item.pageno)
            ws.write(column, 2, item.originalfingercoX)
            ws.write(column, 3, item.originalfingercoY)
            ws.write(column, 4, item.expectfingercoX)
            ws.write(column, 5, item.expectfingercoY)
            ws.write(column, 6, item.correctnum)
            ws.write(column, 7, item.returncoX)
            ws.write(column, 8, item.returncoY)
            ws.write(column, 9, item.returnnum)
            ws.write(column, 10, item.distance)
            column += 1
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))


def main():
    txtfileList = getAllTxtfile()
    pageList = wrapperExpectedbean(txtfileList)
    objectList = readjsonfile()
    resutlList = compareAndwrapper(pageList, objectList)
    writeExcelContent('整理后结果', resutlList)


if __name__ == '__main__':
    main()
