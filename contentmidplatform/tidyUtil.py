# @File  : tidyUtil.py
# @Author: LiuXingsheng
# @Date  : 2020/10/28
# @Desc  : 对月报数据进行整理时使用的工具类
import os
import xlrd
import decryptorUtil

def wrapper(strlist, strindex):
    """
    6月标注Id 标准不全，需要根据第几屏命中去反查qusiotnid内容进行标注
    :param strlist:
    :param strindex:
    :return:
    """
    correctlist = []
    quesiontlist = strlist[:-1].split(';')
    if strindex.endswith(','):
        indexlist = strindex[:-1].split(',')
    else:
        indexlist = strindex.split(',')
    decodequesiontlist = [quesiontlist[0]] + decryptorUtil.decryption_Qids(quesiontlist[1:])
    for inx in indexlist:
        correctlist.append(decodequesiontlist[int(inx) - 1])
    decryptorUtil.shutdownJVM()
    return correctlist

def wrapper_simple(strlist):
    """
    答案标准很全，questionId都已经列在里边了
    :param strlist:
    :return:
    """
    signlist = []
    if ';' in str(strlist):
        encodelist = strlist.split(';')
    else:
        signlist.append(str(int(strlist)))
        return signlist
    for quesitonId in encodelist:
        if '=' in quesitonId and quesitonId != '':
            decodeid = decryptorUtil.decryption_Qid(quesitonId)
            signlist.append(str(decodeid))
        else:
            if quesitonId != '':
                signlist.append(str(quesitonId))
            else:
                pass
    return signlist

def readExcel():
    filepath = os.path.join(r'H:\内容中台\精准搜题项目\测试集\作业工具月报测试集', '11月标注Id.xlsx')
    contentdata = xlrd.open_workbook(filepath)
    sheet = contentdata.sheets()[1]
    rows = sheet.nrows
    for row in range(1, rows):
        # print(sheet.cell_value(row,0))
        # print(wrapper(sheet.cell_value(row, 0), sheet.cell_value(row, 1)))
        print(wrapper_simple(sheet.cell_value(row, 2)))

if __name__ == '__main__':
    # ids = [
    #     "DAO6lzuE494k0p34g96CKg==",
    #     "S7y30sB5NYjeIV6oH/cVXA==",
    #     "Fs42GRPe0oZ8f4viy1e2hg==",
    #     "44Q0Jh6MbuXlG1h6b/wjBQ=="
    # ]
    # print(decryptorUtil.decryption_Qids(ids))
    readExcel()
    decryptorUtil.releaseJVM()