# @File  : cv2test.py
# @Author: LiuXingsheng
# @Date  : 2020/6/2
# @Desc  :

import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

Dirpath = r'\\DH106960\wholepics'


def jointpic(pic1, pic2, pic3):
    src = cv2.imread(os.path.join(Dirpath, pic1))
    src1 = cv2.imread(os.path.join(Dirpath, pic2))
    src2 = cv2.imread(os.path.join(Dirpath, pic3))
    # print(src.shape)
    # x,y = src.shape[0:2]
    src_test2 = cv2.resize(src, (0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_NEAREST)
    src_test3 = cv2.resize(src1, (0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_NEAREST)
    src_test4 = cv2.resize(src2, (0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_NEAREST)
    # 下述的6行无需添加，直接对缩放后的图片合并即可
    gray1 = Image.fromarray(cv2.cvtColor(src_test2, cv2.COLOR_BGR2RGB))
    gray2 = Image.fromarray(cv2.cvtColor(src_test3, cv2.COLOR_BGR2RGB))
    gray3 = Image.fromarray(cv2.cvtColor(src_test4, cv2.COLOR_BGR2RGB))
    img1 = cv2.cvtColor(np.asarray(gray1), cv2.COLOR_RGB2BGR)
    img2 = cv2.cvtColor(np.asarray(gray2), cv2.COLOR_RGB2BGR)
    img3 = cv2.cvtColor(np.asarray(gray3), cv2.COLOR_RGB2BGR)
    image = np.concatenate([img1, img2, img3], axis=1)
    cv2.imshow('input_image', image)


def getpics():
    machinelist = []
    piclist = []
    chosenlist = []
    files = os.listdir(Dirpath)
    for item in files:
        if item.endswith('.jpg') or item.endswith('bmp'):
            piclist.append(item)
    step = 3
    orderlist = [piclist[i:i + step] for i in range(0, len(piclist), step)]
    # for item in orderlist:
    #     chosenlist.append(random.choice(item))
    #     machinelist.append(str(item).split('_')[1])
    # print('机器序列号',len(machinelist),'去重后',len(list(set(machinelist))))
    # print(len(orderlist), orderlist)
    # os.mkdir(os.path.join(r'H:\wholepics','machine_withonepic'))
    # for chosen in chosenlist:
    #     shutil.move(os.path.join(r'H:\wholepics',chosen),os.path.join(r'H:\wholepics','machine_withonepic'))
    # return chosenlist
    # return piclist
    return orderlist


def showimage(piclist):
    notcertainlist = []
    ismarketlist = []
    notmarketlist = []
    num = len(piclist)
    for files in piclist:
        machineid = files[0].split('_')[1]
        jointpic(files[0], files[1], files[2])
        while True:
            key = cv2.waitKey()
            line = machineid
            if key == 49:  # 1是售点机器
                line += '---->' + '售点机器' + '\n'
                print(line)
                ismarketlist.append(machineid)
                break
            elif key == 50:  # 2 是非售点机器
                line += '---->' + '非售点机器' + '\n'
                print(line)
                notmarketlist.append(machineid)
                break
            elif key == 51:  # 3 暂时不能确认
                line += '---->' + '不能确定' + '\n'
                print(line)
                notcertainlist.append(machineid)
                break
            else:
                print('点击错误按键，数字键1--->售点机器,数字键2--->非售点机器,数字键3--->暂时不能确认')
        with open('marketlabel.txt', 'a') as fwrite:
            fwrite.write(line)
            fwrite.flush()
    print('一共有', num, '张图片', '售点标签准确率初步是', len(ismarketlist) / num)
    with open('marketlabel.txt', 'a') as fwrite:
        fwrite.write('售点标签准确率: ' + str(len(ismarketlist) / num))


def putText_chinese(img, text, position):
    img_PIL = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_PIL)

    font = ImageFont.truetype('simhei.ttf', 40, encoding='utf-8')
    fillColor = (255, 97, 0)

    # if not isinstance(text, unicode):
    #     text = text.decode('utf8')
    draw.text(position, text, font=font, fill=fillColor)
    img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img


def cvtestinterface():
    src = cv2.imread(r'H:\wholepics\test\PAAPhoto_70S3A9600BB9M_PAAPhoto20200101103305_1001_1149_1251_2448_3264.jpg')
    src1 = cv2.imread(r'H:\wholepics\test\PAAPhoto_70S3A9600BB9M_PAAPhoto20200104103354_1001_1180_2232_2448_3264.jpg')
    src_test2 = cv2.resize(src, (0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_NEAREST)
    src_test3 = cv2.resize(src1, (0, 0), fx=0.2, fy=0.2, interpolation=cv2.INTER_NEAREST)
    image = np.concatenate([src_test2, src_test3], axis=1)
    cv2.imshow('input_image', image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test():
    numlist = list(range(1, 10))
    print(numlist)
    listnum = [x for x in range(1, 10) if x % 2 == 0]
    print(listnum)


if __name__ == '__main__':
    # piclist = getpics()
    # showimage(piclist)
    # cvtestinterface()
    test()
