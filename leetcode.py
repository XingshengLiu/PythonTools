# @File  : leetcode.py
# @Author: LiuXingsheng
# @Date  : 2021/1/27
# @Desc  : 最长子串&最长回文子串

import math


# from airtest.core.android.android import Android
# from airtest.core.api import *


def getMaxSonStr(targetstr):
    numset = set()
    rightpointer, targetlength = -1, 0
    length = len(targetstr)
    for i in range(len(targetstr)):
        if 0 != i:
            numset.remove(targetstr[i - 1])
        while rightpointer + 1 < length and targetstr[rightpointer + 1] not in numset:
            numset.add(targetstr[rightpointer + 1])
            rightpointer += 1
        targetlength = max(rightpointer - i + 1, targetlength)
    print(targetlength)


def expandAroundCenter(s, left, right):
    while left >= 0 and right < len(s) and s[left] == s[right]:
        left -= 1
        right += 1
    return left + 1, right - 1


def longestPalindrome(s):
    start, end = 0, 0
    for i in range(len(s)):
        # 奇数长度的回文串（即中间一个字符是对称轴）
        left1, right1 = expandAroundCenter(s, i, i)
        # 偶数长度的回文串（即中间两个字符是对称轴）
        left2, right2 = expandAroundCenter(s, i, i + 1)
        if right1 - left1 > end - start:
            start, end = left1, right1
        if right2 - left2 > end - start:
            start, end = left2, right2
    # 按道理说，取start 和 end之间的字符就够了，这里+1，是因为python 字符串切片是按 左闭右开 取的，所以按照start:end 就只能取到end前一个字符，所以+1才能取到完整的回文串
    return s[start: end + 1]


def revers(x):
    res = -1 if x < 0 else 1
    res *= int(str(abs(x))[::-1])
    return res if -2 ** 31 <= res <= 2 ** 31 - 1 else 0


def revers_num1(x):
    rev = 0
    while x != 0:
        digit = x % 10
        print('+++++++++++++11111', digit)
        if x < 0 and digit > 0:
            print('+++++++++++++', digit)
            digit -= 10
            print('+++++++++++++', digit)
        x = (x - digit) // 10
        rev = rev * 10 + digit
        print('-------->', digit, x, rev)
    print(rev)


def query():
    numlist = [2, 3, 1]
    length = len(numlist)
    for i in range(length):
        for j in range(length):
            if numlist[i] > numlist[j]:
                numlist[i], numlist[j] = numlist[j], numlist[i]
    print(numlist)


def isPalindrome(x):
    if x < 0:
        return False
    revertednum = 0
    while x > revertednum:
        revertednum = revertednum * 10 + x % 10
        x = x // 10
    return x == revertednum or x == revertednum // 10


def maxArea():
    arealist = []
    numdic = {}
    numlist = [1, 2, 1]
    for location, value in enumerate(numlist):
        numdic[location] = value
    numdiclist = sorted(numdic.items(), key=lambda item: item[1], reverse=True)
    print(numdiclist)
    for item in numdiclist[1:]:
        arealist.append(abs(numdiclist[0][0] - item[0]) * item[1])
    print(max(arealist))


def maxarea():
    numlist = [1, 2, 1]
    left, right = 0, len(numlist) - 1
    ans = 0
    while left < right:
        temparea = min(numlist[left], numlist[right]) * (right - left)
        ans = max(temparea, ans)
        if numlist[left] <= numlist[right]:
            left += 1
        else:
            right -= 1
    print(ans)


def test_formal(num, formal):
    numlist = []
    while (num > 0):
        numlist.append(num % formal)
        num = num // formal
    numlist.reverse()
    print(numlist)


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class LinkedList:
    def __init__(self, head=None):
        self.head = head

    def append(self, newelement):
        current = self.head
        if self.head:
            while current.next:
                current = current.next
            current.next = newelement
        else:
            self.head = newelement

    def print_list(self):
        temp = self.head
        while temp is not None:
            print(temp.val)
            temp = temp.next

    def reverse_list(self):
        pre = None
        current = self.head

        while current is not None:
            nxt = current.next
            current.next = pre
            pre = current
            current = nxt
        self.head = pre

    def get_length(self):
        temp = self.head
        length = 0
        while temp is not None:
            length += 1
            temp = temp.next
        return length


def test(l1):
    sum = 0
    sum2 = 0
    for i in range(len(l1)):
        sum += l1[i] * 10 ** i
    print(sum)
    maxlength = len(l1) - 1
    for j in l1:
        sum2 += j * 10 ** maxlength
        maxlength = maxlength - 1
    print(sum2)


def splitnum(num):
    numlist = []
    while num:
        numlist.append(num % 10)
        num = num // 10
    print(102//10)
    print(numlist)

def twonums(numlist,taret):
    numdic = {}
    for i,num in enumerate(numlist):
        print('------>',i,num)
        if numdic.get(taret-num) is not None:
            return i,numdic[taret-num]
        numdic[num] = i

def midnum():
    l1 = [1,2,3]
    l2 = [4,5,6]
    l3 = l1 + l2
    sorted(l3)
    if len(l3)%2 == 0:
        return (l3[len(l3)//2-1] +l3[len(l3)//2])/2
    else:
        return l3[len(l3)//2]

def letterCombinations(digits):
    if not digits:
        return list()

    phoneMap = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    def backtrack(index):
        if index == len(digits):
            combinations.append("".join(combination))
        else:
            digit = digits[index]
            for letter in phoneMap[digit]:
                combination.append(letter)
                backtrack(index + 1)
                combination.pop()
    combination = list()
    combinations = list()
    backtrack(0)
    return combinations

if __name__ == '__main__':
    # getMaxSonStr('pwwkew')
    # print(longestPalindrome('cbbddbb'))
    # print(revers(123))
    # print(type(str(abs(123))[::-1]))
    # teststr = 'test'
    # print(teststr[::-1])
    # num = 456
    # st = str(num)
    # li = list(st)
    # print(li)
    # li.reverse()
    # print(int("".join(li)))
    # num = '123'
    # print(num.isnumeric())
    # query()
    # print(isPalindrome(12321))
    # maxarea()
    # test_formal(9, 2)
    # test_formal(4, 2)
    # revers_num1(-123)
    # headnode = ListNode(0)
    # list1 = LinkedList(headnode)
    # for i in range(1,6,2):
    #     list1.append(ListNode(i))
    # list1.print_list()
    # print('------------------->')
    # list1.reverse_list()
    # list1.print_list()
    # print(list1.get_length())
    # test([1, 2, 3])
    # splitnum(123)
    # print(type(twonums([1,2,3],3)))
    # print(midnum())
    print(letterCombinations("23"))
    for i in "abc":
        print(i)
    numlsit = list()
    numlsit.append(1)
    numlsit.append(2)
    print('1次打印',numlsit)
    numlsit.pop()
    print('2次打印',numlsit)
    numlsit.pop()
    print('3次打印',numlsit)