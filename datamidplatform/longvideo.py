# @File  : longvideo.py
# @Author: LiuXingsheng
# @Date  : 2020/9/18
# @Desc  : 长视频相关标签

import xlrd
import os
import collections

def readdata():
    videoresultlist = collections.defaultdict(list)
    datadiclist = collections.defaultdict(list)
    filepath = r'H:\大数据中台项目\标签测试报告\长视频相关标签\测试方案'
    contentdata = xlrd.open_workbook(os.path.join(filepath, '长视频播放及时长原始数据（50个视频id).xlsx'))
    sheets = contentdata.sheets()
    for sheet in sheets:
        for row in range(1, sheet.nrows):
            # 播放时长，机器序列号
            if sheet.cell_value(row, 7) =='null':
                pass
            else:
                datadiclist[int(sheet.cell_value(row, 2))].append([int(sheet.cell_value(row, 7)),sheet.cell_value(row, 10)])
    for key in datadiclist.keys():
        playsumtime = 0
        machieset = set()
        playtimes = len(datadiclist[key])
        for item in datadiclist[key]:
            playsumtime += item[0]
            machieset.add(item[1])
        avgplaytime = playsumtime/playtimes
        videoresultlist[key].append([playtimes,len(machieset),playsumtime,avgplaytime])
    return videoresultlist

def readLikedata(videoresultlist):
    datadiclist = collections.defaultdict(list)
    filepath = r'H:\大数据中台项目\标签测试报告\长视频相关标签\测试方案'
    contentdata = xlrd.open_workbook(os.path.join(filepath, '点赞原始数据（50个).xlsx'))
    sheets = contentdata.sheets()
    for sheet in sheets:
        for row in range(1, sheet.nrows):
            datadiclist[int(sheet.cell_value(row, 3))].append(sheet.cell_value(row, 5))
    for key in videoresultlist.keys():
        videoresultlist[key].append(len(datadiclist[key]))
    for key in videoresultlist.keys():
        print(key,videoresultlist[key][0][0],videoresultlist[key][0][1],videoresultlist[key][0][2],videoresultlist[key][0][3],videoresultlist[key][1])

if __name__ == '__main__':
    videoresultlist = readdata()
    readLikedata(videoresultlist)