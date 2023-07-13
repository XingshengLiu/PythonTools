# @File  : equationAccuracyTest.py
# @Author: LiuXingsheng
# @Date  : 2020/8/18
# @Desc  : 算式识别率测试
import os
import json
import xlrd
import xlsxwriter
import requests

PicPath = r'C:\Users\Administrator\Desktop\JpgData20200817165032_0_821_307_3456_4608g.jpg'
Dirpath = r'\\172.28.2.84\kf2share1\AIData\业务全链路\智慧小布\技术专项-计算题\用户笔迹\粗框图'
def readAccurateFrameExcel():
    accurateFramedic = {}
    contentdata = xlrd.open_workbook(os.path.join(Dirpath, '图片名1.xlsx'))
    sheet = contentdata.sheets()[0]
    for row in range(1,sheet.nrows):
        accurateFramedic[sheet.cell_value(row, 0).split('_')[0]] = sheet.cell_value(row, 1)
    
def readExcel(Dirpath,filename):
    piclist = []
    # contentdata = xlrd.open_workbook(os.path.join(os.getcwd(),'图片名1.xlsx'))
    contentdata = xlrd.open_workbook(os.path.join(Dirpath, filename))
    sheet = contentdata.sheets()[0]
    for row in range(1,sheet.nrows):
        piclist.append([sheet.cell_value(row, 3),sheet.cell_value(row, 4)])
    return piclist


def writecontent(cmpltlist,path = Dirpath,fliename='算式识别准确率_灰度前.xlsx'):
    workbook = xlsxwriter.Workbook(os.path.join(path, fliename))
    # workbook = xlsxwriter.Workbook(os.path.join(os.getcwd(), '算式识别准确率.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(cmpltlist)):
        for column in range(len(cmpltlist[row])):
            ws.write(row,column,cmpltlist[row][column])
    workbook.close()


def cleanStr(excelstr):
    if r'/' in excelstr or '*' in excelstr:
        return excelstr.strip().replace(' ', '').replace('/', '÷').replace('*','×')
    else:
        return str(excelstr.strip().replace(' ', '').split('=')[0])


def mergePageAllBox(piclist):
    header = {'machineId': '700S594001FDA', 'accountId': '37511587', 'apkPackageName': 'com.eebbk.aisearch.fingerstyle',
              'apkVersionCode': '4040000', 'apkVersionName': 'V4.4.0.0', 'deviceModel': 'S5',
              'deviceOSVersion': 'V1.0.0_180409'}
    cmpltlist = []
    validcount = 0
    correctcount = 0
    url = 'http://testaliyun.eebbk.net/work-review/app/oralComputational/mergePageAllBox'
    for pic in piclist:
        if pic[1] in ['无效','无效图片']:
            pass
        else:
            validcount += 1
            wordslist = []
            newlabelstr = cleanStr(pic[1])
            iscorrect = 0
            with open(os.path.join(Dirpath,pic[0]), 'rb') as f:
                file = {'file': f.read()}
                result = requests.post(url=url, files=file,headers = header)
                if result.status_code == 200 and 'data' in result.text:
                    objdata = json.loads(result.text)
                    if objdata['data'] and 'pageAllBoxVos' in objdata['data'] and len(objdata['data']['pageAllBoxVos']) != 0:
                        for item in objdata['data']['pageAllBoxVos']:
                            if item is None or item['sub'] is None:
                                pass
                            else:
                                for item in item['sub']:
                                    if item['words'] is None:
                                        wordslist.append('null')
                                        continue
                                    else:
                                        wordslist.append(item['words'])
                        for word in wordslist:
                            if newlabelstr in word:
                                print('标注字符串是{0} 返回字符串是{1}'.format(newlabelstr,str(word)))
                                iscorrect = 1
                                correctcount +=1
                                break
                            else:
                                pass
                        if iscorrect:cmpltlist.append([pic[0], newlabelstr, str(wordslist), '正确'])
                        else:cmpltlist.append([pic[0], newlabelstr, str(wordslist), '错误'])
                    else:
                        errmsg = '未返回pageAllBoxVos 或 pageAllBoxVos 数据为空'
                        print(pic[0],'返回信息是',result.text)
                        cmpltlist.append([pic[0], newlabelstr, errmsg, '错误'])
                else:
                    errmsg = result.text
                    print(pic[0], '错误信息是', errmsg)
                    cmpltlist.append([pic[0], newlabelstr, errmsg, '错误'])
    print('正确率：',correctcount/validcount)
    return cmpltlist


if __name__ == '__main__':
    piclist = readExcel()
    cmpltlist = mergePageAllBox(piclist)
    writecontent(cmpltlist)
    # url = 'http://testaliyun.eebbk.net/work-review/app/oralComputational/mergePageAllBox'
    # with open(os.path.join(Dirpath, 'JpgData20200817165032_0_316672896_307_3456_4608.jpg'), 'rb') as f:
    #     file = {'file': f.read()}
    #     result = requests.post(url=url, files=file)
    #     print(result.text)
