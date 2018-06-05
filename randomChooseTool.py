import xlrd,os,random,xlwt

result = set()
originalList = []
resultlist = []
excelfileList = []
path = os.getcwd()
filelist = os.listdir(path)

for file in filelist:
    if file.endswith('.xlsx'):
        excelfileList.append(file)
    else:
        continue
for file in excelfileList:
    print(path + '\\' + file)
    data = xlrd.open_workbook(path + '\\' + file)
    test = data.sheets()[0]
    rows = test.nrows
    if rows <= 10:
        for i in range(rows):
            originaldata = test.cell_value(i, 0)
            originalskillId = test.cell_value(i, 1)
            originalintentName = test.cell_value(i, 2)
            originalTemple = {'data': originaldata, 'skillId': originalskillId, 'intentName': originalintentName}
            originalList.append(originalTemple)
        row1 = 0
        workbook1 = xlwt.Workbook(encoding='utf-8')
        ws1 = workbook1.add_sheet('sheet1', cell_overwrite_ok=True)
        for origianlitem in originalList:
            ws1.write(row1, 0, origianlitem.get("data"))
            ws1.write(row1, 1, origianlitem.get("skillId"))
            ws1.write(row1, 2, origianlitem.get("intentName"))
            row1 = row1 + 1
        workbook1.save(file + '_randomresult.xls')
        originalList.clear()
    else:
        while len(result) < 10:
            temp = random.randint(1, rows - 1)
            result.add(temp)
        for item in result:
            data = test.cell_value(item, 0)
            skillId = test.cell_value(item, 1)
            intentName = test.cell_value(item, 2)
            temple = {'data': data, 'skillId': skillId, 'intentName': intentName}
            resultlist.append(temple)
        row = 1
        try:
            workbook = xlwt.Workbook(encoding='utf-8')
            ws = workbook.add_sheet('sheet1', cell_overwrite_ok=True)
            ws.write(0, 0, 'data')
            ws.write(0, 1, 'skillId')
            ws.write(0, 2, 'intentName')
            for i in resultlist:
                ws.write(row, 0, i.get("data"))
                ws.write(row, 1, i.get("skillId"))
                ws.write(row, 2, i.get("intentName"))
                row = row + 1
            workbook.save(file + '_randomresult.xls')
        except IOError as ioeror:
            print("写入错误：" + str(ioeror))
        result.clear()
        resultlist.clear()
