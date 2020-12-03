# @File  : weakknowledge_v3.py
# @Author: LiuXingsheng
# @Date  : 2020/11/25
# @Desc  :

import random
littleletterlist = ['k', 'j', 'i', 'h','g', 'f', 'e', 'd', 'c', 'b', 'a']

def generateMahineid(number):
    # 生成指定数量的序列号
    bigletterlist = []
    machineidlist = []
    numlist = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
    littleletterlist = ['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h',
                        'g', 'f', 'e', 'd', 'c', 'b', 'a']
    for letter in littleletterlist:
        bigletterlist.append(str.upper(letter))
    for i in range(number):
        machineidlist.append("".join(random.sample(littleletterlist + bigletterlist + numlist, 13)))
    return machineidlist

def generageRandomPoint():
    randomseed = random.randint(1,5)
    knowledgelist = random.sample(littleletterlist,randomseed)
    return knowledgelist

def generateRecord(machinelist,topiclist):
    for machine in machinelist:
        rightpointlist = []
        wrongpointlist = []
        exerciseseed = random.randint(10,19)
        rightpercent = random.randint(1,9)/10
        exercisenum = random.sample(topiclist,exerciseseed)
        length = len(exercisenum)
        rightlist = exercisenum[0:int(length*rightpercent)]
        wronglist = exercisenum[int(length*rightpercent):]
        for rightitem in rightlist:
            rightpointlist.append(rightitem[1])


if __name__ == '__main__':
    generageRandomPoint()
    rightpercent = random.randint(1, 9) / 10
    exercisenum = [1,2,3,4,5]
    rightlist = exercisenum[0:int(len(exercisenum) * rightpercent)]
    wronglist = exercisenum[int(len(exercisenum) * rightpercent):]
    print(rightlist, wronglist)