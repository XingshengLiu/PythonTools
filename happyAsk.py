# @File  : happyAsk.py
# @Author: LiuXingsheng
# @Date  : 2018/10/24
# @Desc  :
import hashlib, demjson, time
import requests

REQUEST_DOMAIN = 'https://x.bbkedu.com'

PHONE_NUM = '18576370106'
PHONE_PWD = 'lxs123456'
COMMON_PARAM = {'pid': '0',
                'rid': 'b80385dc5c0240d2ab5137d8add83163', 'cpFlag': '0'}

MEMID = '0497135fdd184a5d8189d1bf81080de5'
TOKEN = '568d7ce6a80844e3931419c51cb1f238'

PHONE_NUM_DSX = '13669882994'
PHONE_PWD_DSX = 'dsx123456'
MEMID_DSX = 'a998ec400a544d84838631a9d0e4ab69'
TOKEN_DSX = 'b7fb1d4c55374f25b00e22d0932d180a'

PHONE_NUM_YCY = '13971877710'
PHONE_PWD_YCY = 'ycy123456'
MEMID_YCY = '4de3a9fd75554b6c930c09ba6877a164'
TOKEN_YCY = '65e67f92465e42ee9a5623f281094b1b'

PHONE_NUM_MM = '15009693096'
PHONE_PWD_MM = 'zsq123456'
MEMID_FHM = '18589ce5055e4061945448553006cd50'
TOKEN_FHM = '2fb89916a21e45689eb01fdbf52f0e44'

PHONE_NUM_HXL = '18676386216'
PHONE_PWD_HXL = 'hxl123456'
MEMID_HXL = '7d9f919186074fd499d7b1392d3bd978'
TOKEN_HXL = 'd35eff8cdf7740f8b272f94dc8ec564f'

PHONE_NUM_YXQ = '13266225488'
PHONE_PWD_YXQ = 'hxl123456'
MEMID_YXQ = '0167f1b37b234d7eb40522743c84442f'
TOKEN_YXQ = '0f7edef45ccd41af9c318306cfabe04a'


# 获取当前时间戳
def getTimeStamp():
    t = time.time()
    return int(t)


# 获取请求头
def getRequestHeader(url, timestamp):
    headerStr = url + MEMID + TOKEN + timestamp
    print(getMD5Str(headerStr))
    return {'sIgn': getMD5Str(headerStr)}


# 获取验证码
def getMessageCode(phoneNum):
    url = REQUEST_DOMAIN + '/api/user/getSmsMsg.do'
    requestParams = {'memPhone': phoneNum, 'msgType': '1', 'msgLen': '4'}
    result = requests.request(method='POST', url=url, json=requestParams)
    print(result.text)


# 注册当前用户 此处smsVerifCode 需要从手机上查看，动态变化
def register(num, name, psd, sms):
    url = REQUEST_DOMAIN + '/api/user/register.do'
    requestParams = {'memPhone': num, 'memName': name, 'memPwd1': getMD5Str(psd), 'smsVerifCode': str(sms),
                     'pid': '0',
                     'rid': 'b80385dc5c0240d2ab5137d8add83163', 'cpFlag': '0', 'regEquipment': 'BK'}
    result = requests.request(method='POST', url=url, json=requestParams)
    print(result.text)


# 登录接口
def login(num, psd):
    url = REQUEST_DOMAIN + '/api/user/login.do'
    requestParam = {'loginType': '2', 'loginAccount': num, 'loginPwd': getMD5Str(psd), 'regEquipment': 'WX'}
    requestParam.update(COMMON_PARAM)
    result = requests.request(method='POST', url=url, json=requestParam)
    print(result.text)
    if result.status_code == 200:
        loginInfo = demjson.decode(result.text)
        if 'data' in loginInfo:
            MEMID = loginInfo['data']['memId']
            TOKEN = loginInfo['data']['tokEn']
            print(MEMID + ' ' + TOKEN)


# 课程详情
def getMyCoursePlayList():
    timestamp = str(getTimeStamp())
    print(timestamp)
    url = REQUEST_DOMAIN + '/api/user/myCoursePlayList.do'
    urlwitParam = url + '?&memId=' + MEMID + '&ts=' + timestamp
    requestParam = {'bookingId': 20254567, 'courseId': 13544, 'pid': '0'}
    # result = requests.request(method='POST', url=urlwitParam,
    #                           headers=getRequestHeader(REQUEST_DOMAIN + '/api/user/myCoursePlayList.do', timestamp),
    #                           json=requestParam)
    # print(result.text)


