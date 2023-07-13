# @File  : getPaLabelId.py
# @Author: LiuXingsheng
# @Date  : 2020/8/10
# @Desc  :
from jpype import *
import json
import demjson
import xlrd
import os
import requests
import collections
import xlsxwriter
import DESCoder
import decryptorUtil
import time
# 图片素材路径
PicPath = r'\\172.28.2.84\kf2share1\AIData\业务全链路\智慧小布\竞品对比-点问搜题\10月\已入库素材\英语\粗框图'
# 报告生成路径
FilePath = r'H:\内容中台\精准搜题项目\测试集\作业工具月报测试集'

# 测试报告生成标题
ReportDict = {'TestTitle': '更新索引',
              'TestResourceMonth': '英语错误部分',
              'TestEnv': '专项环境',
              'TestDate': '1221'}
# 测试结果
ResultDict = {'FiveCounter': 0,
              'OneCounter': 0,
              'SumCounter': 0,
              'FiveAcc': 0.0,
              'OneAcc': 0.0,
              'SumTime':0.0,
              'AvgTime':0.0}
# 标注文件中序列号位于第几列
MachineIndex = 0
# 标注文件中图片名位于第几列（原粗框第1列,整页框第3列）
PicIndex = 1
# 标注文件中标注id位于第几列
LabelIndex = 2
# 统计结果文件中统计数据列号
CounterIndex = 10
# x坐标位于图片名中的索引（原粗框图x:-3 y:-2,整页框x:-6,y:-5）
XIndex = -4
# y坐标位于图片名中的索引
YIndex = -3

# 测试环境请求地址
# url = 'http://test.eebbk.net/pointquestion-app/app/topicProcess/searchDifficultProblems'
# 正式环境请求地址
url = 'http://pointquestion.eebbk.net/pointquestion-app/app/topicProcess/searchDifficultProblems'
# 专项验证环境请求地址
# url = 'http://47.112.238.105:8014/pointquestion-app/app/topicProcess/searchDifficultProblems'
# 测试环境整页框请求地址
# url = 'http://test.eebbk.net/pointquestion-app/app/topicProcess/searchProblemsByWholePicture'


