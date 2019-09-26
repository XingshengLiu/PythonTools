# @File  : fillScene.py
# @Author: LiuXingsheng
# @Date  : 2019/5/5
# @Desc  : 充单条结果的图片场景
import xlrd, os, xlsxwriter

NOSCENE = 0
COMPLETE = 1


class PicWithNoScene(object):
    picname = ''
    result = ''
    questionId = ''
    successId = ''
    subject = ''
    type = ''

    def __init__(self, name, result, questionId, successId, subject):
        self.picname = name
        self.result = result
        self.questionId = questionId
        self.successId = successId
        self.subject = subject


class PicComplete(object):
    picname = ''
    type = ''

    def __init__(self, picname, type):
        self.picname = picname
        self.type = type


def readExcelContent(fileName, beanType):
    contentbeanList = []
    data = xlrd.open_workbook(os.getcwd() + '\\' + fileName + '.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        if beanType == 0:
            picsence = PicWithNoScene(sheet.cell_value(row, 0), sheet.cell_value(row, 1),
                                      sheet.cell_value(row, 2), sheet.cell_value(row, 3),
                                      sheet.cell_value(row, 4))
            contentbeanList.append(picsence)
        else:
            piccom = PicComplete(sheet.cell_value(row, 0), sheet.cell_value(row, 5))
            contentbeanList.append(piccom)
    return contentbeanList


def writeExcelContent(fileName, chosenList):
    try:
        column = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + fileName + '.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '文件名')
        ws.write(0, 1, '搜索结果')
        ws.write(0, 2, 'questionCred')
        ws.write(0, 3, 'successId')
        ws.write(0, 4, '科目')
        ws.write(0, 5, '类型')
        for item in chosenList:
            ws.write(column, 0, item.picname)
            ws.write(column, 1, item.result)
            ws.write(column, 2, item.questionId)
            ws.write(column, 3, item.successId)
            ws.write(column, 4, item.subject)
            ws.write(column, 5, item.type)
            column += 1
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))


def compareAndWrapper(noSceneList, completeList):
    for noscene in noSceneList:
        for complete in completeList:
            if noscene.picname == complete.picname:
                noscene.type = complete.type
                break
            else:
                pass
    return noSceneList


def test():
    """
    break只打破内层循环
    :return:
    """
    for i in range(5):
        for j in range(6):
            print('j的值是：', j)
            if i == 3:
                break
        print('i的值是：', i)


def test1():
    """

    :return:
    """
    for i in range(1, 2):
        print(i)


def main():
    noSceneList = readExcelContent('未填充', NOSCENE)
    completeList = readExcelContent('已填充', COMPLETE)
    for item in completeList:
        print(item)
    print('tes')
    newList = compareAndWrapper(noSceneList, completeList)
    writeExcelContent('完成', newList)


if __name__ == '__main__':
    main()
