import os, xlrd, xlsxwriter


class SheetObject:
    id = ''
    machineId = ''
    model = ''
    appVersion = ''
    audio = ''
    text = ''
    errorType = ''
    fixedText = ''
    jumpStruc = ''
    condition = ''
    originalIntent = ''
    realIntent = ''
    support = ''


def getChosenMachineId():
    machineList = []
    data = xlrd.open_workbook(os.getcwd() + '\\machine.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        machineList.append(sheet.cell_value(row, 0))
    return machineList


def getAllContent():
    contetnList = []
    machineList = getChosenMachineId()
    data = xlrd.open_workbook(os.getcwd() + '\\data.xlsx')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        sheetObject = wrappObject(row, sheet)
        for tempId in machineList:
            if sheetObject.machineId == tempId:
                contetnList.append(sheetObject)
            else:
                continue
    return contetnList


def wrappObject(row, sheet):
    data = SheetObject()
    data.id = sheet.cell_value(row, 0)
    data.machineId = sheet.cell_value(row, 1)
    data.model = sheet.cell_value(row, 2)
    data.appVersion = sheet.cell_value(row, 3)
    data.audio = sheet.cell_value(row, 4)
    data.text = sheet.cell_value(row, 5)
    data.errorType = sheet.cell_value(row, 6)
    data.fixedText = sheet.cell_value(row, 7)
    data.jumpStruc = sheet.cell_value(row, 8)
    data.condition = sheet.cell_value(row, 9)
    data.originalIntent = sheet.cell_value(row, 10)
    data.realIntent = sheet.cell_value(row, 11)
    data.support = sheet.cell_value(row, 12)
    return data


def writeResult(contentList):
    try:
        i = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + 'chosenMachine.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, '语料id')
        ws.write(0, 1, '机器序列号')
        ws.write(0, 2, '机型')
        ws.write(0, 3, 'app版本')
        ws.write(0, 4, '语音')
        ws.write(0, 5, '识别文本')
        ws.write(0, 6, '识别错误类型')
        ws.write(0, 7, '修改后文本')
        ws.write(0, 8, '跳转结构')
        ws.write(0, 9, '语音识别情况')
        ws.write(0, 10, '原命中意图')
        ws.write(0, 11, '实际意图')
        ws.write(0, 12, '有无内容支撑')
        for bean in contentList:
            ws.write(i, 0, bean.id)
            ws.write(i, 1, bean.machineId)
            ws.write(i, 2, bean.model)
            ws.write(i, 3, bean.appVersion)
            ws.write(i, 4, bean.audio)
            ws.write(i, 5, bean.text)
            ws.write(i, 6, bean.errorType)
            ws.write(i, 7, bean.fixedText)
            ws.write(i, 8, bean.jumpStruc)
            ws.write(i, 9, bean.condition)
            ws.write(i, 10, bean.originalIntent)
            ws.write(i, 11, bean.realIntent)
            ws.write(i, 12, bean.support)
            i = i + 1
        workbook.close()
    except IOError as ioerror:
        print("写入错误：" + str(ioerror))


def main():
    tempList = getAllContent()
    writeResult(tempList)


if __name__ == '__main__':
    main()