def searchDifficultProblems():
    PicCount = collections.defaultdict(list)
    ContentData = xlrd.open_workbook(os.path.join(FilePath, ReportDict['TestResourceMonth'] + '标注Id.xlsx'))
    Sheets = ContentData.sheets()
    for sheet in Sheets:
        for row in range(1, sheet.nrows):
            # print(sheet.cell_value(row,0))
            LabelList = cleanStr(sheet.cell_value(row, LabelIndex)).split(',')
            PicCount[sheet.cell_value(row, MachineIndex)].append(sheet.cell_value(row, PicIndex))
            PicCount[sheet.cell_value(row, MachineIndex)].append(LabelList)
    header = {'machineId': '700S593001AE5', 'accountId': '37511587', 'apkPackageName': 'com.eebbk.aisearch.fingerstyle',
              'apkVersionCode': '4040000', 'apkVersionName': 'V4.4.0.0', 'deviceModel': 'S5',
              'deviceOSVersion': 'V1.0.0_180409'}
    ResultDict['SumCounter'] = len(PicCount)
    for machine in PicCount.keys():
        picName = PicCount[machine][0]
        try:
            with open(os.path.join(PicPath, picName), 'rb') as f:
                file = [('file', (picName, f.read()))]
            OrdXy = picName.split('_')
            prevtime = time.time()
            # 现网&测试&整页框&专项参数
            result = requests.post(url=url, headers=header, files=file,
                                   params={'xPoint': OrdXy[XIndex], 'yPoint': OrdXy[YIndex], 'isLimitTimes': '0'})
            # 整页框专项环境参数
            # result = requests.post(url=url, headers=header, files=file,
            #                        data={'xPoint': OrdXy[XIndex],'yPoint': OrdXy[YIndex],'isLimitTimes': '0',
            #                        'img_name': key,'src_w': 1224,'src_h': 1632})
            # print(result.text)
            posttime = time.time()
            requesttime = posttime-prevtime
            ResultDict['SumTime'] += requesttime
            if 'questionListId' in result.text and 'questions' in result.text:
                # 用于记录第几屏得到正确结果
                HitNumList = []
                FstQuesitonList = []
                objdata = json.loads(result.text)
                if objdata['data']['questions']:
                    fstquesitons = DESCoder.decryption_Q_py(objdata['data']['questions'])
                    if 'questionId' in fstquesitons:
                        FstQuesitonList = [str(fstquesitons['questionId'])]
                if objdata['data']['questionListId']:
                    decodequestionlist = DESCoder.decryption_Qids_py(objdata['data']['questionListId'])
                    # print('------>返回的后四屏结果',decodequestionlist)
                    CmpltList = FstQuesitonList + decodequestionlist
                    UnionSet = set(PicCount[machine][1]) & set(CmpltList)
                    print(CmpltList, PicCount[machine][1], '交集是', UnionSet)
                    PicCount[machine].append(CmpltList)
                    PicCount[machine].append(list(UnionSet))
                    for hit in list(UnionSet):
                        HitNumList.append(CmpltList.index(hit) + 1)
                    PicCount[machine].append(HitNumList)
                    if UnionSet:
                        PicCount[machine].append('五屏正确')
                        ResultDict['FiveCounter'] += 1
                    else:
                        PicCount[machine].append('五屏错误')
                    if 1 in HitNumList:
                        PicCount[machine].append('首屏正确')
                        ResultDict['OneCounter'] += 1
                    else:
                        PicCount[machine].append('首屏错误')
                else:
                    erormeg = 'data 或 questionListId返回数据为空'
                    PicCount[machine].append(erormeg)
                    PicCount[machine].append('')
                    PicCount[machine].append('')
                    PicCount[machine].append('五屏错误')
                    PicCount[machine].append('首屏错误')
            else:
                erormeg = 'questionListId或question未返回'
                PicCount[machine].append(erormeg)
                PicCount[machine].append('')
                PicCount[machine].append('')
                PicCount[machine].append('五屏错误')
                PicCount[machine].append('首屏错误')
        except TimeoutError:
            erormeg = '请求超时'
            PicCount[machine].append(erormeg)
            PicCount[machine].append('')
            PicCount[machine].append('')
            PicCount[machine].append('五屏错误')
            PicCount[machine].append('首屏错误')
        except KeyError:
            erormeg = '文件不存在'
            PicCount[machine].append(erormeg)
            PicCount[machine].append('')
            PicCount[machine].append('')
            PicCount[machine].append('五屏错误')
            PicCount[machine].append('首屏错误')
        except ConnectionError:
            erormeg = '连接错误'
            PicCount[machine].append(erormeg)
            PicCount[machine].append('')
            PicCount[machine].append('')
            PicCount[machine].append('五屏错误')
            PicCount[machine].append('首屏错误')
        except TypeError:
            erormeg = 'NoneType'
            PicCount[machine].append(erormeg)
            PicCount[machine].append('')
            PicCount[machine].append('')
            PicCount[machine].append('五屏错误')
            PicCount[machine].append('首屏错误')
        PicCount[machine].append(requesttime)
    ResultDict['FiveAcc'] = round(ResultDict['FiveCounter'] / ResultDict['SumCounter'], 2)
    ResultDict['OneAcc'] = round(ResultDict['OneCounter'] / ResultDict['SumCounter'], 2)
    ResultDict['AvgTime'] = ResultDict['SumTime'] / ResultDict['SumCounter']
    return PicCount


def cleanStr(excelstr):
    return excelstr.replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')

def setTitleProperty():
    return {
        'font_size': 11,
        'font_color': '#FFFFFF',
        'bold': False,
        'align': 'left',
        'valign': 'vcenter',
        'font_name': u'宋体',
        'text_wrap': False,
        'fg_color': '#00B0F0'
    }


