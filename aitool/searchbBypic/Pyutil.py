# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     Pyutil
   Description :
   Author :       Administrator
   date：          2019/4/6
-------------------------------------------------
   Change Activity:
                   2019/4/6:
-------------------------------------------------
"""
__author__ = 'Administrator'

import xlrd
import sys,os
import cv2
import numpy as np
import re
import subprocess
from zhon.hanzi import characters
from zhon.hanzi import punctuation as han_pun
from string import punctuation as eng_pun
from zhon.hanzi import non_stops
from zhon.hanzi import stops






def travel_dir(path, extn='wav',recursive=True):
    """
    递归遍历文件夹中的后缀格式的文件
    :param path: 文件目录
    :param extn: 后缀名称不带点号
    :return:
    """
    if not os.path.isdir(path):
        print("please input correct dir name ! error path:", path)
        return
    path_name_list = []
    li = os.listdir(path)
    for p in li[:]:
        pathname = os.path.join(path, p)

        if os.path.isdir(pathname):
            if not recursive:
                continue
            li.remove(p)
            path_name_list.extend(travel_dir(pathname, extn,recursive))
        else:
            if p.split('.')[-1].find(extn) >= 0:
                li.remove(p)
                path_name_list.append(pathname)
                continue

    return path_name_list

def parse_excel_sheet_cols(xls_name,sheet_indx=0,col=(0,),row=(0,-1)):
    """
    提取excel某个表格的几列，和指定行数
    :param xls_name:  excel文件名
    :param sheet_indx: 第几张表
    :param col:  提取的列(0,)
    :param row:  提取的行数(beg,end)
    :return:
    """
    xlsfp=xlrd.open_workbook(xls_name)

    sheet_exls=xlsfp.sheet_by_index(sheet_indx)

    cols=[]
    for v in col:
        if row[1] !=-1:
            cols.append(sheet_exls.col_values(v)[row[0]:row[1]])
        else:
            cols.append(sheet_exls.col_values(v)[row[0]:])

    return cols

def rename_paths(paths,fmt='',dst=''):
    """
    重命名路径中的部分字符串，一般用作将绝对路径变为相对路径
    :param paths: 输入路径字符串
    :param fmt:
    :param dst:
    :return:
    """

    new_path=[]
    for f in paths:
        new_path.append(f.replace(fmt,dst))
    return new_path

def cv_imread(path):
    """
    opencv读取中文路径图片路径
    :param path:
    :return:
    """
    return cv2.imdecode(np.fromfile(path,dtype=np.uint8),cv2.IMREAD_COLOR)

def cv_imwrite(path,im):
    """
    opencv 保存图片
    :param path:
    :param im:
    :return:
    """
    file=os.path.split(path)
    cv2.imencode('.'+file[-1].split('.')[-1], im)[1].tofile(path)

def reverse_pic_mask(pic):
    """
    反色图片 dim=2 or 3
    :param pic:  输入图片 dim=2,3
    :return:
    """

    dim=len(pic.shape)

    if dim <2 or dim >3:
        print("picture date shape eror, dim not 2 or 3")
        sys.exit(-6)
    for row in range(pic.shape[0]):
        for col in range(pic.shape[1]):
            if dim ==3:
                for channel in range(pic.shape[2]):
                    pic[row,col,channel]=255-pic[row,col,channel]
            else:
                pic[row, col] = 255 - pic[row, col]
    return pic

def hasNumbers(inputString):
    """
    判断字符串是否有数字
    :param inputString:
    :return: True have number; Flase no Number
    """
    return bool(re.search(r'\d', inputString))

def find_number(imputs):
    return re.findall(r"\d+\.?\d*", imputs)

zh_pattern = re.compile(u'[\u4e00-\u9fa5]+')
def contain_zh(word):
    '''
    判断传入字符串是否包含中文
    :param word: 待判断字符串
    :return: True:包含中文  False:不包含中文
    '''

    global zh_pattern
    match = zh_pattern.search(word)

    return match

def findall_hanzi(sentens):
    """
    字符串中的汉字全部找出
    :param sentens:
    :return:
    """
    new_txt=re.findall('[{}]'.format(characters),sentens)
    return "".join(new_txt)

def findall_char_digi(sentence,mode=0):
    """
     0表示找出所有字母字符串 1表示找出英文字符串 2表示找出数字串
    :param sentence:
    :param mode: 0表示找出所有字母字符串 1表示找出英文字符串 2表示找出数字串
    :return:
    """
    if mode==0:
        partm='[a-zA-Z0-9]+'
    elif mode==1:
        partm = '[a-zA-Z]+'
    elif mode==2:
        partm = '[0-9]+'
    return re.findall(partm, sentence)

def strip_han_punchar(sentens,space=False,mode=0):
    """
    去除中文标点
    mode=0 表示去除所有中文标点
    mode=1 表示去除（除末尾句号类eg: ！。？）的中文标点
    mode=2 表示去除末尾句号类的中文标点
    :param sentens:
    :param space: True表示用空格代替中文标点 False表示直接去除中文标点
    :param mode: 0,1,2
    :return:
    """
    if space:
        spc=" "
    else:
        spc=""

    if mode==0:
        new_sentence=re.sub('[{}]'.format(han_pun),spc,sentens)
    elif mode==1:
        new_sentence=re.sub('[{}]'.format(non_stops),spc,sentens)
    elif mode==2:
        new_sentence = re.sub('[{}]'.format(stops), spc, sentens)
    else:
        return ""
    return new_sentence

def strip_eng_punchar(sentence,space=False):
    """
    处理英文标点
    :param sentence:
    :param space: False 去除英文标点，True 英文标点用空格代替
    :return:
    """
    if space:
        spc=" "
    else:
        spc=""
    return re.sub("[{}]".format(eng_pun),spc,sentence)

def strip_char_digi(sentence,mode=0):
    """
     0表示去除所有字母字符串 1表示去除英文字符串 2表示去除数字串
    :param sentence:
    :param mode: 0表示去除所有字母字符串 1表示去除英文字符串 2表示去除数字串
    :return:
    """

    if mode==0:
        partm='[a-zA-Z0-9]+'
    elif mode==1:
        partm = '[a-zA-Z]+'
    elif mode==2:
        partm = '[0-9]+'
    return re.sub(partm,"", sentence)

def splite_sentence(sentence):
    return re.split("[{}]".format(stops),sentence)

def ffmpeg(file_in,file_out,samprate=16000,log=True):
    """
    :param file_in:  输入文件名
    :param file_out: 输出文件名
    :param samprate:  采样率设置
    :param log: 是否打印完整的ffmpeg命令
    :return:
    """

    mpeg=r'E:\software\ffmpeg-latest-win64-static\bin\ffmpeg.exe'
    arg=' -i '+"\""+file_in+ "\""+' -ar '+str(samprate)+' '+"\""+file_out+"\""
    if log:
        print(mpeg+arg)
    subprocess.call((mpeg+arg))

def rename_suffix(dirs,old_suffix,new_suffix):
    """
    :param dirs:  需要修改后缀名称的目录
    :param old_suffix:  如果是“”表示需要修改的后缀文件名不限
    :param new_suffix: 新的后缀字符串，不能是“”，不带点号
    :return:
    """
    files=travel_dir(dirs,extn=old_suffix)
    for f in files:
        (path_name,file_name)= os.path.split(f)
        os.rename(f, path_name + '\\' +file_name+ "."+new_suffix)

def levenshtein(s1,s2):
    """
    求新的S2字符串和人工标注S1字符串的编辑距离
    :param s1:  ref string ground true
    :param s2:  new tring pred
    :return:  distence
    """

    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                 newDistances.append(1 + min((distances[index1], distances[index1+1], newDistances[-1])))
        distances = newDistances
    return distances[-1]/len(s1)


def corr_matrix(a,b):
    """
    求两个矩阵的相关系数,两个矩阵必须维度（维数，和度量）一致
    :param a: a.shape must equal to b.shape
    :param b:
    :return: a float number
    """
    assert a.shape==b.shape
    corr = np.sum((a - np.mean(a)) * (b - np.mean(b))) / np.sqrt(
        np.sum(np.square((a - np.mean(a)))) * np.sum(np.square((b - np.mean(b)))))
    return corr

def vad_eng_db(data,dbthr):

    eps = 0.000000001
    da_ = np.copy(data)
    data_np = np.array(da_)
    sum = np.sum(data_np * data_np)
    assert  data_np.shape[0] != 0
    sum_avg = np.sqrt(sum / data_np.shape[0])
    db = 20 * np.log10((sum_avg + eps) / 32767.0)
    if db < dbthr:
        return 0
    else:
        return 1



if __name__=='__main__':

    a='123asb12 2 3'
    b=find_number(a)
    print(b)

    sys.exit(-6)
    a = [2, 4, 6, 3, 3, 7]
    b = [5, 7, 1, 6, 8, 2]

    a = np.reshape(a, (2, 3))
    b = np.reshape(b, (2, 3))

    print(corr_matrix(a,b))


    txt="""‘,O人守三、读下面的材料.完成ar,习。(13分)折肆水土流失面积1万平方千米:丁找田水土漉失面积367万平方千米.约占全国面积的38弘.全国平均每坪六找田荒灌化土地面积已达262万平方千米,并且每年还以216O平方千米的匹度寸:.圹枣 -全国已有.三=草」也退化*沙化和监碱化【以下简称“三化”)面积连年增加。化"乒」也面积,. 35亿公顷.约占草地面积的1/3.」十且每年还在以zoo万公顷竚廸戌增加 .L从以上材料中你j孕剑了哪些」n息?13分 )试峩国己有]5% -20%的动植物种类受到威胁.高于世界10%-13:%的平均水平。一一一一一一一一一一一一一一一一一一一一一一一一一一一一了萨//一一一一一一一一一一一一一一一.':-.].结合自己平时的观察和走访、了解.说说造成这些现象的原因。【4分)子P<’是啊.所有降临到地球身上的一一切终将会降临在我们人类自己的身上!如髡地球茁破坏J' .我们将別无去处!保护地球.就是[呈护我们人类自己啊'. TA'为保护地球母亲提出你的建议和意见吧! (6分)::我的建议、意见: 一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一一丁一一一.一一一一一一一一一一一一一一一一一一一一一
