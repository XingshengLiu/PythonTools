# @File  : data_platform_hotvideo.py
# @Author: LiuXingsheng
# @Date  : 2020/6/18
# @Desc  :
import xlrd
import xlsxwriter
from scipy.stats import norm
import math


def wilson_and_imdb_hot(posR, posN, n, r, confidence):
    """
    计算威尔逊置信度下限值
    :param posR: 近期点赞量
    :param posN: 总点赞数
    :param n: 总播放量
    :param r: 近期播放量
    :return: 热度值
    :param confidence: 置信度水平，该值的区间为[0,1]
    """
    wr = posN / (posN + posR) * 0.3 + posR / (posN + posR) * 0.7
    if n == 0:
        return 0
    else:
        """
            1、z：表示对应置信度水平confidence下的正态分布统计量；
            2、confidence：解决冷启动问题，避免因新视频上架时间短，用户点击量少导致的评分不公正问题。
            3、缺点是排行榜前列总是那些票数最多的项目，新项目或者冷门的项目，很难有出头机会，排名可能会长期靠后。因此分别计算了长期热度和短期热度，再将长短期热度值相加，得到最终热度。
            4、未来考虑加入时间因子权重。暂时没有加。    stan        
        """
        z = norm.cdf(1 - (1 - confidence) / 2)
    phatN = 1.0 * posN / n
    phatR = 1.0 * posR / r
    hotN = (phatN + z * z / (2 * n) - z * math.sqrt((phatN * (1 - phatN) + z * z / (4 * n)) / n)) / (1 + z * z / n)
    hotR = (phatR + z * z / (2 * n) - z * math.sqrt((phatR * (1 - phatR) + z * z / (4 * n)) / n)) / (1 + z * z / n)
    hot = pow((hotN + hotR), 0.8) * wr
    # print("hot:", hot, "wr:", wr)
    return hot


if __name__ == '__main__':
    alllist = []
    typelist = []
    workbook = xlrd.open_workbook(r'C:\Users\Administrator\Desktop\【短视频推荐】构造测试数据.xlsx')
    sheets = workbook.sheets()
    for sheet in sheets:
        rows = sheet.nrows
        for row in range(1, rows):
            hotvalue = wilson_and_imdb_hot(int(sheet.cell_value(row, 0)), int(sheet.cell_value(row, 1)),
                                           int(sheet.cell_value(row, 2)),
                                           int(sheet.cell_value(row, 3)), 0.9)
            typelist.append(
                (int(sheet.cell_value(row, 0)), int(sheet.cell_value(row, 1)), int(sheet.cell_value(row, 2)),
                 int(sheet.cell_value(row, 3)), hotvalue))
        alllist.append(typelist)
        typelist = []
    titlelist = [[('近期点赞数', '总点赞数', '总点击量', '近期播放量','热度值')]]
    workbook = xlsxwriter.Workbook(r'C:\Users\Administrator\Desktop\【短视频推荐】构造测试数据_热度值.xlsx')
    for tp in range(len(alllist)):
        ws = workbook.add_worksheet('sheet' + str(tp))
        for row in range(len(alllist[tp])):
            for column in range(len(alllist[tp][row])):
                ws.write(row, column, alllist[tp][row][column])
    workbook.close()
