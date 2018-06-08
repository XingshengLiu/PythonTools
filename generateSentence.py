import sys, re


def getLocationAndSlide():
    # 词语#的#生字#另一个(发音|读音|拼音)(怎么|怎样|怎么样|咋样|咋|如何)读呢
    slide = []
    change = []
    normal = []
    ask = '#词语#的#生字#另一个(发音|读音|拼音)(怎么|怎样|怎么样|咋样|咋|如何)读呢'


def generateTest():
    p = re.compile(r"(?<=\[).+?(?=\])")
    p2 = re.compile(r"(?<=\().+?(?=\))")
    p3 = re.compile(r"#.*?#")
    s = u"#词语#[这个|那个]#词语字数#个(字|汉字)(怎么|咋|如何|怎样)写"
    s2 = u"春天"
    s3 = u'slide1 + 中括号1 + slide2 + normal + 小括号1 + 小括号2 + normal'
    lst = p.findall(s)
    lst2 = p2.findall(s)
    lst3 = p3.findall(s)
    bracketList = []
    curvesList = []
    print("词语槽结果：",lst3)
    for i in lst:
        bracketList.append(i.split("|"))
        # print(i)
    print('中括号结果：', bracketList)
    for i in lst2:
        curvesList.append(i.split("|"))
        # print(i)
    print('小括号结果：', curvesList)
    arr3 = []
    for i in bracketList:
        for k in i:
            arr3.append(s2 + str(k) + str(len(s2)) + "个")
    for num in range(2):
        length = len(arr3)
        for i in range(length):
            for j in curvesList[num]:
                arr3.append(arr3[i] + j)
        arr3 = arr3[length:]
    for i in range(len(arr3)):
        arr3[i] += "写"
    # for i in arr3:
    #     print(i)


def main():
    generateTest()


if __name__ == '__main__':
    main()
