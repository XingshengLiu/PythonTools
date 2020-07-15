# @File  : decotest.py
# @Author: LiuXingsheng
# @Date  : 2020/5/28
# @Desc  : 装饰器测试

from functools import wraps
import difflib
import collections
import time


def sumdeco(func):
    def wrapper_inner(*args, **kwargs):
        print(args)
        for item in range(len(args)):
            if args[item] < 0:
                print('is illegal')
            else:
                return func(*args, **kwargs)

    return wrapper_inner


@sumdeco
def getTwonumberSum(a, b):
    return a + b


class Student(object):
    __slots__ = ('_age', '_score')

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an interger or float')
        self._score = value


def test():
    (test, test1, test2) = range(3)
    print(test)
    print(test1)
    print(test2)


def meeting():
    sum = 0
    numlist = [0, 1, 2, -1, -3, 4]
    numlist.sort()
    length = len(numlist)
    for num in numlist:
        sum += num
    if sum % 3 == 0:
        partsum = sum / 3
        res = []

        def backtrack(i, tmp_sum, tmp_list):
            if tmp_sum == partsum:
                res.append(tmp_list)
                return
            for j in range(i, length):
                if tmp_sum + numlist[j] > partsum:
                    break
                if j > i and numlist[j] == numlist[j - 1]:
                    continue
                backtrack(j + 1, tmp_sum + numlist[j], tmp_list + [numlist[j]])

        backtrack(0, 0, [])
        print(res)
    else:
        return False


def test11():
    # nums = [1, 7, 3, 6, 5, 6]
    nums = [-1, -1, -1, -1, 0, -1, -1]
    total = sum(nums)
    part_sum = 0
    for i, j in enumerate(nums):
        if part_sum == (total - j) / 2:
            return i
        part_sum += j
    return -1


def test12():
    target = 7
    numlist = [2, 3, 4, 1]
    nmap = {}
    for i in range(len(numlist)):
        if target - numlist[i] in nmap:
            return i, nmap[target - numlist[i]]
        nmap[numlist[i]] = i


def test13():
    temp = []
    if temp:
        print(True)
    else:
        print(False)
    if temp is not None:
        print(True)
    else:
        print(False)


def merge1():
    intervals = [[1, 2], [3, 4], [0, 6]]
    if not intervals: return []
    intervals.sort()
    print(intervals)
    res = [intervals[0]]
    for x, y in intervals[1:]:
        print(res[-1][1])
        if res[-1][1] < x:
            res.append([x, y])
        else:
            res[-1][1] = max(y, res[-1][1])
    print(res)
    return res


def merge():
    intervals = [[1, 2], [3, 4]]
    # intervals = [[1, 4], [1, 4]]
    # intervals = [[1, 4], [2, 3]]
    # intervals = [[1, 4], [0, 1]]
    # intervals = [[1, 4], [3, 4]]
    # intervals = [[1,3],[2,6],[8,10],[15,18]]
    # intervals = [[1,4],[0,2],[3,5]]
    # intervals = [[1, 4], [0,5]]
    # intervals = [[0, 4], [3, 5]]
    intervals = [[4, 5], [1, 4], [0, 1]]
    # intervals = [[1, 2], [3, 4], [0, 6]]
    temp = []
    mergelist = []
    if len(intervals) == 1:
        return intervals
    intervals.sort()  # 需要想到先排序，排序后可以解决，下一个读取的区间可能大于已整理好的数据区间
    for i in range(len(intervals)):
        if temp:
            if temp[1] < intervals[i][0] or temp[0] > intervals[i][1]:  # 1<2 或 1>2 无重叠场景
                temp = [intervals[i][0], intervals[i][1]]
            elif temp[1] >= intervals[i][0] and temp[0] < intervals[i][0] and temp[1] < intervals[i][1]:  # 1<2 重叠场景
                temp = [temp[0], intervals[i][1]]
            elif intervals[i][1] >= temp[0] and intervals[i][0] < temp[0] and intervals[i][1] < temp[1]:  # 1 >2 重叠场景
                temp = [intervals[i][0], temp[1]]
            elif temp[0] >= intervals[i][0] and temp[1] <= intervals[i][1]:  # 2包含1
                temp = [intervals[i][0], intervals[i][1]]
            elif temp[0] <= intervals[i][0] and temp[1] >= intervals[i][1]:  # 1包含2
                temp = temp
            else:  # 1等于2
                temp = [intervals[i][0], intervals[i][1]]
        else:
            if i + 1 < len(intervals):
                if intervals[i][1] < intervals[i + 1][0] or intervals[i][0] > intervals[i + 1][1]:  # 1<2 或 1>2 无重叠场景
                    temp = [intervals[i][0], intervals[i][1]]
                elif intervals[i][1] >= intervals[i + 1][0] and intervals[i][0] < intervals[i + 1][0] and intervals[i][
                    1] < intervals[i + 1][1]:  # 1<2 重叠场景
                    temp = [intervals[i][0], intervals[i + 1][1]]
                elif intervals[i + 1][1] >= intervals[i][0] and intervals[i + 1][0] < intervals[i][0] and \
                        intervals[i + 1][1] < intervals[i][1]:  # 1 >2 重叠场景
                    temp = [intervals[i + 1][0], intervals[i][1]]
                elif intervals[i][0] >= intervals[i + 1][0] and intervals[i][1] <= intervals[i + 1][1]:  # 2包含1
                    temp = [intervals[i + 1][0], intervals[i + 1][1]]
                elif intervals[i][0] <= intervals[i + 1][0] and intervals[i][1] >= intervals[i + 1][1]:  # 1包含2
                    temp = [intervals[i][0], intervals[i][1]]
                else:  # 1等于2
                    temp = [intervals[i][0], intervals[i][1]]
            else:
                pass
        if temp in mergelist:
            pass
        else:
            if temp:
                print('temp-------', temp)
                mergelist.append(temp)
                if len(mergelist) > 1:
                    for item in mergelist:
                        if item[0] == temp[0]:
                            if item[1] >= temp[1]:
                                pass
                            else:
                                mergelist.remove(item)
                        else:
                            pass
                        if item[1] == temp[1]:
                            if item[0] <= temp[0]:
                                pass
                            else:
                                mergelist.remove(item)
                        else:
                            pass
                else:
                    pass
            else:
                mergelist.append(intervals[i])
    print(mergelist)
    return mergelist


