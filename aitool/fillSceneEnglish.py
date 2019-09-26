# @File  : fillSceneEnglish.py
# @Author: LiuXingsheng
# @Date  : 2019/9/20
# @Desc  : 填充英文ocr类型

from aitool import EnglishBean
import xlrd, xlsxwriter, os

NOSCENE = 0
COMPLETE = 1

DIR_PATH = r'F:\AI搜相关结果\测试工具\第二季度英文'

def readExcelContent(fileName, beanType):
    contentbeanList = []
    data = xlrd.open_workbook(DIR_PATH + '\\' + fileName + '.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        if beanType == 0:
            picsence = EnglishBean.OcrEngBean(sheet.cell_value(row, 1), sheet.cell_value(row, 2),
                                              sheet.cell_value(row, 3), sheet.cell_value(row, 4),
                                              sheet.cell_value(row, 5), sheet.cell_value(row, 6),
                                              sheet.cell_value(row, 7), sheet.cell_value(row, 8),
                                              '')
            contentbeanList.append(picsence)
        else:
            piccom = EnglishBean.EngType(sheet.cell_value(row, 0), sheet.cell_value(row, 1))
            contentbeanList.append(piccom)
    return contentbeanList


def compareAndWrapper(noSceneList, SceneList):
    for noscene in noSceneList:
        for sceneItem in SceneList:
            if noscene.picName == sceneItem.picName:
                noscene.type = sceneItem.type
                break
            else:
                pass
    return noSceneList


def writeExcelContent(fileName, chosenList):
    try:
        column = 1
        workbook = xlsxwriter.Workbook(DIR_PATH + '\\' + fileName + '.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '图片编号')
        ws.write(0, 1, '标注文本')
        ws.write(0, 2, '自研结果')
        ws.write(0, 3, '有道结果')
        ws.write(0, 4, '汉王结果')
        ws.write(0, 5, '自研准确率')
        ws.write(0, 6, '有道准确率')
        ws.write(0, 7, '汉王准确率')
        ws.write(0, 8, '图片类型')
        for item in chosenList:
            ws.write(column, 0, item.picName)
            ws.write(column, 1, item.labelText)
            ws.write(column, 2, item.ZY)
            ws.write(column, 3, item.YD)
            ws.write(column, 4, item.HW)
            ws.write(column, 5, item.ZYresut)
            ws.write(column, 6, item.YDresult)
            ws.write(column, 7, item.HWresult)
            ws.write(column, 8, item.type)
            column += 1
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))


def main():
    fileName = '英文ocr_test'
    noSceneList = readExcelContent(fileName, NOSCENE)
    sceneList = readExcelContent('整合分类', COMPLETE)
    resultList = compareAndWrapper(noSceneList, sceneList)
    writeExcelContent(fileName + '_完成', resultList)

def getList():
    path = r'\\172.28.1.23\ai数据素材\AI测试素材库\已标注素材\图像\OCR\印刷体\英文印刷体\第二季度OCR英文素材_1'
    print(os.listdir(path))

if __name__ == '__main__':
    # main()
    getList()
