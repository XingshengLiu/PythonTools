# @File  : aisearch.py
# @Author: LiuXingsheng
# @Date  : 2020/1/10
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import aisearch_testUrlSet
import requests

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.aisearch)


def test_searchByOcrAndFile():
    url = manager.getDomain() + aisearch_testUrlSet.AisearchUrlSet['searchByOcrAndFile']
    print(url)
    param = {'zipType': 'none', 'xPoint': '367', 'yPoint': '217'}
    with open(r'C:\Users\Administrator\Desktop\P0用例\apisearchByOcrAndFile_P0级用例\FingerData3204791_0_367_217_2448_3264.jpg',
            'rb')as f:
        file = {'file': f.read()}
    result = requests.post(url=url, data=param, files=file)
    print(result.text)


def searchByOcrAndFile2():
    pass


if __name__ == '__main__':
    searchByOcrAndFile()
