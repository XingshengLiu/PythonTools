# @File  : wrongPicClassify.py
# @Author: LiuXingsheng
# @Date  : 2019/6/13
# @Desc  : 搜题错误图片筛选工具——修正可用


import shutil, os, xlrd


class WrongPicBean(object):
    picNum = ''
    picName = ''
    result = ''


def readExcelContent():
    contentbeanList = []
    filelist = os.listdir(r'G:\ocr2.0_pfmpic')
    for file in filelist:
        if file.endswith('.xlsx'):
            temp = file
            break
        else:
            continue
    data = xlrd.open_workbook(r'G:\ocr2.0_pfmpic' + '\\' + temp)
    sheet = data.sheets()[0]
    rows = sheet.nrows
    for row in range(1, rows):
        bean = WrongPicBean()
        bean.picNum = sheet.cell_value(row, 0)
        bean.picName = sheet.cell_value(row, 1)
        bean.result = sheet.cell_value(row, 2)
        contentbeanList.append(bean)
    return contentbeanList


def mkdkirNotExist():
    path = r'G:\ocr2.0_pfmpic' + '\\' + 'notExist'
    os.mkdir(path)
    return path


def main():
    path = mkdkirNotExist()
    wrongContentList = readExcelContent()
    for chosen in wrongContentList:
        shutil.move(r'G:\ocr2.0_pfmpic' + '\\' + str(chosen.picName), path)


if __name__ == '__main__':
    main()
