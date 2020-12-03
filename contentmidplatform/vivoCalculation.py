# @File  : vivoCalculation.py
# @Author: LiuXingsheng
# @Date  : 2020/10/23
# @Desc  : 计算题优化_v2
import os
import requests
import demjson
from contentmidplatform.equationAccuracyTest import readExcel
from contentmidplatform.equationAccuracyTest import writecontent

Dirpath = r'H:\内容中台\精准搜题项目\测试集\计算题测试\用户笔迹\粗框图'

def searchVivoCalculation(piclist):
    compllist = []
    url = 'http://testaliyun.eebbk.net/ai-search/api/searchVivoCalculation'
    for pic in piclist:
        ordx,ordy = pic[0].split('_')[-4],pic[0].split('_')[-3]
        with open(os.path.join(Dirpath,pic[0]),'rb') as f:
            file = {'file':f.read()}
            result = requests.post(url=url,files = file,params = {'zipType':'unzip','xPoint':int(ordx),'yPoint':int(ordy),'ocrType':'self4'})
            print(result.text)
            if result.status_code == requests.status_codes.codes.ok:
                if 'resultBean' in result.text:
                    objdata = demjson.decode(result.text)
                    if objdata['data']['resultBean'] and ('questionAnalyse' in objdata['data']['resultBean']):
                        print('------>>>>>',objdata['data']['resultBean']['questionAnalyse'])
                        if pic[1] == objdata['data']['resultBean']['questionAnalyse']:
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

if __name__ == '__main__':
    piclist = readExcel()
    compllist = searchVivoCalculation(piclist)
    writecontent(compllist,Dirpath,'计算题优化_正式环境基线准确率.xlsx')