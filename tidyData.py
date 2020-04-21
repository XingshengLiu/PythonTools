import xlwt, xlrd, os, json, xlsxwriter,random


class ExcelData:
    machineId = ''
    picInfo = ''
    picPath = ''
    clickInfo = ''
    version = ''


def getData():
    exceldataList = []
    list1 = []
    list2 = []
    list3 = []
    contentdata = xlrd.open_workbook(os.getcwd() + '\\data.xlsx')
    sheet = contentdata.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        data = ExcelData()
        data.machineId = sheet.cell_value(row, 0)
        tempdata = sheet.cell_value(row, 1)
        # print('原始字符串是：',tempdata)
        # json_str = json.dumps(str(tempdata))
        # print('jsonstr 字符串是：', json_str)
        objectdata = json.loads(tempdata)
        data.picInfo = objectdata['picInfo']
        data.picPath = objectdata['picPath']
        data.clickInfo = objectdata['clickInfo']
        data.version = objectdata['version']
        exceldataList.append(data)
    for item in exceldataList:
        if '2018/05/28' in item.picPath:
            list1.append(item)
        elif '2018/05/29' in item.picPath:
            list2.append(item)
        else:
            list3.append(item)
    try:
        i = 1
        workbook = xlwt.Workbook(encoding='utf-8')
        ws = workbook.add_sheet('Sheet1', cell_overwrite_ok=True)
        ws.write(0, 0, 'machineId')
        ws.write(0, 1, 'picInfo')
        ws.write(0, 2, 'picPath')
        ws.write(0, 3, 'clickInfo')
        ws.write(0, 4, 'version')
        for item_28 in list1:
            ws.write(i, 0, item_28.machineId)
            ws.write(i, 1, item_28.picInfo)
            ws.write(i, 2, item_28.picPath)
            ws.write(i, 3, item_28.clickInfo)
            ws.write(i, 4, item_28.version)
            i = i + 1
        for item_29 in list2:
            ws.write(i, 0, item_29.machineId)
            ws.write(i, 1, item_29.picInfo)
            ws.write(i, 2, item_29.picPath)
            ws.write(i, 3, item_29.clickInfo)
            ws.write(i, 4, item_29.version)
            i = i + 1
        for item_30 in list3:
            ws.write(i, 0, item_30.machineId)
            ws.write(i, 1, item_30.picInfo)
            ws.write(i, 2, item_30.picPath)
            ws.write(i, 3, item_30.clickInfo)
            ws.write(i, 4, item_30.version)
            i = i + 1
        workbook.save('tidysheet.xls')
    except IOError as ioerror:
        print("write error：" + str(ioerror))


def cleanData():
    savepath = r'G:\JmeterPressureScript\vtrainging'
    videolist = []
    contentdata = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\工作簿1.xlsx')
    sheet = contentdata.sheets()[0]
    for row in range(1, sheet.nrows):
        videolist.append(sheet.cell_value(row, 0).replace('\\\'', ''))
    for step in [10, 20, 30, 40]:
        listturn = [videolist[id:id + step] for id in range(0, len(videolist), step)]
        workbook = xlsxwriter.Workbook(os.path.join(savepath, '分割数据' + str(step) + '.xlsx'))
        ws = workbook.add_worksheet(u'sheet1')
        column = 1
        for item in listturn:
            for i in range(100):
                random.shuffle(item)
                ws.write(column, 0, str(item).replace('[','').replace(']','').replace('\'','').replace(' ','') + '@')
                column += 1
        workbook.close()

def test():
    listnum = [1,2,3,4,5,6,7,8,9,10]
    random.shuffle(listnum)
    print(listnum)

def main():
    # getData()
    cleanData()
    # test()


if __name__ == '__main__':
    main()