def writeExcel(PicCount):
    Titlelist = ['序列号','粗框图', '标注Id', '返回id', '相同Id', '第几屏相同', '五屏结果', '首屏结果','请求耗时']
    workbook = xlsxwriter.Workbook(os.path.join(
        FilePath, '_'.join([ReportDict['TestTitle'], ReportDict['TestResourceMonth'],
                            ReportDict['TestEnv'], ReportDict['TestDate']]) + '.xlsx'))
    titleform = workbook.add_format(setTitleProperty())
    ws = workbook.add_worksheet(u'sheet1')
    for TitleIndex in range(len(Titlelist)):
        ws.write(0, TitleIndex, Titlelist[TitleIndex], titleform)
    row = 1
    for key in PicCount.keys():
        # 序列号
        ws.write(row, 0, str(key))
        # 粗框图文件名
        ws.write(row, 1, str(PicCount[key][0]))
        # 标注Id
        ws.write(row, 2, str(PicCount[key][1]))
        # 返回ID
        ws.write(row, 3, str(PicCount[key][2]))
        # 相同Id
        ws.write(row, 4, str(PicCount[key][3]))
        # 第几屏击中
        ws.write(row, 5, str(PicCount[key][4]))
        # 五屏结果
        ws.write(row, 6, str(PicCount[key][5]))
        # 首屏结果
        ws.write(row, 7, str(PicCount[key][6]))
        ws.write(row, 8, str(PicCount[key][7]))
        row += 1
    ws.write(0, CounterIndex, ResultDict['FiveCounter'])
    ws.write(1, CounterIndex, ResultDict['OneCounter'])
    ws.write(2, CounterIndex, ResultDict['SumCounter'])
    ws.write(3, CounterIndex, ResultDict['FiveAcc'])
    ws.write(4, CounterIndex, ResultDict['OneAcc'])
    ws.write(5, CounterIndex, ResultDict['AvgTime'])
    workbook.close()


def test():
    testpath = r'\\172.28.2.84\kf2share1\AIData\业务全链路\智慧小布\全链路-点问搜题\11月\PointAndAskFile\粗框图'
    url = 'http://pointquestion.eebbk.net/pointquestion-app/app/topicProcess/searchDifficultProblems'
    # url = 'http://47.112.238.105:8014/pointquestion-app/app/topicProcess/searchDifficultProblems'
    header = {'machineId': '700S593001AE5', 'accountId': '37511587', 'apkPackageName': 'com.eebbk.aisearch.fingerstyle',
              'apkVersionCode': '4040000', 'apkVersionName': 'V4.4.0.0', 'deviceModel': 'S5',
              'deviceOSVersion': 'V1.0.0_180409'}
    key = 'QuestionData20201119091946_489_217_700S5940013F0_material_PAAPhoto_70S5C08007836_PAAPhoto20201117120138_1001_1118_1566_2448_3264.jpg'
    with open(os.path.join(testpath,
                           key),
              'rb') as f:
        file = {'file': f.read()}
    ordx_y = key.split('_')
    t1 = time.time()
    result = requests.post(url=url, headers=header, files=file,
                           params={'xPoint': ordx_y[-4], 'yPoint': ordx_y[-3], 'isLimitTimes': '0'})
    print('请求耗时',str(result.elapsed.seconds))
    t2 = time.time()
    print('相减时间',t2 - t1)
    print(result.text)
    if 'questionListId' in result.text:
        objdata = demjson.decode(result.text)
        fstquesitons = DESCoder.decryption_Q_py(objdata['data']['questions'])
        # fstquesitons_origi = decryptorUtil.decryption_Q(objdata['data']['questions'])
        if 'questionId' in fstquesitons:
            FstQuesitonList = [str(fstquesitons['questionId'])]
            # FstQuesitonList_origi = [str(fstquesitons['questionId'])]
        if objdata['data']:
            if objdata['data']['questionListId']:
                decodequestionlist = DESCoder.decryption_Qids_py(objdata['data']['questionListId'])
                # decodequestionlist_origi = decryptorUtil.decryption_Qids(objdata['data']['questionListId'])
                print('原',FstQuesitonList+decodequestionlist)
                # print('现在', FstQuesitonList_origi + decodequestionlist_origi)
            else:
                print('questionListId返回数据为空')
    else:
        print('未返回questionListId')


if __name__ == "__main__":
    test()
    # piccunt = searchDifficultProblems()
    # writeExcel(piccunt)
    # shutdownJVM()
    # execute_sql()

