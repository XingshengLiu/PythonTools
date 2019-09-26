# @File  : jsontest.py
# @Author: LiuXingsheng
# @Date  : 2019/1/15
# @Desc  :
import json


# py_dict = {'name': 'tone', 'age': '30', 'sex': 'true'}
# py_list = [1, 3]
# py_tuple = ('A', 'B', 'C')
#
# py_dict['a'] = py_list
# py_dict['b'] = py_tuple
#
# print(py_dict)
# print(type(py_dict))
#
# json_obj = json.dumps(py_dict)
# print(json_obj)
# print(type(json_obj))
#
# json_obj = json.dumps(py_dict, indent=4)
# print(json_obj)
#
# with open('data1.json', 'w')as f:
#     json.dump(py_dict, f)
#
# with open('data2.json', 'w')as f:
#     json.dump(py_dict, f, indent=4)


def getCount():
    count = 0
    with open('input.csv') as file:
        while file:
            line = file.readline()
            if 'banana' in line:
                count += 1
    return count


def getrever():
    test = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 11, 12, 13, 14, 15]
    print(test[-10:])




def getelement(arr):
    return arr[-10:]


def get3timeselment(arr):
    chosen = []
    for item in arr:
        if (arr % 3) == 0:
            chosen.append(item)
    return chosen


def getreversenumber(num):
    """
    假设num是一个-999-999之间的数字
    :param num:
    :return:
    """
    isPositive = True
    if num < 0:
        isPositive = False
        num = abs(num)
    if num >= 100:
        hund = num // 100
        ten = (num - hund * 100) // 10
        unit = num - hund * 00 - ten * 10
        newnum = unit * 100 + ten * 10 + hund * 1
    elif num >= 10:
        ten = num // 10
        unit = (num - ten * 10)
        newnum = unit * 10 + ten
    else:
        newnum = num

    if isPositive:
        return newnum
    else:
        return (0 - newnum)