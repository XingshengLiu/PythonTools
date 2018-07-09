import os, xlrd, xlwt


class FileContent:
    fileName = ''
    content = ''


class FileTidyName:
    newName = ''
    content = ''


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
    pcmfileList = getAllPCMFiles()
    i = 1
    for pcm in pcmfileList:
        matchBean = MatchBean()
        matchBean.originalName = pcm
        if i < 10:
            matchBean.tidyName = '00' + str(i) + '.pcm'
        elif 10 <= i <= 99:
            matchBean.tidyName = '0' + str(i) + '.pcm'
        else:
            matchBean.tidyName = str(i) + '.pcm'
        matchBeanList.append(matchBean)
        i = i + 1
    return matchBeanList


def readExcelFileContent():
    fileContentList = []
    fileRenameList = readFileNameAndRename()
    tidyList = []
    allfileList = os.listdir(os.getcwd())
    for name in allfileList:
        if name.endswith('xlsx'):
            excelName = name
            break
        else:
            continue
    contentdata = xlrd.open_workbook(os.getcwd() + '\\' + excelName)
    contenttest = contentdata.sheets()[0]
    rows = contenttest.nrows
    for row in range(1, rows):
        filecontent = FileContent()
        fileName = contenttest.cell_value(row, 4)
        start = fileName.find('F:')
        virtualName = fileName[start:]
        realName = virtualName.replace(':', '_')
        filecontent.fileName = realName
        filecontent.content = contenttest.cell_value(row, 5)
        fileContentList.append(filecontent)
    print("内容长度：", len(fileContentList))
    print(fileContentList[0].fileName, fileContentList[0].content)

    for contentitem in fileContentList:
        for nameitem in fileRenameList:
            if contentitem.fileName == nameitem.originalName:
                filetidyname = FileTidyName()
                filetidyname.newName = nameitem.tidyName
                filetidyname.content = contentitem.content
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
        ws.write(0, 1, 'fileName')
        ws.write(0, 2, 'id')
        ws.write(0, 3, 'name')
        for resultitem in tidyList:
            ws.write(i, 0, resultitem.content)
            ws.write(i, 1, resultitem.newName)
            ws.write(i, 2, ' ')
            ws.write(i, 3, ' ')
            i = i + 1
        workbook.save('result.xls')
    except IOError as ioerror:
        print("写入错误：" + str(ioerror))
    for item in fileRenameList:
        os.rename(os.getcwd() + '\\' + item.originalName, os.getcwd() + '\\' + item.tidyName)
    fileContentList.clear()
    fileRenameList.clear()
    tidyList.clear()


def main():
    readFileNameAndRename()
    readExcelFileContent()
    # 删除临时生成的changed文件
    # os.remove(os.getcwd() + '\\changed.xls')


if __name__ == '__main__':
    main()
