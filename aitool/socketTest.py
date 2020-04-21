# @File  : socketTest.py
# @Author: LiuXingsheng
# @Date  : 2019/10/18
# @Desc  :

import websocket
import json
url = 'wss://dds.dui.ai/dds/v2/test?serviceType=websocket&productId=278578090&apikey=0ddddeeeeeeeeeeee88888888260c8ab'
ws = websocket.create_connection(url=url)
data = {'topic':'recorder.stream.start','audio.audioType':'wav','audio.sampleRate':'16000','audio.channel':'1',
        'audio.sampleBytes':'2',}
ws.send(json.dumps(data))
print(ws.recv())
ws.close()