# @File  : calcuvolume.py
# @Author: LiuXingsheng
# @Date  : 2020/5/27
# @Desc  :

import math
from collections import namedtuple

FomralType = [float,int]

class Cylinder():
    radius = 0
    height = 0

    def __init__(self, radius, height):
        if str(type(radius)) in str(FomralType) and str(type(height)) in str(FomralType) and radius > 0 and height > 0:
            self.radius = radius
            self.height = height
        else:
            print('invalid radius or height')
            return

    def judgeinvalid(self):
        if self.getRadius() == 0 or self.getHeight() == 0:
            return True
        else:
            return False

    def getRadius(self):
        return self.radius

    def getHeight(self):
        return self.height

    def getArea(self):
        if self.judgeinvalid():
            return 'invalid paramter'
        else:
            return math.pow(self.radius, 2) * math.pi

    def getVolume(self):
        if self.judgeinvalid():
            return 'invalid paramter'
        else:
            return self.getArea() * self.height


class Deco():
    def getVolume(self):
        pass

class CylinderDeco(Deco):
    def __init__(self, cylinder, logpath):
        self.cylinder = cylinder
        if logpath:
            self.logpath = logpath
        else:
            print('log path is null')

    def getVolume(self):
        volumn = self.cylinder.getVolume()
        content = 'radius is {0} height is {1} volumn is {2}\n'.format \
            (self.cylinder.getRadius(), self.cylinder.getHeight(), volumn)
        with open(self.logpath, 'a+', encoding='utf-8') as fwrite:
            fwrite.write(content)


class TestDemo():

    def __init__(self, cylinder, reportpath):
        self.cylinder = cylinder
        if reportpath:
            self.reportpath = reportpath
        else:
            print('reportpath path is null')

    def judgeresult(self, calcuresult, expectresult):
        if 'invalid' in str(calcuresult):
            return 'invalid paramter'
        if calcuresult == expectresult:
            return True
        else:
            return False

    def test_getArea(self):
        calcuresult = self.cylinder.getArea()
        expectresult = math.pow(self.cylinder.getRadius(), 2) * math.pi
        return self.judgeresult(calcuresult, expectresult)

    def test_getVolumn(self):
        calcuresult = self.cylinder.getVolume()
        expectresult = math.pow(self.cylinder.getRadius(), 2) * math.pi * self.cylinder.getHeight()
        return self.judgeresult(calcuresult, expectresult)

    def generatereport(self):
        resultArea = self.test_getArea()
        resultVolumn = self.test_getVolumn()
        title = 'radius\theight\tareaResult\tvolumnResult\n'
        content = '{0}\t{1}\t{2}\t{3}\n'.format(self.cylinder.getRadius(), self.cylinder.getHeight(), resultArea,
                                                resultVolumn)
        with open(self.reportpath, 'a+', encoding='utf-8') as fwrite:
            fwrite.write(title + content)


if __name__ == '__main__':
    paramlist = [Cylinder(-1,1),Cylinder(1,-1),Cylinder(1,0),Cylinder(0,0),Cylinder(0,1),Cylinder('1',1),Cylinder([],[]),Cylinder((),[])
                 ,Cylinder(1.1,2.2),Cylinder(100000000.2,4561231124578456.3)]
    for param in paramlist:
        cydeco = CylinderDeco(param, 'log.log')
        cydeco.getVolume()
        tstdemo = TestDemo(param, 'result.log')
        tstdemo.generatereport()



