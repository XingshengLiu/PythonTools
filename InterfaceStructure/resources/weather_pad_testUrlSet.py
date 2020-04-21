# @File  : weather_pad_testUrlSet.py
# @Author: LiuXingsheng
# @Date  : 2020/4/7
# @Desc  :

WeatherPadUrlSet = {
    # ---------------城市相关接口-----------------------
    # 获取热门城市
    'hotCities': '/city/hotCities',
    # 城市搜索(关键字搜索)
    'search': '/city/search',
    # 城市搜索(经纬度)
    'geo': '/city/search/geo',
    # -------------天气相关接口------------------------
    # 获取24小时预报
    '24HoursForecast': '/weather/24HoursForecast',
    # 获取逐日预报
    '7daysForecast': '/weather/7daysForecast',
    # 批量获取多个城市的实况
    'batch': '/weather/current/batch',
    #  今日总览+今日天气详情
    'today': '/weather/today',
    # 获取今日建议
    'todaySuggestion': '/weather/todaySuggestion',
    # 天气预警
    'warning': '/weather/warning'
}
