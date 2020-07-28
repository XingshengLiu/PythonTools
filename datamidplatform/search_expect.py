# @File  : search_expect.py
# @Author: LiuXingsheng
# @Date  : 2020/7/24
# @Desc  : 商店搜索预测
import csv
import os
import json
import collections
import xlsxwriter

DirPath = r'H:\大数据中台项目\标签测试报告\应用商店\搜索预估'
TypeCalcuPath = r'H:\大数据中台项目\标签测试报告\应用商店\搜索预估\type_v2'
APPCalcuPath = r'H:\大数据中台项目\标签测试报告\应用商店\搜索预估\app_v2'


def readData():
    """
    读取csv数据,因为会有重复的包名和类型名，所以使用了set
    :return:
    """
    keycount = collections.defaultdict(set)
    typecount = collections.defaultdict(set)
    with open(os.path.join(DirPath, '抽取测试数据.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for data in datalist[::-1]:
        if data[1] == 'NULL':
            datalist.remove(data)
    for data in datalist[1:]:
        key = data[1].strip().replace('。', '').replace('.', '')
        keycount[key].add(data[2])
        typecount[key].add(data[3])
    return keycount, typecount


def writeContent(keycount, typecount):
    """
    预测结果整理，该数据未使用，但方法未废弃
    :param keycount:
    :param typecount:
    :return:
    """
    # workbook = xlsxwriter.Workbook(os.path.join(DirPath, '搜索预测结果_test.xlsx'))
    # ws = workbook.add_worksheet(u'sheet1')
    # row = 0
    # for key in keycount:
    #     column = 0
    #     ws.write(row, column, key)
    #     lengthkey = len(keycount[key])
    #     for i in range(lengthkey):
    #         column += 1
    #         ws.write(row, column, keycount[key][i])
    #     typelength = len(typecount[key])
    #     for j in range(typelength):
    #         column += 1
    #         ws.write(row, column, typecount[key][j])
    #     row += 1
    # workbook.close()
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, '搜索预测结果_test_new.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    row = 0
    for key in keycount:
        ws.write(row, 0, key)
        ws.write(row, 1, str(keycount[key]))
        ws.write(row, 2, str(typecount[key]))
        row += 1
    workbook.close()


def readExpectData(path):
    datalist = []
    expectcount = collections.defaultdict(set)
    filelist = os.listdir(path)
    try:
        for file in filelist:
            with open(os.path.join(path, file), 'r', encoding='utf-8', errors='ignore') as f:
                for jsonstr in f.readlines():
                    if not jsonstr:
                        pass
                    else:
                        objdata = json.loads(jsonstr)
                        datalist.append(objdata)
                        if path == APPCalcuPath:
                            if objdata.get('package_name'):
                                expectcount[objdata['inputKey']].add(objdata['package_name'])
                            else:
                                pass
                        else:
                            if objdata.get('father_tag_name'):
                                expectcount[objdata['inputKey']].add(objdata['father_tag_name'])
                            else:
                                pass
    except KeyError:
        print('00000', objdata)
        print('----->', file)
    print(expectcount)
    print('所有json读取合并的原始列表长度是', len(datalist))
    return expectcount


def compare(keycount, expectcount,kind):
    """
    大数据的expectcount 不是全量数据，只有部分
    :param keycount:
    :param expectcount:
    :return:
    """
    bdlength = len(expectcount)
    print('大数据有结果返回数量',bdlength)
    accuracycount, recallsum = 0, 0
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, kind + '搜索预测测试整理_v2_test.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    row = 0
    for key in expectcount:
        ws.write(row, 0, key)
        ws.write(row, 1, str(keycount[key]))
        ws.write(row, 2, str(expectcount[key]))
        recallcount = 0
        if keycount[key] & expectcount[key]:
            accuracycount += 1
            ws.write(row, 3, '包含')
        else:
            ws.write(row, 3, '未包含')
            pass
        for item in list(keycount[key]):
            if item in expectcount[key]:
                recallcount += 1
        ws.write(row, 4, str(recallcount))
        if len(keycount[key]):
            recallsum += recallcount / len(keycount[key])
            ws.write(row, 5, str(recallcount / len(keycount[key])))
        else:
            recallsum += 0
            ws.write(row, 5, str(0))
        row += 1
    workbook.close()
    print(kind + '精确率 %.2f' % (accuracycount / bdlength))
    print(kind + '召回率 %.2f' % (recallsum / bdlength))



if __name__ == '__main__':
    keycount, typecount = readData()
    # writeContent(keycount, typecount)
    appexpectcount = readExpectData(APPCalcuPath)
    compare(keycount, appexpectcount,'APP')
    print('---------------')
    typeexpectcount = readExpectData(TypeCalcuPath)
    compare(typecount, typeexpectcount,'TYPE')
