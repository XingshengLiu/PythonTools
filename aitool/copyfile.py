# @File  : copyfile.py
# @Author: LiuXingsheng
# @Date  : 2019/7/4
# @Desc  : 图片复制工具

import shutil, os
import xlsxwriter
import xlrd

dirpath = r'C:\Users\Administrator\Desktop'


def getpics():
    pics = []
    contentdata = xlrd.open_workbook(os.path.join(dirpath, '8月英语.xlsx'))
    sheet = contentdata.sheets()[0]
    rows = sheet.nrows
    for row in range(rows):
        pics.append(sheet.cell_value(row, 1))
    return pics


def copyFile(picList):
    dest = r'E:\PyGitHub\oyqt5\accsearch\src\索引优化前_8月_20210218\英语'
    src = r'E:\PyGitHub\oyqt5\accsearch\src\索引优化前_8月_20210218'

    # with open('data.txt', 'r') as f:
    #     content = f.read()
    #     newcontent = content.replace('\n', '')
    #     picList = newcontent.split(',')
    #     print('length is :', len(picList))
    for item in picList:
        try:
            # shutil.copy2(os.path.join(src, str(item)), dest)
            shutil.move(os.path.join(src, str(item)), dest)
        except FileNotFoundError:
            print(str(item))
            pass


def renametest():
    path = r'H:\内容中台\retest'
    filelist = [['1.txt', '001.txt'], ['2.txt', '002.txt'], ['3.txt', '003.txt']]
    for file in filelist:
        os.rename(os.path.join(path, file[0]), os.path.join(path, file[1]))


def writecontent(DirPath, filename, completelist):
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, filename + '.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(completelist)):
        for column in range(len(completelist[row])):
            ws.write(row, column, completelist[row][column])
    workbook.close()


def main():
    picslist = getpics()
    copyFile(picslist)
    # renametest()


if __name__ == '__main__':
    main()
