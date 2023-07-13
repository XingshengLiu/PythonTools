# @File  : vivoCalculation.py
# @Author: LiuXingsheng
# @Date  : 2020/10/23
# @Desc  : 计算题优化_v2
import os
import requests
import demjson
import json
from contentmidplatform.equationAccuracyTest import readExcel
from contentmidplatform.equationAccuracyTest import writecontent

Dirpath = r'\\172.28.2.84\kf2share1\AIData\业务全链路\智慧小布\技术专项-计算题\无等号&除法竖式&比大小\压缩校正图'

def searchVivoCalculation(piclist):
    compllist = []
    # url = 'http://testaliyun.eebbk.net/ai-search/api/searchVivoCalculation'
    url = 'http://47.112.238.105:8014/ai-search/api/searchVivoCalculation'
    for pic in piclist:
        ordx,ordy = pic[0].split('_')[-6],pic[0].split('_')[-5]
        with open(os.path.join(Dirpath,pic[0]),'rb') as f:
            file = {'file':f.read()}
            result = requests.post(url=url,files = file,params = {'zipType':'unzip','xPoint':int(ordx),'yPoint':int(ordy),'ocrType':'self4','isTest':True})
            print(result.text)
            if result.status_code == requests.status_codes.codes.ok:
                if 'resultBean' in result.text:
                    objdata = demjson.decode(result.text)
                    if objdata['data']['resultBean'] and ('questionAnalyse' in objdata['data']['resultBean']):
                        print('------>>>>>',objdata['data']['resultBean']['questionAnalyse'])
                        if cleanStr(pic[1]) == objdata['data']['resultBean']['questionAnalyse']:
                            print('正确')
                            compllist.append([pic[0],pic[1],objdata['data']['resultBean']['questionAnalyse'],'正确'])
                        else:
                            print('错误，图片名{0}，标注是{1}，返回是{2}'.format(pic[0],pic[1],objdata['data']['resultBean']['questionAnalyse']))
                            compllist.append([pic[0],pic[1],objdata['data']['resultBean']['questionAnalyse'],'错误'])
                    else:
                        print('---->',pic[0])
                        compllist.append([pic[0],pic[1],'无返回','questionAnalyse未返回'])
                else:
                    print('---->>', pic[0])
                    compllist.append([pic[0], pic[1], '无返回', 'resultBean未返回'])
            else:
                print('---->>>', pic[0])
                compllist.append([pic[0],pic[1],'无返回','请求错误'])
    return compllist

def cleanStr(labelstr):
    return str(labelstr).replace('（','(').replace('）',')').replace(' ','')


if __name__ == '__main__':
    piclist = readExcel(Dirpath,'计算题标注.xlsx')
    compllist = searchVivoCalculation(piclist)
    writecontent(compllist,Dirpath,'计算题优化_专项环境_优化场景素材准确率0220.xlsx')