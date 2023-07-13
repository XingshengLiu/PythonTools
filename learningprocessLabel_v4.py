# @File  : learningprocessLabel_v4.py
# @Author: LiuXingsheng
# @Date  : 2020/12/19
# @Desc  : 学习进度标签v4

import os
import xlrd
import xlsxwriter
from collections import defaultdict,Counter
FilePath = r'H:\大数据中台项目\标签测试报告\Z计划-个人学习进度标签\搜题\V4.0\学习进度提测'

ExerciseRecordParam = {'filename':'习题+收藏原始数据后50个用户.xlsx','unitId_index':4,'secId_index':5,'type':'习题'}
SyncParam = {'filename':'同步数学+名师原始数据后50个用户(包含24个用户).xlsx','unitId_index':4,'secId_index':5,'type':'同步'}

def readRecord(param):
    MachinDic = defaultdict(list)
    MachinFinalDic = defaultdict(list)
    ContentData = xlrd.open_workbook(os.path.join(FilePath,param['filename']))
    Sheets = ContentData.sheets()
    for sheet in Sheets:
        for row in range(1, sheet.nrows):
            if sheet.cell_value(row, param['unitId_index']) == 42:
                pass
            else:
                MachinDic[sheet.cell_value(row, 0)].append((str(int(sheet.cell_value(row, param['unitId_index']))),
                                                            str(int(sheet.cell_value(row, param['secId_index'])))))
    for key in MachinDic.keys():
        result = Counter(MachinDic[key])
        d = sorted(result.items(), key=lambda x: x[1], reverse=True)
        print(key,'进度记录--------',d)
        MachinFinalDic[key] = d[0]
    print('\n\n世间最华丽的分割线\n\n')
    for key in MachinFinalDic.keys():
        print(key,'整理后进度记录-------------',MachinFinalDic[key])
    # workbook = xlsxwriter.Workbook(os.path.join(FilePath, '_'.join([param['type'], '学习进度']) + '.xlsx'))
    # ws = workbook.add_worksheet(u'sheet1')
    # row = 0
    # for key in MachinFinalDic.keys():
    #     ws.write(row, 0, key)
    #     ws.write(row, 1, MachinFinalDic[key][0][0])
    #     ws.write(row, 2, MachinFinalDic[key][0][1])
    #     row += 1
    # workbook.close()

def test():
    """
    列表根据出现次数降序排列
    :return:
    """
    a = [(1,1), (1, 1), (2, 2), (5, 5), (5, 5), (5,5)]
    result = Counter(a)
    d = sorted(result.items(),key=lambda x:x[1],reverse=True)
    print(d)

if __name__ == '__main__':
    readRecord(SyncParam)
    # test()