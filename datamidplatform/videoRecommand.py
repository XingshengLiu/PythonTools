# @File  : videoRecommand.py
# @Author: LiuXingsheng
# @Date  : 2020/10/19
# @Desc  :

import requests
import demjson
from pymysql import connect

def getVideoHot():
    url = 'http://udc.eebbk.net/recommend-api/api/course/getVideoHot'
    param = {'machineId':'700S60100145G','subjectId':1,'pageIndex':0,'pageSize':400,'gradeId':6,'termId':2}
    result = requests.post(url=url,params=  param)
    objdata = demjson.decode(result.text)
    print(result.text)
    print(len(objdata['data']))

if __name__ == '__main__':
    getVideoHot()