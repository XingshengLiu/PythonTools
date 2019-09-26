# @File  : regcompiletest.py
# @Author: LiuXingsheng
# @Date  : 2019/1/12
# @Desc  :
import re

p = r'\w+@zhijieketang\.com'
regex = re.compile(p)

test = "Tony's emil is tony_guan588@zhijieketang.com"
m = regex.search(test)
print(m)

m = regex.match(test)
print(m)

p = r'[Jj]ava'
reg = re.compile(p)
text = 'I like Java and java.'

match_list = reg.findall(text)
print(match_list)

match_iter = reg.finditer(text)
for m in match_iter:
    print(m.group())

p = r'\d+'
regex = re.compile(p)
text = 'AB12CD34EF'
clist = regex.split(text)
print(clist)

repace_text = regex.sub(' ', text)
print('匹配的文档是：{0},类型是：{1}'.format(repace_text, type(repace_text)))

p = r'(java).*(python)'
regex = re.compile(p, re.IGNORECASE)
m = regex.search('I like Java and Python')
print(m)
m = regex.search('I like JAVA and PYTHON')
print(m)
m = regex.search('I like java and python')
print(m)
