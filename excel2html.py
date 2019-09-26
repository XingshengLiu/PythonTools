# @File  : excel2html.py
# @Author: LiuXingsheng
# @Date  : 2019/9/17
# @Desc  : excel转为html

import codecs
import pandas as pd

xd = pd.ExcelFile('点播测试结果.xlsx')
pd.set_option('display.max_colwidth', 1000)
df = xd.parse()
with codecs.open('test.html', 'w')as html_file:
    html_file.write(df.to_html(header=True, index=False))
