# @File  : weather_pad_test.py
# @Author: LiuXingsheng
# @Date  : 2020/4/7
# @Desc  :

from InterfaceStructure.resources import constants
from InterfaceStructure import domainManager
from InterfaceStructure.resources import weather_pad_testUrlSet
import requests
import demjson

manager = domainManager.DomainManager()
manager.setDomainType(constants.TestDomainType_Asia)
manager.setItemName(constants.weather_pad)


def hotCities():
    chinacitylist = []
    internationallist = []
    citynamelist = []
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['hotCities']
    print(url)
    result = requests.get(url=url)
    objdata = demjson.decode(result.text)
    if objdata['data']:
        if objdata['data']['hotCities'] and objdata['data']['hotCitiesInternational']:
            for chinaitem in objdata['data']['hotCities']:
                chinacitylist.append(chinaitem['locationKey'])
                citynamelist.append(chinaitem['cityName'])
            for nationitem in objdata['data']['hotCitiesInternational']:
                internationallist.append(nationitem['locationKey'])
                citynamelist.append(nationitem['cityName'])
    else:
        print('请求有误')
    return chinacitylist, internationallist, citynamelist


def search(citynamelist):
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['search']
    print(url)
    for city in citynamelist:
        result = requests.get(url=url, params={'cityName': city})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            print(objdata['data'])
        else:
            print(city, '数据为空')


def geo():
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['geo']
    print(url)
    ordinateList = [('47.663', '128.829'), ('38.435', '106.288'), ('22.539', '114.089')]
    for ordinate in ordinateList:
        result = requests.get(url=url, params={'latitude': ordinate[0], 'longitude': ordinate[1]})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            for item in objdata['data']:
                if item['name'] and item['parentCityName'] and item['adminName'] and item['countryName'] and \
                        item['rank'] and item['locationKey']:
                    print(objdata['data'])
                else:
                    print('数据为空')


def HoursForecast(chinacitylist):
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['24HoursForecast']
    print(url)
    for city in chinacitylist:
        result = requests.get(url=url, params={'locationKey': city})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            for hour in objdata['data']:
                if hour['weatherText']:
                    pass
                else:
                    print('有数据为空')


def daysForecast(chinacitylist):
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['7daysForecast']
    print(url)
    for city in chinacitylist:
        result = requests.get(url=url, params={'locationKey': city})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            pass
        else:
            print('7天数据为空')


def batch(chinacitylist):
    params = ''
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['batch']
    print(url)
    param = str(chinacitylist).replace('[', '').replace(']', '').replace(' ', '')
    print(param)
    result = requests.get(url=url, params={'locationKeys': param})
    print(result.text)
    objdata = demjson.decode(result.text)
    if objdata['data']:
        if len(objdata['data']) == len(chinacitylist):
            print('获取天气数量和传入数量一致')
        else:
            print('天气数据量和传入不一致')


def today(chinacitylist):
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['today']
    print(url)
    for city in chinacitylist:
        result = requests.get(url=url, params={'locationKey': city})
        objdata = demjson.decode(result.text)
        if objdata['data']:
            pass
        else:
            print('今日数据为空')


def todaySuggestion(chinacitylist):
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['todaySuggestion']
    print(url)
    for city in chinacitylist:
        result = requests.get(url=url, params={'locationKey': city})
        print(result.text)
        objdata = demjson.decode(result.text)
        if 'data' in objdata and objdata['data']:
            pass
        else:
            print('今日建议为空')


def warning(chinacitylist):
    url = manager.getDomain() + weather_pad_testUrlSet.WeatherPadUrlSet['warning']
    print(url)
    for city in chinacitylist:
        result = requests.get(url=url, params={'locationKey': city})
        objdata = demjson.decode(result.text)
        print(objdata)


if __name__ == '__main__':
    chinacitylist, internationallist, citynamelist = hotCities()
    search(citynamelist)
    geo()
    HoursForecast(internationallist)
    daysForecast(internationallist)
    batch(internationallist)
    today(internationallist)
    todaySuggestion(internationallist)
    warning(internationallist)
