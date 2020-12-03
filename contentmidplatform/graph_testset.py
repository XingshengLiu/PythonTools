# @File  : graph_testset.py
# @Author: LiuXingsheng
# @Date  : 2020/9/24
# @Desc  : 知识图谱V0.2测试集筛选
import os
import csv
import json
DirPath = r'C:\Users\Administrator\Desktop'

def readUserData():
    sentencelist = []
    with open(os.path.join(DirPath, '知识图谱v0.2测试集.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        datalist = [row for row in reader]
        for data in datalist:
            sentencelist.append(data[4])
        with open(os.path.join(DirPath,'0.2测试集.txt'),'w',encoding='utf-8')as fwrite:
            for sentece in sentencelist:
                if 'nlu' in sentece:
                    objdata = json.loads(sentece)
                    fwrite.write(str(objdata['nlu']['input']) + '\n')
                else:
                    pass

if __name__ == '__main__':
    readUserData()
