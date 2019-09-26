# @File  : EnglishBean.py
# @Author: LiuXingsheng
# @Date  : 2019/9/20
# @Desc  :

class OcrEngBean(object):

    def __init__(self, picName, labelText, ZY, YD, HW, ZYresut, YDresult, HWresult, type):
        self.picName = picName
        self.labelText = labelText
        self.ZY = ZY
        self.YD = YD
        self.HW = HW
        self.ZYresut = ZYresut
        self.YDresult = YDresult
        self.HWresult = HWresult
        self.type = type


class EngType(object):

    def __init__(self, picName, type):
        self.picName = picName
        self.type = type
