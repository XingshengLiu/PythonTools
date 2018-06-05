import os, xlrd, xlsxwriter


class OriginalIntent:
    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getOrigianlIntent(self):
        return self.origianlIntent

    def setOriginalIntent(self, intent):
        self.origianlIntent = intent


class ResultIntent:
    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getResultIntent(self):
        return self.resultIntent

    def setResultIntent(self, resultIntent):
        self.resultIntent = resultIntent


class MeanBean:
    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getOrigianlIntent(self):
        return self.origianlIntent

    def setOriginalIntent(self, intent):
        self.origianlIntent = intent

    def getResultIntent(self):
        return self.resultIntent

    def setResultIntent(self, resultIntent):
        self.resultIntent = resultIntent

    def getResult(self):
        return self.result

    def setResult(self, result):
        self.result = result


def generateResult():
    resultList = []
    originalList = []
    meanList = []
    resultdata = xlrd.open_workbook(os.getcwd() + '\\result.xls')
    resultsheet = resultdata.sheets()[0]
    rows = resultsheet.nrows
    for row in range(1, rows):
        resultIntent = ResultIntent()
        resultIntent.setData(resultsheet.cell_value(row, 0))
        resultIntent.setResultIntent(resultsheet.cell_value(row, 1))
        resultList.append(resultIntent)
    originaldata = xlrd.open_workbook(os.getcwd() + '\\original.xls')
    originalsheet = originaldata.sheets()[0]
    orows = originalsheet.nrows
    for orow in range(1, orows):
        originalintent = OriginalIntent()
        originalintent.setData(originalsheet.cell_value(orow, 0))
        originalintent.setOriginalIntent(originalsheet.cell_value(orow, 1))
        originalList.append(originalintent)
    for originalItem in originalList:
        flag = True
        for resultItem in resultList:
            if resultItem.getData() == originalItem.getData():
                meanBean = MeanBean()
                meanBean.setData(originalItem.getData())
                meanBean.setOriginalIntent(originalItem.getOrigianlIntent())
                meanBean.setResultIntent(resultItem.getResultIntent())
                if resultItem.getResultIntent() == originalItem.getOrigianlIntent():
                    meanBean.setResult('1')
                else:
                    meanBean.setResult('0')
                meanList.append(meanBean)
                flag = False
                break
            else:
                flag = True
                continue
        if flag:
            errorBean = MeanBean()
            errorBean.setData(originalItem.getData())
            errorBean.setOriginalIntent(originalItem.getOrigianlIntent())
            errorBean.setResultIntent("null")
            errorBean.setResult("null")
            meanList.append(errorBean)

    try:
        i = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + 'resultundestanding.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, 'data')
        ws.write(0, 1, 'origianlIntent')
        ws.write(0, 2, 'resultIntent')
        ws.write(0, 3, 'result')
        for bean in meanList:
            ws.write(i, 0, bean.getData())
            ws.write(i, 1, bean.getOrigianlIntent())
            ws.write(i, 2, bean.getResultIntent())
            ws.write(i, 3, bean.getResult())
            i = i + 1
        workbook.close()
    except IOError as ioerror:
        print("写入错误：" + str(ioerror))
    resultList.clear()
    originalList.clear()
    meanList.clear()


def main():
    generateResult()


if __name__ == '__main__':
    main()
