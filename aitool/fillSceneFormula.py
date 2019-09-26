# @File  : fillSceneFormula.py
# @Author: LiuXingsheng
# @Date  : 2019/6/25
# @Desc  : 填充公式场景

from aitool import FornulaBean
import xlrd, xlsxwriter, os

NOSCENE = 0
COMPLETE = 1


def readExcelContent(fileName, beanType):
    contentbeanList = []
    data = xlrd.open_workbook(os.getcwd() + '\\' + fileName + '.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        if beanType == 0:
            picsence = FornulaBean.PicWithNoScene(sheet.cell_value(row, 0), sheet.cell_value(row, 1),
                                                  sheet.cell_value(row, 2), sheet.cell_value(row, 3), )
            contentbeanList.append(picsence)
        else:
            piccom = FornulaBean.PicWithScene(sheet.cell_value(row, 0), sheet.cell_value(row, 1),
                                              sheet.cell_value(row, 2))
            contentbeanList.append(piccom)
    return contentbeanList


def compareAndWrapper(noSceneList, SceneList):
    for noscene in noSceneList:
        for sceneItem in SceneList:
            if noscene.picname == sceneItem.picname:
                noscene.suject = sceneItem.suject
                noscene.scene = sceneItem.scene
                break
            else:
                pass
    return noSceneList


def writeExcelContent(fileName, chosenList):
    try:
        column = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + fileName + '.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '文件名')
        ws.write(0, 1, '标准Latex')
        ws.write(0, 2, '识别结果')
        ws.write(0, 3, '准确率')
        ws.write(0, 4, '科目')
        ws.write(0, 5, '类型')
        for item in chosenList:
            ws.write(column, 0, item.picname)
            ws.write(column, 1, item.trueText)
            ws.write(column, 2, item.recogText)
            ws.write(column, 3, item.result)
            ws.write(column, 4, item.suject)
            ws.write(column, 5, item.scene)
            column += 1
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))


def main():
    fileName = '1568968217_步步高自研'
    noSceneList = readExcelContent(fileName, NOSCENE)
    sceneList = readExcelContent('已填充', COMPLETE)
    resultList = compareAndWrapper(noSceneList, sceneList)
    writeExcelContent(fileName + '_完成', resultList)


if __name__ == '__main__':
    main()
