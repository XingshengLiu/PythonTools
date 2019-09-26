# @File  : ocrInterface.py
# @Author: LiuXingsheng
# @Date  : 2019/6/10
# @Desc  : 自研ocr接口测试

import requests



DOMAIN = 'http://ocr.eebbk.net'


def recognizeLatexLocal():
    """
    公式ocr
    :return:
    """
    url = DOMAIN + '/ocr/api/recognizeLatexLocal'
    file = {'url': open('ques.bmp', 'rb')}
    result = requests.post(url=url, files=file)
    print(result.text)


def recognizeLocal():
    """
    中英文ocr
    :return:
    """
    url = DOMAIN + '/ocr/api/recognizeLocal'
    file = {'url': open('eg.jpg', 'rb')}
    result = requests.post(url=url, files=file)
    print(result.text)


def recognizeWithLatexLocal():
    """
    综合ocr接口
    :return:
    """
    url = DOMAIN + '/ocr/api/recognizeWithLatexLocal'
    file = {'url': open('ques.bmp', 'rb')}
    result = requests.post(url=url, files=file)
    print(result.text)


def customizationOcr():
    """
    有道精准框
    :return:
    """
    url = 'http://socialsearch.eebbk.net/ocr/customizationOcr'
    param = {'xPoint': '0', 'yPoint': '0', 'serviceType': 'ocr', 'docRectify': 'no'}
    file = {'file': open('ques.bmp', 'rb')}
    result = requests.post(url=url, data=param, files=file)
    print(result.text)


def ocrWisdomWord():
    """
    有道字词
    :return:
    """
    url = 'http://socialsearch.eebbk.net/ocr/ocrWisdomWord'
    file = {'file': open('eg.jpg', 'rb')}
    result = requests.post(url=url, files=file)
    print(result.text)


def ocrFileReach():
    url = 'http://172.28.194.73:9080/ocr/api/recognizeLatexLocal'
    file = {'url': open('eg.jpg', 'rb')}
    result = requests.post(url=url, files=file)
    print(result.text)
    print(result.status_code)


def main():
    recognizeLatexLocal()
    recognizeLocal()
    recognizeWithLatexLocal()
    customizationOcr()
    ocrWisdomWord()
    # ocrFileReach()


if __name__ == '__main__':
    main()
