# @File  : ASRtest.py
# @Author: LiuXingsheng
# @Date  : 2019/10/23
# @Desc  : ASR准确率测试

import json
import time
import hmac
import asyncio
import websockets
from hashlib import sha1
from uuid import uuid4
import os
import xlrd
import xlsxwriter
import datetime

alias = "prod"
audioFile = "1.wav"

# 小布问作业产品id及apikey
productId = "278571900"
apikey = "63f0f24fc55263f0f24fc5525ad93aab"
PATH = r'H:\ocr本地自动化保存结果\ASRresult\ASR_resources_Path.txt'


def openResouce():
    with open(PATH, 'r')as f:
        allPath = f.read()
    pathList = allPath.split('@')
    resoutcePath = pathList[0]
    savePath = pathList[1]
    return resoutcePath, savePath


def getLabelcontent(resoutcePath, savePath):
    wavList = []
    filelist = os.listdir(resoutcePath)
    for file in filelist:
        if file.endswith('.xlsx'):
            data = xlrd.open_workbook(os.path.join(resoutcePath, file))
            sheet = data.sheets()[0]
            rows = sheet.nrows
            for row in range(1, rows):
                wavList.append((sheet.cell_value(row, 0),
                                sheet.cell_value(row, 1).strip().replace("“", "").replace("”", "").replace(" ", "")))
            return wavList


async def textRequest(ws):
    content = {
        "aiType": "dm",
        "topic": 'nlu.input.text',
        "recordId": uuid4().hex,
        "refText": "姚明是谁"
    }
    try:
        await ws.send(json.dumps(content))
        resp = await ws.recv()
        print(resp)
    except websockets.exceptions.ConnectionClosed as exp:
        print(exp)


async def triggerIntent(ws):
    content = {
        "aiType": "dm",
        'topic': 'dm.input.intent',
        'recordId': uuid4().hex,
        'skillId': '2018040200000004',
        'intent': '查询天气',
        'task': "天气",
        'slots': {
            '国内城市': "苏州"
        }
    }
    try:
        await ws.send(json.dumps(content))
        resp = await ws.recv()
        print(resp)
    except websockets.exceptions.ConnectionClosed as exp:
        print(exp)


async def audioRequest(ws, wavList):
    successcount = 0
    failcount = 0
    resoutcePath, savePath = openResouce()
    resList = []
    content = {
        "aiType": "dm",
        "topic": "recorder.stream.start",
        "recordId": uuid4().hex,
        "audio": {
            "audioType": "wav",
            "sampleRate": 16000,
            "channel": 1,
            "sampleBytes": 2
        }
    }
    try:
        for wav in wavList:
            await ws.send(json.dumps(content))
            filePath = os.path.join(resoutcePath, wav[0])
            fileLabel = wav[1]
            with open(filePath, 'rb') as f:
                while True:
                    chunk = f.read(3200)
                    if not chunk:
                        await ws.send(bytes("", encoding="utf-8"))
                        break
                    await ws.send(chunk)
            async for message in ws:
                resp = json.loads(message)
                if resp is None or resp['dm'] is None:
                    recogtext = ''
                    result = '-1 response data is null'
                    resList.append((filePath, fileLabel, recogtext, result))
                    return resList, successcount, failcount
                if resp['dm']['input'] == fileLabel:
                    successcount += 1
                    resList.append((filePath, fileLabel, resp['dm']['input'], '1'))
                else:
                    failcount += 1
                    resList.append((filePath, fileLabel, resp['dm']['input'], '0'))
                if 'dm' in resp:
                    break
        return resList, successcount, failcount
    except websockets.exceptions.ConnectionClosed as exp:
        print(exp)
        ws.close()


def setTitleProperty():
    return {
        'font_size': 11,
        'font_color': '#FFFFFF',
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': u'微软雅黑',
        'text_wrap': False,
        'fg_color': '#00B0F0'
    }


def setContentProperty():
    return {
        'font_size': 11,
        'font_color': '#000000',
        'bold': False,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': u'微软雅黑',
        'text_wrap': False,
    }


def writeContent(resList, sucess, fail):
    dt = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = '{0}{1}{2}'.format('ASRResult_', str(dt), '.xlsx')
    resoucePath, savePath = openResouce()
    column = 1
    try:
        workbook = xlsxwriter.Workbook(os.path.join(savePath, filename))
        titleform = workbook.add_format(setTitleProperty())
        contentform = workbook.add_format(setContentProperty())
        ws_detail = workbook.add_worksheet(u'测试详情')
        ws_sum = workbook.add_worksheet(u'统计结果')
        ws_detail.set_column("A:D", 30)
        ws_detail.write(0, 0, '文件名', titleform)
        ws_detail.write(0, 1, '标注文本', titleform)
        ws_detail.write(0, 2, '识别结果', titleform)
        ws_detail.write(0, 3, '结果(1 为正确，0 为错误)', titleform)
        for tp in resList:
            ws_detail.write(column, 0, tp[0], contentform)
            ws_detail.write(column, 1, tp[1], contentform)
            ws_detail.write(column, 2, tp[2], contentform)
            ws_detail.write(column, 3, tp[3], contentform)
            column = column + 1
        ws_sum.write(0, 1, '个数', titleform)
        ws_sum.write(0, 2, '占比', titleform)
        ws_sum.write(1, 0, '正确', titleform)
        ws_sum.write(2, 0, '错误', titleform)
        ws_sum.write(1, 1, str(sucess), contentform)
        ws_sum.write(1, 2, '{:.2f}%'.format(sucess / (sucess + fail) * 100), contentform)
        ws_sum.write(2, 1, str(fail), contentform)
        ws_sum.write(2, 2, '{:.2f}%'.format(fail / (sucess + fail) * 100), contentform)
        workbook.close()
    except IOError as ioerror:
        print('文件写错误:' + str(ioerror))


async def dds_demo(wavList):
    # 云端对云端。
    # url = f"wss://dds.dui.ai/dds/v2/{alias}?serviceType=websocket&productId={productId}&apikey={apikey}"
    url = 'ws://dds-hb.dui.ai/dds/v1/prod370?productId=278571900&serviceType=websocket&apikey=DUIKEYS-BBKTEST'

    async with websockets.connect(url) as websocket:
        # await textRequest(websocket)
        # await triggerIntent(websocket)
        resList, sucess, fail = await audioRequest(websocket, wavList)
        writeContent(resList, sucess, fail)


def findnewestfile(file_path):
    filenames = os.listdir(file_path)
    print(filenames)
    name_ = []
    time_ = []
    for filename in filenames:
        if '.xlsx' == filename[-5:]:  ##因我只想查询png类的文件，不用的可以删除
            # print filename
            c_time = os.path.getctime(file_path + '\\' + filename)

            # print type(mtime)
            name_.append(file_path + '\\' + filename)
            time_.append(c_time)
            # print filename,mtime
    newest_file = name_[time_.index(max(time_))]
    return newest_file


def startFunction():
    resoutcePath, savePath = openResouce()
    wavList = getLabelcontent(resoutcePath, savePath)
    asyncio.get_event_loop().run_until_complete(dds_demo(wavList))
    filename = findnewestfile(savePath)
    return str(os.path.join(savePath, filename))

# if __name__ == '__main__':
#     wavList = getLabelcontent()
#     asyncio.get_event_loop().run_until_complete(dds_demo(wavList))