.f..\dot{\cdot}--..、UL_{i\overrightarrow{h}}..\Lambda^{*}\cdot\pm_{h}\infty_{-}J\|_{L}\cdot,=1=y./-l.-\cdot*\Lambda*h.\cdot.*...h〃./..\dot{.},r..e^{-}/F[仳、\/......,..*.ty...i.▱..-谳-r:如"..、、I.f...*...一←⊂⊇.IJ./-.,垂...--4⊂.'{\dot{\pm_{*}}}^{1}.\dot{\cdot}\dot{,}.hhh.么-=.IJlu-^.*t忡"Et鲁、咯
~上.".t'叩帆蚝S‘ .-.I卢.r.'<'.∽八J,-,-.o:尸.町一Ni.吣占。示y一九1覓.lq.氕q【弘..、屺.….十住,一’.--.' .:.【-』-,.J f'.嘍【,」-直.丁.i‘匝.一.。.,.…、卉矿一。q_唾NJ-.. *吓,A*.铲昂E…1m*』.,q、,A旺」,』怔='ll一一.'..' .A .守.O,';*,1兜M也叨匝O匕虬..一≃⋱- l 'iJ 弗vv i- wJ  I' -f- . ,rr, tI  "',*t, '+ :r  , A .;: .L .J.- . ,,, A_ 【 ,. u_ A -, N..   j_'tt.,A仁..'】1 “「吧议】”心0 .T丁止几丸,r, .冉丸,:rn丸虹‘:'巳叱斗i”「,:昏咀..n ,【立.t'IAI疋压.rcr, .此是㈧pj吐员'n眄几云.ry.n_:耳人夕_ -r .,而-'L-:h缸u_ b:】,,-,:>心啶“J -一O」.疋啣=皿”"J m va-.公』*J; .-r+t它们..而JL只有吐m qnⅧ.'X古怔凡匹.-」 .岬】 -'J逼Ⅱ毫凹**J-』 ")'\工有一托扨牛一凡司恤,n术m屯石.书战凡阳儿.青-rf-时;矿里饥肌4'L T 艋k_ .,.IT’L必项帕A"A- ,还你一」l叨心帕亞丸15.门÷内什么-怔椰LE括灭去-「色彩-?[2分)J』:川m姓给青年僻除苦吨n<J.方法;wtt'么? (z分1」.涧IZ短文后,你受到了什么启监7 ( 2.分)∓列过Z吗?你是样酃畏呢’试羞写二乌「。 L3分)‘i .粱(
语形容他们吗?.  中有许多能言善辩的人.你能用成明明说:巧舌如簧 口若悬河我来说:2.请你展示描写人物神态的成语b例如:呆若木鸡 目瞪口呆我来说:3.我能用许多词语来表达我对科学精裤的认识.如:实事求是、一丝不苟。我来说:"""
    new_txt=re.findall('[{}]'.format(characters),txt)
    xx="".join(new_txt)
    print(xx)

    new_txt1=strip_han_punchar(txt,True)
    new_txt2=strip_eng_punchar(new_txt1,True)
    new_txt3=re.findall('[a-zA-Z0-9]+',new_txt2)

    xx="第1题。说一说1厘米、1平方厘米、1立方厘米分别是用来计量什么量的单位，它们有什么不同。1厘米是计量长度的单位；1平方厘米是计量面积的单位；1立方厘米是计量体积的单位。1厘米计量的是一段线段的长度；1平方厘米计量的是一个物体放在地面上占多大面积；1立方厘米是计量一个物体所占空间的大小。同学们，你做对了吗？加油哦！"
    xx1=splite_sentence(xx)
    print()