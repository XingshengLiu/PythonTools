import os, xlrd, shutil, xlwt


class VoiceFileBean:
    content = ''
    filename = ''
    skillid = ''
    name = ''


def getAllPcmFiles():
    pcmFilelist = []
    filelist = os.listdir(os.getcwd())
    for file in filelist:
        if file.endswith('.pcm'):
            pcmFilelist.append(file)
        else:
            continue
    return pcmFilelist


def readExcelFile():
    wavfileNameList = []
    filelist = os.listdir(os.getcwd())
    for file in filelist:
        if file.endswith('.xls'):
            temp = file
            break
        else:
            continue
    data = xlrd.open_workbook(os.getcwd() + '\\' + temp)
    test = data.sheets()[0]
    rows = test.nrows
    for row in range(1, rows):
        wavFileName = test.cell_value(row, 1)
        wavfileNameList.append(wavFileName)
    for wavfile in wavfileNameList:
        shutil.move(os.getcwd() + '\\' + wavfile , os.getcwd() + '\\' + "test")


def readPCMFile():
    chosenlist = []
    pcmlist = getAllPcmFiles()
    data = xlrd.open_workbook(os.getcwd() + '\\' + 'original.xls')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for pcm in pcmlist:
        for row in range(1, rows):
            if sheet.cell_value(row, 1) == pcm:
                voiceBean = VoiceFileBean()
                voiceBean.content = sheet.cell_value(row, 0)
                voiceBean.filename = sheet.cell_value(row, 1)
                voiceBean.skillid = ' '
                voiceBean.name = ' '
                chosenlist.append(voiceBean)
                break
            else:
                continue
    return chosenlist


def writeChosenResult():
    column = 1
    chosenlist = readPCMFile()
    try:
        workbook = xlwt.Workbook(encoding='utf-8')
        ws = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        ws.write(0, 0, '语音内容')
        ws.write(0, 1, '文件名')
        ws.write(0, 2, 'id')
        ws.write(0, 3, 'name')
        for item in chosenlist:
            ws.write(column, 0, item.content)
            ws.write(column, 1, item.filename)
            ws.write(column, 2, item.skillid)
            ws.write(column, 3, item.name)
            column = column + 1
        workbook.save(os.getcwd() + '\\' + 'chosen.xls')
    except IOError as ioerror:
        print("文件写错误:", str(ioerror))


def main():
    flag = input("excel筛选音频文件选1，音频文件填写excel选2 \n")
    if flag == '1':
        readExcelFile()
    else:
        writeChosenResult()


if __name__ == '__main__':
    main()
