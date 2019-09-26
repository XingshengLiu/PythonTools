# @File  : copyfile.py
# @Author: LiuXingsheng
# @Date  : 2019/7/4
# @Desc  : 图片复制工具

import shutil,os


def copyFile():
    dest = r'\\172.28.1.23\ai数据素材\AI测试素材库\未标注素材\框题测试集'
    src = r'G:\框题测试集已处理_自研框题结果\wen1\\'

    with open('data.txt', 'r') as f:
        content = f.read()
        newcontent = content.replace('\n', '')
        picList = newcontent.split(',')
        print('length is :', len(picList))
        for item in picList:
            try:
                shutil.copy2(src + str(item), dest)
            except FileNotFoundError:
                print(str(item))
                pass



def main():
    copyFile()
    # test()


if __name__ == '__main__':
    main()
