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

    def getOriginalSkill(self):
        return self.originalTask

    def setOrigianlSkill(self, task):
        self.originalTask = task


class ResultIntent:
    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def getResultIntent(self):
        return self.resultIntent

    def setResultIntent(self, resultIntent):
        self.resultIntent = resultIntent

    def setSkill(self, skill):
        self.skill = skill

    def getSkill(self):
        return self.skill

    def setTask(self, task):
        self.task = task

    def getTask(self):
        return self.task

    def setSlide(self, slide):
        self.slide = slide

    def getSlide(self):
        return self.slide


class MeanBean:
    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data

    def setOriginalSkill(self, task):
        self.originalTask = task

    def getOriginalSkill(self):
        return self.originalTask

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

    def setSkill(self, skill):
        self.skill = skill

    def getSkill(self):
        return self.skill

    def setTask(self, task):
        self.task = task

    def getTask(self):
        return self.task

    def setSlide(self, slide):
        self.slide = slide

    def getSlide(self):
        return self.slide


def generateResult():
    resultList = []
    originalList = []
    meanList = []
    resultdata = xlrd.open_workbook(os.getcwd() + '\\result.xls')
    resultsheet = resultdata.sheets()[0]
    rows = resultsheet.nrows
    for row in range(1, rows):
        resultIntent = ResultIntent()
        resultIntent.setData(resultsheet.cell_value(row, 1).strip())
        resultIntent.setSkill(resultsheet.cell_value(row, 2).strip())
        resultIntent.setTask(resultsheet.cell_value(row, 3).strip())
        resultIntent.setResultIntent(resultsheet.cell_value(row, 4).strip())
        resultIntent.setSlide(resultsheet.cell_value(row, 5).strip())
        resultList.append(resultIntent)
    originaldata = xlrd.open_workbook(os.getcwd() + '\\original.xls')
    originalsheet = originaldata.sheets()[0]
    orows = originalsheet.nrows
    for orow in range(1, orows):
        originalintent = OriginalIntent()
        originalintent.setData(originalsheet.cell_value(orow, 0).strip())
        originalintent.setOrigianlSkill(originalsheet.cell_value(orow, 1).strip())
        originalintent.setOriginalIntent(originalsheet.cell_value(orow, 2).strip())
        originalList.append(originalintent)
    for originalItem in originalList:
        flag = True
        for resultItem in resultList:
            if resultItem.getData() == originalItem.getData():
                meanBean = MeanBean()
                meanBean.setData(originalItem.getData())
                meanBean.setOriginalIntent(originalItem.getOrigianlIntent())
                meanBean.setOriginalSkill(originalItem.getOriginalSkill())
                meanBean.setResultIntent(resultItem.getResultIntent())
                meanBean.setSkill(resultItem.getSkill())
                meanBean.setTask(resultItem.getTask())
                meanBean.setSlide(resultItem.getSlide())
                if resultItem.getResultIntent() == originalItem.getOrigianlIntent() and resultItem.getSkill() == originalItem.getOriginalSkill():
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
            errorBean.setOriginalSkill(originalItem.getOriginalSkill())
            errorBean.setResultIntent("null")
            errorBean.setSkill('null')
            errorBean.setResult("null")
            errorBean.setSlide('null')
            errorBean.setTask('null')
            meanList.append(errorBean)

    try:
        i = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + 'resultundestanding.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, 'result')
        ws.write(0, 1, 'data')
        ws.write(0, 2, 'originalIntent')
        ws.write(0, 3, 'originalSkill')
        ws.write(0, 4, 'resultIntent')
        ws.write(0, 5, 'resultSkill')
        ws.write(0, 6, 'resultTask')
        ws.write(0, 7, 'resultSlide')
        for bean in meanList:
            ws.write(i, 0, bean.getResult())
            ws.write(i, 1, bean.getData())
            ws.write(i, 2, bean.getOrigianlIntent())
            ws.write(i, 3, bean.getOriginalSkill())
            ws.write(i, 4, bean.getResultIntent())
            ws.write(i, 5, bean.getSkill())
            ws.write(i, 6, bean.getTask())
            ws.write(i, 7, bean.getSlide())
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
