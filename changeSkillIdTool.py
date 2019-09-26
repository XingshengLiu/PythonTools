import xlrd
import os
import xlwt


def chooseFilesAndCopyToAnotherDir():
    xlsFilelist = []
    filelist = os.listdir(os.getcwd())
    for file in filelist:
        if file.endswith('.xls'):
            xlsFilelist.append(file)
        else:
            continue
    return xlsFilelist


def changeId():
    originalList = []
    num = input('选择技能：\n 1,变字 2,查字 3,古诗冲突 4,词语 5,古诗二版 6,句子 7,控制命令 8,拼音 9,生字 10,同类型词语 11,同类型的字 12,闲聊 13,组词 14,作文 15,特殊句式 16,翻译web版 17,英文 18,英文字母 19, 闲聊2\n')
    if num == '1':
        id = '2018042000000028'
    elif num == '2':
        id = '2018041800000036'
    elif num == '3':
        id = '2018050700000056'
    elif num == '4':
        id = '2018030700000034'
    elif num == '5':
        id = '2018062300000004'
    elif num == '6':
        id = '2018030800000047'
    elif num == '7':
        id = '2018010800000016'
    elif num == '8':
        id = '2018030800000016'
    elif num == '9':
        id = '2018061500000003'
    elif num == '10':
        id = '2018041600000008'
    elif num == '11':
        id = '2018041600000007'
    elif num == '12':
        id = '2018032000000039'
    elif num == '13':
        id = '2018042000000026'
    elif num == '14':
        id = '2018030800000046'
    elif num == '15':
        id = '2018052200000070'
    elif num == '16':
        id = '2018030800000010'
    elif num == '17':
        id = '2018082500000008'
    elif num == '18':
        id = '2018082700000001'
    else:
        id = '2018032000000039'
    path = os.getcwd()
    excelList = chooseFilesAndCopyToAnotherDir()
    for file in excelList:
        data = xlrd.open_workbook(path + '\\' + file)
        test = data.sheets()[0]
        rows = test.nrows
        for i in range(1, rows):
            originaldata = test.cell_value(i, 0)
            originalskillId = test.cell_value(i, 1)
            originalintentName = test.cell_value(i, 2)
            originalTemple = {'data': originaldata, 'skillId': originalskillId, 'intentName': originalintentName}
            originalList.append(originalTemple)
        workbook1 = xlwt.Workbook(encoding='utf-8')
        ws1 = workbook1.add_sheet('sheet1', cell_overwrite_ok=True)
        row = 0
        ws1.write(row, 0, "data")
        ws1.write(row, 1, "skillId")
        ws1.write(row, 2, "intentName")
        row = 1
        for origianlItem in originalList:
            ws1.write(row, 0, origianlItem.get("data"))
            ws1.write(row, 1, id)
            ws1.write(row, 2, origianlItem.get("intentName"))
            row = row + 1
        workbook1.save(file)
        originalList.clear()


def main():
    changeId()


if __name__ == '__main__':
    main()
