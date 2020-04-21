# @File  : testDomain.py
# @Author: LiuXingsheng
# @Date  : 2019/12/19
# @Desc  :
from InterfaceStructure import domainManager
from InterfaceStructure.resources import constants
import requests

manager = domainManager.DomainManager()
manager.setDomainType(constants.TestDomainType_Asia)
manager.setItemName(constants.askhomework)


def getHeader():
    return {'machineId': '700S593001B3V', 'deviceModel': 'S5', 'apkVersionName': '4.0.0.0.0',
            'apkVersionCode': '4000000',
            'apkPackageName': 'com.eebbk.aisearch.fingerstyle', 'accountId': '897', 'deviceOSVersion': 'V1.0.0_180409'}


def test_getResourcePackages():
    url = manager.getDomain() + '/app/search/other/getResourcePackages'
    result = requests.get(url=url, headers=getHeader())
    print(result.text)

def test():
    result = requests.get('http://test.eebbk.net/pointread-online-app/app/search/getSimilarEnglishBookById?bookId=653&devicemodel=V100')
    print(result.text)

def test_apli():
    print('hello world')



if __name__ == '__main__':
    # pytest.main(['-v','testDomain.py'])
    test()
