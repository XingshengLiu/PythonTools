# @File  : english_pointread_online_api_testUrlSet.py
# @Author: LiuXingsheng
# @Date  : 2019/12/26
# @Desc  :

# swagger-ui:http://test.eebbk.net/english-pointread-online-api/swagger-ui.html

PointreadOnlineUrlset = {
    # 通过出版社获取书本列表
    'getBookByPublisher': '/api/oral/getBookByPublisher',
    # 获书本单元目录信息
    'getBookUnitsInfos': '/api/oral/getBookUnitsInfos',
    # 获取单元下所有Part列表
    'getPartInfoByBookUnit': '/api/oral/getPartInfoByBookUnit',
    # 获取出版社书本信息
    'getPublisherBooks': '/api/oral/getPublisherBooks',
    # 获取出版社列表
    'getPublishers': '/api/oral/getPublishers',
    # 智慧语音 早晚听 英语部分
    'getUnitVoiceInfo': '/api/book/getUnitVoiceInfo',
    # 根据书本id获取书本信息
    'getBookUnitInfoByBookId': '/api/book/getBookUnitInfoByBookId'}
