# @File  : covercalcu.py
# @Author: LiuXingsheng
# @Date  : 2021/1/20
# @Desc  : 学习进度覆盖率计算脚本
from collections import defaultdict
import csv
import os
DirPath = r'F:\EnterpriseMM Cache\WXWork Files\File\2021-01\NeuralCD_predict_Version02_test\NeuralCD_predict_Version02\bubugao_data\original_data'
def getAllData():
    counternum = [0,0,0,0,0]
    datadiclist = defaultdict(set)
    with open(os.path.join(DirPath, 'exercise_search_record_formerweek.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
    for data in datalist[1:]:
        datadiclist[data[0]].add(data[2])
    sum = len(datadiclist)
    for key in datadiclist.keys():
        if len(datadiclist[key]) >= 4:
            counternum[0] += 1
        if len(datadiclist[key]) >= 6:
            counternum[1] += 1
        if len(datadiclist[key]) >= 8:
            counternum[2] += 1
        if len(datadiclist[key]) >= 10:
            counternum[3] += 1
        if len(datadiclist[key]) >= 12:
            counternum[4] += 1
    print('总数是',sum)
    for count in counternum:
        print(count/sum)


if __name__ == '__main__':
    getAllData()
