# @File  : syn-chinese-api_test.py
# @Author: LiuXingsheng
# @Date  : 2020/3/25
# @Desc  :

import requests

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import syn_chinese_api_testUrlSet

manager = domainManager.DomainManager()
manager.setDomainType(constants.FormalDomainType)
manager.setItemName(constants.syn_chinese_api)


def searchSyncWordByWord():
    url = manager.getDomain() + syn_chinese_api_testUrlSet.SynChineseApi['searchSyncWordByWord']
    print(url)
    machineid = '700S593001AE5'
    paramlist = [{'searchWord': '率领', 'machineId': machineid}, {'searchWord': '挣扎', 'machineId': machineid},
                 {'searchWord': '露水', 'machineId': machineid}, {'searchWord': '首都', 'machineId': machineid}]
    for param in paramlist:
        result = requests.get(url=url, params=param)
        print(result.text)


if __name__ == '__main__':
    searchSyncWordByWord()
