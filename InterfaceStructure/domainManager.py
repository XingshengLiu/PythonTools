# @File  : domainManager.py
# @Author: LiuXingsheng
# @Date  : 2019/12/19
# @Desc  :

from InterfaceStructure.resources import constants


class DomainManager():
    def setDomainType(self, domainType):
        self.domainType = domainType

    def getDomainType(self):
        return self.domainType

    def setItemName(self, item):
        self.item = item

    def getItemName(self):
        return self.item

    def getDomain(self):
        if self.getDomainType() == constants.TestDomainType_Asia:
            return constants.TestDomain + self.getItemName()
        elif self.getDomainType() == constants.TestDomainType_Ali:
            return constants.TestDomainAli + self.getItemName()
        elif self.getDomainType() == constants.AlphaDomainType:
            return constants.AlphaDomain + self.getItemName()
        else:
            return constants.FormalDomainDic[self.getItemName()]
