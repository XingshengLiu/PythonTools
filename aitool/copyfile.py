# @File  : copyfile.py
# @Author: LiuXingsheng
# @Date  : 2019/7/4
# @Desc  : 图片复制工具

import shutil,os
import xlrd
dirpath = r'H:\内容中台\精准搜题项目\测试集\作业工具月报测试集\opensearch'
def getpics():
    pics = []
    contentdata = xlrd.open_workbook(os.path.join(dirpath, '搜题错误.xlsx'))
    sheet = contentdata.sheets()[0]
    rows = sheet.nrows
    for row in range(rows):
        pics.append(sheet.cell_value(row, 1))
    return pics

def copyFile(picList):
    dest = r'H:\内容中台\精准搜题项目\测试集\作业工具月报测试集\opensearch'
    src = r'\\172.28.2.84\kf2share1\AIData\业务全链路\智慧小布\全链路-点问搜题\7月\粗框图'

    # with open('data.txt', 'r') as f:
    #     content = f.read()
    #     newcontent = content.replace('\n', '')
    #     picList = newcontent.split(',')
    #     print('length is :', len(picList))
    for item in picList:
        try:
            shutil.copy2(os.path.join(src,str(item)), dest)
            # shutil.move(os.path.join(src, str(item)), dest)
        except FileNotFoundError:
            print(str(item))
            pass

def renametest():
    path = r'H:\内容中台\retest'
    filelist = [['1.txt','001.txt'],['2.txt','002.txt'],['3.txt','003.txt']]
    for file in filelist:
        os.rename(os.path.join(path,file[0]),os.path.join(path,file[1]))

def main():
    picslist = getpics()
    copyFile(picslist)
    # renametest()



if __name__ == '__main__':
    main()
