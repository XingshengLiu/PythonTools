# @File  : ApkObject.py
# @Author: LiuXingsheng
# @Date  : 2019/8/6
# @Desc  :

class ApkObject(object):
    origianlApkName = ''
    searchApkName = ''
    result = ''

    def __init__(self, originalApkName, searchApkname, result):
        self.origianlApkName = originalApkName
        self.searchApkName = searchApkname
        self.result = result
