# @File  : writedownContent.py
# @Author: LiuXingsheng
# @Date  : 2019/8/16
# @Desc  :
import os,base64

def getAllPic():
    picList = []
    filelist = os.listdir(r'\\172.28.1.23\ai数据素材\AI测试素材库\未标注素材\准备标注素材\中文\表格')
    for file in filelist:
        if file.endswith('.bmp'):
            picList.append(file)
        else:
            pass
    for item in picList:
        with open(item, "rb") as img_file:
            img_data = img_file.read()
        img_data = base64.b64encode(img_data)
