# @File  : FornulaBean.py
# @Author: LiuXingsheng
# @Date  : 2019/6/25
# @Desc  :

class PicWithNoScene(object):
    picname = ''
    trueText = ''
    recogText = ''
    result = ''
    suject = ''
    scene = ''

    def __init__(self, picname, trueText, recogText, result):
        self.picname = picname
        self.trueText = trueText
        self.recogText = recogText
        self.result = result


class PicWithScene(object):
    suject = ''
    scene = ''
    picname = ''

    def __init__(self, suject, scene, picname):
        self.suject = suject
        self.scene = scene
        self.picname = picname


class CompletePic(object):
    picname = ''
    trueText = ''
    recogText = ''
    result = ''
    suject = ''
    scene = ''

    def __init__(self, picname, trueText, recogText, result, suject, scene):
        self.picname = picname
        self.trueText = trueText
        self.recogText = recogText
        self.result = result
        self.suject = suject
        self.scene = scene
