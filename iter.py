# @File  : iter.py
# @Author: LiuXingsheng
# @Date  : 2019/2/19
# @Desc  :
from itertools import permutations

# a = ['a', 'b', 'c']
# a = 'abc'
# for p in permutations(a):
#     print(p)

class Item:
    cont = ''
    count = 0

def getStrCont():
    strTest = 'abca'
    content = set(strTest)
    maxcount = -1
    numberList = []
    for item in content:
        number = Item()
        number.count = strTest.count(item)
        number.cont = item
        numberList.append(number)
    for number in numberList:
        if number.count > maxcount:
            maxcount = number.count
    for number in numberList:
        if maxcount == number.count:
            print('出现次数最多的是：{0}, 对应的次数是：{1}'.format(number.cont,maxcount))


getStrCont()