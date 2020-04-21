# @File  : testsocial.py
# @Author: LiuXingsheng
# @Date  : 2019/12/30
# @Desc  :

import requests

urls = ['10.200.67.219:8081', '10.200.67.220:8081', '10.200.67.221:8081', '10.200.67.223:8081', '10.200.67.224:8081',
        '10.200.67.219:8082', '10.200.67.220:8082', '10.200.67.221:8082', '10.200.67.223:8082', '10.200.67.224:8082']


def searchs():
    file = {'files': open('FingerData3204791_0_367_217_2448_3264.jpg', 'rb')}
    params = {'zipType': 'none', 'xPoint': '367', 'yPoint': '217'}
    for item in urls:
        url = 'http://' + str(item) + '/ai-search/api/searchs'
        result = requests.post(url=url, params=params, files=file)
        print(result.text)


if __name__ == '__main__':
    searchs()
