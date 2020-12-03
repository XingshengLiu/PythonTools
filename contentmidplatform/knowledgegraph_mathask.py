# @File  : knowledgegraph_mathask.py
# @Author: LiuXingsheng
# @Date  : 2020/8/25
# @Desc  : 现网语料库数学意图筛选

import csv
import os
import requests
import json
import xlsxwriter
DirPath = r'H:\内容中台\知识图谱项目\用户数据测试集\现网语料库筛选'
title = 'part1'
import time
def cleanlist(s):
    processed = str(s).replace('[', '').replace(']', '').replace('\'', '')
    if len(processed) >3:
        return processed
    else:
        return 0


def readUserData():
    with open(os.path.join(DirPath, '现网语料库_'  + title + '.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        sentencelist = [row for row in reader]
    # print('长度大于3的句子一共有',len(sentencelist))
    with open(os.path.join(DirPath, title + '现网语料库_筛选确认.txt'), 'a', encoding='utf-8') as fwrite:
        for s in sentencelist:
            sentence = cleanlist(s)
            if not sentence:
                pass
            else:
                time.sleep(0.1)
                result_top = requests.get(url='http://172.28.191.249:8310/ask-homework/top_scene_classify',params = {'sentence':sentence})
                if result_top.status_code == 200:
                    objdata = json.loads(result_top.text)
                    if objdata['classifies']:
                        for item in objdata['classifies']:
                            if item['scene'] == 'study':
                                result_sub = requests.get(
                                    url='http://172.28.191.249:8311/ask-homework/subject_classify',
                                    params={'sentence': sentence})
                                if result_sub.status_code == 200:
                                    sub_objdata = json.loads(result_sub.text)
                                    if sub_objdata['classifies']:
                                        for sub_item in sub_objdata['classifies']:
                                            if sub_item['scene'] == 'math':
                                                fwrite.write(sentence + '\n')
                                                fwrite.flush()
                                            else:
                                                pass
                                    else:
                                        pass
                                else:
                                    pass
                            else:
                                pass
                    else:
                        pass


if __name__ == '__main__':
    sentenceset = readUserData()
