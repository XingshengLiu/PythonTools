# @File  : createfile.py
# @Author: LiuXingsheng
# @Date  : 2021/1/12
# @Desc  : 创建指定大小文件

import os
import base64
import functools
import random

def test():
    name_dic = {}
    j = 1
    name_list = ['敖海波(20260289)','陈桂芬(20255233)','陈红(20263045)','陈可敏(20263038)','陈强(20262377)',
            '樊晓亚(20806071)','冯敏(20805739)','龚熙(20804849)','林静霞(20806023)','马思琴(20805416)','熊世平(20804098)',
            '杨明旭(20805972)','袁方(20262470)','张莉萍(20256865)','张伟强(20806009)','张宇健(20262789)']
    for i in range(len(name_list)):
        name_dic[i] = name_list[i]
    print('姓名序号(按企业微信群姓名顺序)',name_dic)
    numlist = random.sample(range(len(name_list)),len(name_list))
    print(numlist)
    for key in numlist:
        print('姓名',name_dic[key],'位序：',j)
        j += 1



def writecontent():
    with open(os.getcwd() + '\\' + 'b64_kousuanpics1.txt', 'a+', encoding='utf-8') as fwrite:
        with open(os.getcwd() + '\\' + 'PAAPhoto_70S5C9A00BF5U_PAAPhoto20200422174015_1001_1171_806_2448_3264', 'rb') as f:
            base64str = base64.b64encode(f.read())
            fwrite.write(str(base64str, encoding='utf-8') + ',' + '\n')
            fwrite.flush()



def wrappertest(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('decotext_1607.txt', 'a')as f:
            f.write('结果是' + str(result))
        return result
    return wrapper


class V():
    def __init__(self, radius):
        self.radius = radius

    @wrappertest
    def test(self):
        return pow(self.radius, 2) * 3.14

if __name__ == '__main__':
    # 循环写入次数，看着文件大小写
    # for i in range(20):
    #     writecontent()
    # v = V(2)
    # v.test()
    test()