# @File  : DimainTest.py
# @Author: LiuXingsheng
# @Date  : 2019/3/29
# @Desc  :
import requests

import demjson
from pytest import approx


class Test1(object):

    def test_domainTest(self):
        url = 'http://contentcloudbasic.eebbk.net/api/grade/getNeedShowGradesBySubjectName?subjectName=%E8%AF%AD%E6%96%87&module=askHomework'
        result = requests.get(url)
        # print(result.text)
        assert 200 == result.status_code

    def test_dominaTest_1(self):
        url = 'http://contentcloudbasic.eebbk.net/api/publisher/getNeedShowPublishersByGradeNameAndSubjectName?gradeName=%E4%B8%89%E5%B9%B4%E7%BA%A7&subjectName=%E8%AF%AD%E6%96%87&module=askHomework'
        result = requests.get(url)
        print(result.text)
        assert 200 == result.status_code
        objdata = demjson.decode(result.text)
        for item in objdata['data']:
            assert '天津教育出版社' == item['name']

    def test_getEditionNameByShortName(self):
        url = 'http://synchinesecontent.eebbk.net/api/baseinfo/getEditionNameByShortName?editionName=%E4%BA%BA%E6%95%99%E7%89%88'
        result = requests.get(url)
        # print(result.text)
        assert 400 == result.status_code


def test_getBook():
    url = 'http://synchinesecontent.eebbk.net/api/book/getBook?bookName=%5B北京版%5D三年级数学上册'
    result = requests.get(url)
    # print(result.text)
    assert 200 == result.status_code


def test_getBaikeWords():
    url = 'http://test.eebbk.net/search-characterword-api/api/thirdparty/getBaikeWords'
    result = requests.get(url=url, params={'names': '玫瑰酒'})
    assert 200 == result.status_code


def test_num():
    a = 0.1
    b = 0.2
    c = 0.5
    d = 0.25

    print(a+b)
    print(c+d)
    print(b+b)
    print(1/5 + 1/10)
    print(1/5 + 1/5 )
    print(0.1+0.8)


def test_num1():
    assert 0.1 + 0.2 == approx(0.3)


if __name__ == '__main__':
    test_num()
