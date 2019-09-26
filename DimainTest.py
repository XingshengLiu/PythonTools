# @File  : DimainTest.py
# @Author: LiuXingsheng
# @Date  : 2019/3/29
# @Desc  :
import requests


def domainTest():
    url = 'http://contentcloudbasic.eebbk.net/api/grade/getNeedShowGradesBySubjectName?subjectName=%E8%AF%AD%E6%96%87&module=askHomework'
    result = requests.get(url)
    print(result.text)


def dominaTest_1():
    url = 'http://contentcloudbasic.eebbk.net/api/publisher/getNeedShowPublishersByGradeNameAndSubjectName?gradeName=%E4%B8%89%E5%B9%B4%E7%BA%A7&subjectName=%E8%AF%AD%E6%96%87&module=askHomework'
    result = requests.get(url)
    print(result.text)


def getEditionNameByShortName():
    url = 'http://synchinesecontent.eebbk.net/api/baseinfo/getEditionNameByShortName?editionName=%E4%BA%BA%E6%95%99%E7%89%88'
    result = requests.get(url)
    print(result.text)


def getBook():
    url = 'http://synchinesecontent.eebbk.net/api/book/getBook?bookName=%5B北京版%5D三年级数学上册'
    result = requests.get(url)
    print(result.text)


def getBaikeWords():
    url = 'http://test.eebbk.net/search-characterword-api/api/thirdparty/getBaikeWords'
    result = requests.get(url=url, params={'names': '玫瑰酒'})
    print(result.text)
    print(result.status_code)

def main():
    dominaTest_1()
    domainTest()
    getEditionNameByShortName()
    getBook()
    getBaikeWords()

if __name__ == '__main__':
    main()
