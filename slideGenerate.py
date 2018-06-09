import xlrd, os, xlwt


class Relation:
    slide = ''
    wordName = ''


class RealMatch:
    slide = ''
    content = ''


def generateSlide():
    relationshipList = []
    realMatchList = []
    data = xlrd.open_workbook(os.getcwd() + '\\' + 'relation.xls')
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for i in range(1, rows):
        relationship = Relation()
        relationship.slide = sheet.cell_value(i, 0)
        relationship.wordName = sheet.cell_value(i, 1)
        relationshipList.append(relationship)
    try:
        for item in relationshipList:
            realmatch = RealMatch()
            realmatch.slide = item.slide
            fileName = item.wordName
            filedata = open(os.getcwd() + '\\wordlib' + '\\' + fileName + '.csv', encoding='utf-8')
            content = filedata.readline()
            if content.find(','):
                contentlist = content.split(',')
                realmatch.content = contentlist[0]
            else:
                realmatch.content = content
            realMatchList.append(realmatch)
            filedata.close()
    except IOError as ioerror:
        print("文件读错误:", str(ioerror))
    # for realitm in realMatchList:
    #     print(realitm.slide, realitm.content)
    return realMatchList


def writeContentToExcel():
    column = 0
    contentList = generateSlide()
    try:
        workbook = xlwt.Workbook(encoding='utf-8')
        ws = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
        for item in contentList:
            ws.write(0, column, item.slide)
            ws.write(1, column, item.content)
            column = column + 1
        workbook.save(os.getcwd() + '\\' + 'matching.xls')
    except IOError as ioerror:
        print("文件写错误:", str(ioerror))


def main():
    writeContentToExcel()


if __name__ == '__main__':
    main()