# 添加到购物车
def addToCar():
    timestamp = str(getTimeStamp())
    url = REQUEST_DOMAIN + '/api/mcp/cart/c.do'
    urlwitParam = url + '?&memId=' + MEMID + '&ts=' + timestamp
    requestParam = {'seq': 20254567, 'goodsId': 13544, 'orderSource': '0', 'amt': '1', 'pid': '0'}
    result = requests.request(method='POST', url=urlwitParam,
                              headers=getRequestHeader(url, timestamp),
                              json=requestParam)
    print(result.text)
    info = demjson.decode(result.text)
    if 'data' in info:
        seq = info['data']['seq']
        goodsId = info['data']['goodsId']
        faqijiesuan_url = REQUEST_DOMAIN + '/api/mcp/cart/goConfirm.do'
        faqijiesuan_urlwitParam = faqijiesuan_url + '?&memId=' + MEMID + '&ts=' + timestamp
        faqijiesuan_requestParam = {'type': 0, 'orderSource': '小程序',
                                    'selectedItems': [{'seq': str(seq), 'goodsId': str(goodsId)}], 'amt': '1'}
        result = requests.request(method='POST', url=faqijiesuan_urlwitParam,
                                  headers=getRequestHeader(url, timestamp),
                                  json=faqijiesuan_requestParam)
        print(result.text)
        faqijiesuanInfo = demjson.decode(result.text)
        if 'data' in faqijiesuanInfo:
            batchNo = faqijiesuanInfo['batchNo']
            grandTtl = faqijiesuanInfo['grandTtl']
            jiesuan_url = REQUEST_DOMAIN + '/api/mcp/cart/settlement.do'
            jiesuan_urlwitParam = jiesuan_url + '?&memId=' + MEMID + '&ts=' + timestamp
            jiesuan_requestParam = {'type': 0, 'orderSource': '小程序',
                                    'selectedItems': [{'seq': str(seq), 'goodsId': str(goodsId)}], 'amt': '1'}


# 生成MD5加密串
def getMD5Str(params):
    return hashlib.md5(params.encode(encoding='utf-8')).hexdigest()


class Item:
    machineId = ''
    titleImgUrl = ''
    typeId = 0
    typeParentId = 0


def inertpatch():
    url = 'http://test.eebbk.net/pointquestion-app/app/titleCollectInfo/patchInsert?machineId=700H38300018B'
    param = '''[{"machineId": "700H38300018B", "titleImgUrl": "test", "typeId": 93, "typeParentId": 91},
    {"machineId": "700H38300018B", "titleImgUrl": "testtesttest", "typeId": 121, "typeParentId": 119},
    {"machineId": "700H38300018B", "titleImgUrl": "testtesttest123", "typeId": 87, "typeParentId": 83},
    {"machineId": "700H38300018B", "titleImgUrl": "testtesttest123", "typeId": 103, "typeParentId": 101},
    {"machineId": "700H38300018B", "titleImgUrl": "testtesttest5555", "typeId": 121, "typeParentId": 119}]'''
    result = requests.post(url=url, data=param, headers={'Content-Type': 'application/json'})
    print(result.text)


def selectByBookId():
    url = 'http://172.28.194.65:8080/robot/bookInfo/selectByBookId'
    params = 'dcffbe0c087c2b667e323f59209553e823016a608c336a79c7a22330d38805eaf4d2991622cca819'
    result = requests.request(method='POST', url=url, data=params)
    print(result.text)


def main():
    # getMessageCode(PHONE_NUM_DSX)
    # getMessageCode(PHONE_NUM_YCY)
    # getMessageCode(PHONE_NUM_YXQ)
    # getMessageCode(PHONE_NUM_MM)
    # register(PHONE_NUM_DSX,PHONE_PWD_DSX,5221)
    # register(PHONE_NUM_YCY,PHONE_PWD_YCY,5665)
    # register(PHONE_NUM_YXQ,PHONE_PWD_YXQ,6360)
    # register(PHONE_NUM_MM, 'zsq', PHONE_PWD_MM, 5866)
    # login(PHONE_NUM_DSX,PHONE_PWD_DSX)
    # login(PHONE_NUM_YCY,PHONE_PWD_YCY)
    # login(PHONE_NUM_YXQ,PHONE_PWD_YXQ)
    # login(PHONE_NUM_HXL,PHONE_PWD_HXL)
    # login(PHONE_NUM, PHONE_PWD)
    # login(PHONE_NUM_MM, PHONE_PWD_MM)
    # getMyCoursePlayList()
    # addToCar()
    # inertpatch()
    selectByBookId()


if __name__ == '__main__':
    main()
