import os, xlrd, xlsxwriter, xlwt


class FileContent:

    def getAttrFileName(self):
        return self.filename

    def setAttrFileName(self, filename):
        self.filename = filename

    def getAttrContent(self):
        return self.content

    def setAttrContent(self, content):
        self.content = content


class FileRename:
    def getAttrOrigianlName(self):
        return self.originalName

    def setAttrOriginalName(self, originalName):
        self.originalName = originalName

    def getChangedName(self):
        return self.changedName

    def setChangedName(self, mchangedName):
        self.changedName = mchangedName


class FileTidyName:

    def getAttrNewlName(self):
        return self.newName

    def setAttrNewName(self, newName):
        self.newName = newName

    def getContent(self):
        return self.content

    def setContent(self, content):
        self.content = content


class MatchBean:
    originalName = ''
    tidyName = ''


def getAllPCMFiles():
    pcmFilelist = []
    fileList = os.listdir(os.getcwd())
    for file in fileList:
        if file.endswith('pcm'):
            pcmFilelist.append(file)
        else:
            continue
    return pcmFilelist


def readFileNameAndRename():
    matchBeanList = []
    try:
        batfile = open("rename.bat", "w")
        pcmfileList = getAllPCMFiles()
        i = 1
        for pcm in pcmfileList:
            matchBean = MatchBean()
            matchBean.originalName = pcm
            if i < 10:
                batfile.write(r'ren ' + pcm + ' ' + '00' + str(i) + '.pcm\n')
                matchBean.tidyName = '00' + str(i) + '.pcm'
            elif 10 <= i <= 99:
                batfile.write(r'ren ' + pcm + ' ' + '0' + str(i) + '.pcm\n')
                matchBean.tidyName = '0' + str(i) + '.pcm'
            else:
                batfile.write(r'ren ' + pcm + ' ' + str(i) + '.pcm\n')
                matchBean.tidyName = str(i) + '.pcm'
            matchBeanList.append(matchBean)
            i = i + 1
        batfile.close()
        row = 1
        workbook = xlwt.Workbook(encoding='utf-8')
        ws1 = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
        for bean in matchBeanList:
            ws1.write(row, 0, bean.originalName)
            ws1.write(row, 1, bean.tidyName)
            row = row + 1
        workbook.save('changed.xls')
    except IOError as ioerror:
        print('文件读写错误:' + str(ioerror))
    matchBeanList.clear()


def readExcelFileContent():
    fileContentList = []
    fileRenameList = []
    tidyList = []
    contentdata = xlrd.open_workbook(os.getcwd() + '\\content.xls')
    contenttest = contentdata.sheets()[0]
    rows = contenttest.nrows
    for row in range(1, rows):
        filecontent = FileContent()
        filecontent.setAttrContent(contenttest.cell_value(row, 0))
        filecontent.setAttrFileName(contenttest.cell_value(row, 1))
        fileContentList.append(filecontent)
    print("内容长度：", len(fileContentList))
    changedNamedata = xlrd.open_workbook(os.getcwd() + '\\changed.xls')
    changedtest = changedNamedata.sheets()[0]
    rows = changedtest.nrows
    for nrow in range(1, rows):
        filerename = FileRename()
        filerename.setAttrOriginalName(changedtest.cell_value(nrow, 0))
        filerename.setChangedName(changedtest.cell_value(nrow, 1))
        fileRenameList.append(filerename)
    print("name内容长度：", len(fileRenameList))
    for contentitem in fileContentList:
        for nameitem in fileRenameList:
            if contentitem.getAttrFileName() == nameitem.getAttrOrigianlName():
                filetidyname = FileTidyName()
                filetidyname.setAttrNewName(nameitem.getChangedName())
                filetidyname.setContent(contentitem.getAttrContent())
                tidyList.append(filetidyname)
                break
            else:
                continue
    print("tidyList的长度是：", len(tidyList))
    try:
        i = 1
        workbook = xlwt.Workbook(encoding='utf-8')
        ws = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
        ws.write(0, 0, 'content')
        ws.write(0, 1, 'filename')
        ws.write(0, 2, 'id')
        ws.write(0, 3, 'name')
        for resultitem in tidyList:
            ws.write(i, 0, resultitem.getContent())
            ws.write(i, 1, resultitem.getAttrNewlName())
            ws.write(i, 2, ' ')
            ws.write(i, 3, ' ')
            i = i + 1
        workbook.save('result.xls')
    except IOError as ioerror:
        print("写入错误：" + str(ioerror))
    fileContentList.clear()
    fileRenameList.clear()
    tidyList.clear()


def main():
    readFileNameAndRename()
    readExcelFileContent()


if __name__ == '__main__':
    main()