def difftest():
    a = '刚强的柱石支撑起了百年不倒的大桥。'
    b1 = '刚强的柱石支撑起了百年不倒的大桥'
    b2 = '刚强的木纺支撑起了百年不倒的大木乔'
    b3 = '刚强的柱支撑起斥'
    print(difflib.SequenceMatcher(None, a, b1).quick_ratio())
    print(difflib.SequenceMatcher(None, a, b2).quick_ratio())
    print(difflib.SequenceMatcher(None, a, b3).quick_ratio())


def test_1():
    # intervals = [[1, 2], [3, 4]]
    # intervals = [[1, 4], [1, 4]]
    # intervals = [[1, 4], [2, 3]]
    # intervals = [[1, 4], [0, 1]]
    # intervals = [[1, 4], [3, 4]]
    # intervals = [[1,3],[2,6],[8,10],[15,18]]
    # intervals = [[1,4],[0,2],[3,5]]
    # intervals = [[1, 4], [0,5]]
    intervals = [[0, 4], [3, 5]]
    # intervals = [[4, 5], [1, 4], [0, 1]]
    # intervals = [[1, 2], [3, 4], [0, 6]]
    if not intervals: return []
    intervals.sort()
    res = [intervals[0]]
    for x, y in intervals[1:]:
        if res[-1][1] < x:
            res.append([x, y])
        else:
            res[-1][1] = max(y, res[-1][1])
    print(res)
    return res


def testdict():
    # adic = {'test':'1','test1':'2'}
    # print(adic['test'])
    # print(adic['test1'])
    testlist = [1, 2, 4]
    target = 3
    numdic = {}
    test111 = [0] * 12
    print(test111)
    print(test111[:])
    for i, num in enumerate(testlist):
        if numdic.get(target - num) is not None:
            print(i, numdic[target - num])
            return i, numdic[target - num]
        numdic[num] = i


def getdiagonallist():
    start = int(time.time())
    # matrix = [[3], [2]]
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    # matrix = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
    rowlength = len(matrix)
    columnlength = len(matrix[0])
    rowlabellist = [0 + i for i in range(columnlength)]
    columnlabellist = [j + columnlength - 1 for j in range(1, rowlength)]
    labellist = rowlabellist + columnlabellist
    alllist = []
    temp = []
    dic = {}
    for label in labellist:
        for num in range(rowlength):
            for item in range(columnlength):
                if dic.get(num + item):
                    dic[num + item].append(matrix[num][item])
                else:
                    dic[num + item] = [matrix[num][item]]
                if len(temp) < rowlength and (num + item) == label:
                    temp.append(matrix[num][item])
                    break
                if len(temp) == rowlength:
                    break
        alllist.append(temp)
        temp = []
    print(dic)
    for i in range(len(alllist)):
        if i % 2 == 0:
            alllist[i].reverse()
        else:
            pass
    onelist = []
    for i in range(len(alllist)):
        for j in alllist[i]:
            onelist.append(j)
    print(onelist)
    end = int(time.time())
    print('耗时', end - start)
    dic = {0: [1, 2, 3], 1: [2, 3, 4]}
    dic.update({0: 7})
    print('------------*************', dic)


def getdiagonallist_compare():
    start = int(time.time())
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    group = collections.defaultdict(list)
    for r, row in enumerate(matrix):
        for c, num in enumerate(row):
            sum = r + c
            group[sum].append(num)
    res = []
    for k, s in enumerate(group.values()):
        print(s)
        if k % 2 == 0:
            s.reverse()
        for p in s:
            res.append(p)
    print(res)
    end = int(time.time())
    print('耗时', end - start)


if __name__ == '__main__':
    # print(getTwonumberSum(-1, 2))
    # s = Student()
    # s.score = 10
    # s._age = 10

    # s.score = '-1'
    # s._score = '1'
    # print(s.score)
    # test()
    # meeting()
    # print(test12())
    # test13()
    # merge()
    # merge1()
    # difftest()
    # test_1()
    matrix = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    rowzerolist = []
    columnzerolist = []
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j] == 0:
                rowzerolist.append(i)
                columnzerolist.append(j)
            else:
                pass
    rowzerolist = list(set(rowzerolist))
    columnzerolist = list(set(columnzerolist))
    for i in range(len(matrix)):
        if i in rowzerolist:
            for j in range(len(matrix[i])):
                matrix[i][j] = 0
        else:
            for j in range(len(matrix[i])):
                if j in columnzerolist:
                    matrix[i][j] = 0
    # testdict()
    getdiagonallist()
    getdiagonallist_compare()
