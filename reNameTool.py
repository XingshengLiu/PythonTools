import os, xlrd, xlsxwriter


class FileContent:

    def getattrfilname(self):
        return self.filename

    def setattrfilename(self, filename):
        self.filename = filename

    def getattrcontent(self):
        return self.content

    def setattrcontent(self, content):
        self.content = content


class FileRename:
    def getattrorigianlName(self):
        return self.originalName

    def setattroriginalName(self, originalName):
        self.originalName = originalName

    def getChangeName(self):
        return self.changedName

    def setChangedName(self, mchangedName):
        self.changedName = mchangedName


class FileTidyName:

    def getattrnewlName(self):
        return self.newName

    def setattrnewName(self, newName):
        self.newName = newName

    def getcontent(self):
        return self.content

    def setconten(self, content):
        self.content = content


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
    batfile = open("rename.bat", "w")
    pcmfileList = getAllPCMFiles()
    i = 1
    for pcm in pcmfileList:
        if i < 10:
            batfile.write(r'ren ' + pcm + '\t' + '00' + str(i) + '.pcm\n')
        elif 10 <= i <= 99:
            batfile.write(r'ren ' + pcm + '\t' + '0' + str(i) + '.pcm\n')
        else:
            batfile.write(r'ren ' + pcm + '\t' + str(i) + '.pcm\n')
        i = i + 1
    batfile.close()


def readExcelFileContent():
    fileContentList = []
    fileRenameList = []
    tidyList = []
    contentdata = xlrd.open_workbook(os.getcwd() + '\\content.xls')
    contenttest = contentdata.sheets()[0]
    rows = contenttest.nrows
    for row in range(1, rows):
        filecontent = FileContent()
        filecontent.setattrcontent(contenttest.cell_value(row, 0))
        filecontent.setattrfilename(contenttest.cell_value(row, 1))
        fileContentList.append(filecontent)
    print("内容长度：", len(fileContentList))
    changedNamedata = xlrd.open_workbook(os.getcwd() + '\\changed.xls')
    changedtest = changedNamedata.sheets()[0]
    rows = changedtest.nrows
    for nrow in range(1, rows):
        filerename = FileRename()
        filerename.setattroriginalName(changedtest.cell_value(nrow, 0))
        filerename.setChangedName(changedtest.cell_value(nrow, 1))
        fileRenameList.append(filerename)
    print("name内容长度：",len(fileRenameList))
    for contentitem in fileContentList:
        for nameitem in fileRenameList:
            if contentitem.getattrfilname() == nameitem.getattrorigianlName():
                filetidyname = FileTidyName()
                filetidyname.setattrnewName(nameitem.getChangeName())
                filetidyname.setconten(contentitem.getattrcontent())
                tidyList.append(filetidyname)
                break
            else:
                continue
    print("tidyList的长度是：",len(tidyList))
    try:
        i = 1
        workbook = xlsxwriter.Workbook(os.getcwd() + '\\' + 'result.xlsx')
        ws = workbook.add_worksheet(u'sheet1')
        ws.write(0, 0, 'content')
        ws.write(0, 1, 'filename')
        for resultitem in tidyList:
            ws.write(i, 0, resultitem.getcontent())
            ws.write(i, 1, resultitem.getattrnewlName())
            i = i + 1
        workbook.close()
    except IOError as ioerror:
        print("写入错误：" + str(ioerror))
    fileContentList.clear()
    fileRenameList.clear()
    tidyList.clear()


def main():
    # readFileNameAndRename()
    readExcelFileContent()
    print("test是否能够上传")


if __name__ == '__main__':
    main()
