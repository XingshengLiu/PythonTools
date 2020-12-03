# @File  : learningprocessLabel.py
# @Author: LiuXingsheng
# @Date  : 2020/5/10
# @Desc  : 完整的习题对应关系的数据用户做题记录生成脚本
import os
import random
import csv
import xlrd
import demjson
import xlsxwriter

MultiDirPath = r'C:\Users\Administrator\Desktop\quesitonid对应关系\正则匹配一个questionId对应多个知识点'
SingleDirPath = r'C:\Users\Administrator\Desktop\quesitonid对应关系\精准匹配一个questionId对应一个知识点'
DirPath = r'C:\Users\Administrator\Desktop\quesitonid对应关系\构造测试集'
DirPath_v2 = r'C:\Users\Administrator\Desktop'
# 内容V2.0 版本 Z计划个人学习进度复测路径
DirPath_v2_content = r'C:\Users\Administrator\Desktop\quesitonid对应关系\Z计划整机学习进度_构造测试集'
# 给定某个区间段的上限 如获取40~50区间内的随机题目数量，设置为50
EXPECTED_SEED = 10
GroupNum = 3
originallist = [(1, 2, 1369, 1), (1, 2, 1489, 2), (1, 2, 1489, 3), (1, 2, 1411, 4), (1, 3, 1389, 5), (1, 3, 1449, 6),
                (1, 4, 2289, 7), (2, 1, 1569, 10), (2, 1, 13369, 11), (2, 1, 1569, 12), (2, 1, 156933, 13),
                (2, 1, 156945, 14)]


def getoriginalData_csv_v2():
    originallist = []
    with open(os.path.join(DirPath_v2_content, '人教版题目_16w.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    for item in rows[1:]:
        # 顺序及对应字段含义见下表
        # Z计划 第一版 顺序 quesitonid,年级，bookId,单元Id,小节Id,知识点Id
        # originallist.append((item[0], item[2], item[3], item[5], item[7], item[9]))
        # Z计划 内容优化第二版 顺序 quesitonid,年级，bookId,单元Id,小节Id,知识点Id  和第一版一致
        originallist.append((item[0], item[2], item[3], item[5], item[7], item[9]))
    print('去除重复之前的长度', len(originallist))
    originallist = list(set(originallist))
    print('去除重复之后的长度', len(originallist))
    return originallist


def getoriginalData_csv():
    """
    sql更新后 一个question对应多个知识点，
    新写一个函数的原因：excel读出后，知识点没有逗号无法分割，导出用csv文件可以正确包含知识点数据
    :return:
    """
    originallist = []
    with open(os.path.join(MultiDirPath, 'allgradesquestioId知识点对应关系.csv'), 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    for item in rows[1:]:
        # 顺序及对应字段含义见下表
        originallist.append((item[0], item[1], item[2], item[4], item[6], item[8], item[10], item[11]))
    print('去除重复之前的长度', len(originallist))
    originallist = list(set(originallist))
    print('去除重复之后的长度', len(originallist))
    return originallist


def getoriginalData():
    """
    原sql 一个question对应一个知识点
    :return:
    """
    originallist = []
    filepath = os.path.join(SingleDirPath, 'allgradesquestionid对应关系1_1比例.xlsx')
    contentdata = xlrd.open_workbook(filepath)
    sheet = contentdata.sheets()[0]
    print(sheet.nrows)
    for row in range(1, sheet.nrows):
        # 判断python读取的ctype返回类型 0 --empty,1 --string, 2 --number(都是浮点), 3 --date, 4 --boolean, 5 --error
        # 可解决数字读入后变成浮点型数据 2.0、5846.0
        if sheet.cell(row, 0).ctype == 2 or sheet.cell(row, 1).ctype == 2 or \
                sheet.cell(row, 2).ctype == 2 or sheet.cell(row, 4).ctype == 2 or sheet.cell(row, 6).ctype == 2 or \
                sheet.cell(row, 8).ctype == 2 or sheet.cell(row, 10).ctype == 2 or sheet.cell(row, 11).ctype == 2:
            # 顺序 question_id、学期、年级、出版社ID、书本ID、单元ID、节ID
            originallist.append((
                # questionid 序号0
                str(int(sheet.cell_value(row, 0))),
                # 学期 序号1
                str(int(sheet.cell_value(row, 1))),
                # 年级 序号2
                str(int(sheet.cell_value(row, 2))),
                # 出版社id 序号3
                str(int(sheet.cell_value(row, 4))),
                # 书本id 序号4
                str(int(sheet.cell_value(row, 6))),
                # 单元id 序号5
                str(int(sheet.cell_value(row, 8))),
                # 节id 序号6
                str(int(sheet.cell_value(row, 10))),
                # 知识点id 序号7
                str(int(sheet.cell_value(row, 11)))))
    print(originallist)
    return originallist


def postProcess(originallist):
    tidylist = []
    sameunitquestionlist = []
    repeatedunitlist = []
    for item in originallist:
        # v1 精准 + 正则知识点匹配
        # repeatedunitlist.append((item[4], item[5], item[6]))
        # v2 同一道题目对应多个书本、单元、小节
        repeatedunitlist.append((item[2], item[3], item[4]))
    print('未去重之前 共有多少小节', len(repeatedunitlist))
    unitlist = list(set(repeatedunitlist))
    print('书本 、单元、节列表', unitlist, '\n', '共有:', len(unitlist))
    for unit in unitlist:
        for item in originallist:
            # 判断书本id、单元id、节id相同
            if item[2] == unit[0] and item[3] == unit[1] and item[4] == unit[2]:
                sameunitquestionlist.append(item)
            else:
                pass
        tidylist.append(sameunitquestionlist)
        sameunitquestionlist = []
    # for item in tidylist:
    #     V1:
    #     print('长度是', len(item), '单元id是', item[0][5])
    #     V2:
    #     print('长度是', len(item), '单元id是', item[0][3])
    return tidylist


def generagteUserRecord(userlist, processedlist):
    """
    生成每个用户的questionid
    :param userlist: 用户序列号列表
    :param processlist: 已经预处理过的同一个分组列表（表示同一单元、同一小节的题目，目的：确定进度）的题目
    :return:
    """
    lagerthanseedlist = []
    userrecord = []
    # 本轮所有的每个单元、小节生成的随机题目
    turnsingleuserquestionrecord = []
    # 读取unit和section 都相同，则添加到同一个分组列表中（表示同一单元、同一小节的题目，目的：确定进度） 以下为测试数据
    processlist = [
        [(1, 2, 1369, 1), (1, 2, 1489, 2), (1, 2, 1489, 3), (1, 2, 1411, 4), (1, 2, 1389, 5), (1, 2, 1449, 6),
         (1, 2, 2289, 7)],
        [(2, 1, 1569, 10), (2, 1, 13369, 11), (2, 1, 1569, 12), (2, 1, 156933, 13), (2, 1, 156945, 14)]]

    for originalunit in processedlist:
        if len(originalunit) < EXPECTED_SEED:
            pass
        else:
            lagerthanseedlist.append(originalunit)
    print('满足 {0} 随机档位范围的单元、小节数量有 {1}'.format(EXPECTED_SEED, len(lagerthanseedlist)))
    # 随机策略一：@deceprated 会产生完全一致记录的用户questionId 记录
    # for unit in lagerthanseedlist:
    #     seed = random.randint(EXPECTED_SEED - 9, EXPECTED_SEED)
    #     singleuserquestionrecord = random.sample(unit, seed)
    #     turnsingleuserquestionrecord.append(singleuserquestionrecord)
    # for user in userlist:
    #     userrecord.append((user, random.sample(turnsingleuserquestionrecord, 1)))
    # 随机策略二：虽然会出现questionid重复的，但是没有两个用户的questionId记录是完全相同的，通过扩大题库的量级可以降低重复率
    for user in userlist:
        try:
            seed = random.randint(EXPECTED_SEED - 9, EXPECTED_SEED)
            singleuserunit = random.sample(lagerthanseedlist, 1)
            singleuserrecord = random.sample(singleuserunit[0], seed)
            combine = generatecombine(user, singleuserrecord, GroupNum)
            userrecord.append(combine)
        except ValueError as valueerror:
            print(valueerror, 'seed 的大小', seed, '实际单元中包含题目数量', len(singleuserunit))
    # print('用户数据列表------------\n')
    # for user in userrecord:
    # 随机策略一的打印方式：@deprecated
    # print(len(user[1][0]), user)
    # 随机策略二的打印方式：
    #     print(len(user[1]), user)
    return userrecord


def generatecombine(user, singleuserrecord, num):
    length = len(singleuserrecord)
    if num == 2:
        group0 = singleuserrecord[0:int(length / 2)]
        group1 = singleuserrecord[int(length / 2):length]
        # print('总长度{0} 第一个分组长度 {1} 第二个分组长度{2}'.format(len(singleuserrecord),len(group0),len(group1)))
        return user, singleuserrecord, group0, group1
    elif num == 3:
        group0 = singleuserrecord[0:int(length / 3)]
        group1 = singleuserrecord[int(length / 3):int(2 * (length / 3))]
        group2 = singleuserrecord[int(2 * (length / 3)):length]
        # print('总长度{0} 第一个分组长度 {1} 第二个分组长度{2} 第三个分组长度{3}'.format(len(singleuserrecord), len(group0), len(group1),len(group2)))
        return user, singleuserrecord, group0, group1, group2
    else:
        return user, singleuserrecord


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
    # print(machineidlist)
    return machineidlist


def writeuserrecord(userrecord):
    """
    V1 精准知识点 + 正则知识点 写入函数
    :param userrecord:
    :return:
    """
    questions = []
    knowledges = []
    # 每条做题记录的步长
    i = 1
    # 每组做题记录的步长
    j = 0
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, str(EXPECTED_SEED) + '档位_序列号练习题记录.xlsx'))
    ws = workbook.add_worksheet(u'sheet1')
    ws.write(0, 0, 'machineId')
    ws.write(0, 1, 'questionId')
    ws.write(0, 2, '学期')
    ws.write(0, 3, '年级')
    ws.write(0, 4, '出版社')
    ws.write(0, 5, '书本Id')
    ws.write(0, 6, '单元Id')
    ws.write(0, 7, '小节Id')
    ws.write(0, 8, '本题知识点Id')
    ws.write(0, 9, '本序列号所有questions')
    ws.write(0, 10, '本序列号学习的所有知识点')
    ws.write(0, 11, '本序列号questions的数量')
    for user in userrecord:
        # 随机策略一的写方法：@deprecated
        # for question in user[1][0]:
        # 随机策略二的写方法：
        for question in user[1]:
            # quesiotnid
            ws.write(i, 0, user[0])
            ws.write(i, 1, question[0])
            # 学期
            ws.write(i, 2, question[1])
            # 年级
            ws.write(i, 3, question[2])
            # 出版社
            ws.write(i, 4, question[3])
            # 书本
            ws.write(i, 5, question[4])
            # 单元
            ws.write(i, 6, question[5])
            # 小节
            ws.write(i, 7, question[6])
            # 知识点
            ws.write(i, 8, question[7])
            questions.append(question[0])
            knowledges.append(question[7])
            i += 1
        stepandnum = len(questions)
        ws.write(j + stepandnum, 0, user[0])
        ws.write(j + stepandnum, 9, str(questions))
        ws.write(j + stepandnum, 10, str(knowledges))
        ws.write(j + stepandnum, 11, stepandnum)
        j += stepandnum
        questions = []
        knowledges = []
    workbook.close()


def writeuserrecord_v2(userrecord):
    questions = []
    knowledges = []
    # 每条做题记录的步长
    i = 1
    # 每组做题记录的步长
    j = 0
    workbook = xlsxwriter.Workbook(os.path.join(DirPath, str(EXPECTED_SEED) + '档位_序列号练习题记录.xlsx'))
    ws = workbook.add_worksheet('sheet1')
    ws.write(0, 0, 'machineId')
    ws.write(0, 1, 'questionId')
    ws.write(0, 2, '年级')
    ws.write(0, 3, '书本Id')
    ws.write(0, 4, '单元Id')
    ws.write(0, 5, '小节Id')
    ws.write(0, 6, '本题知识点Id')
    ws.write(0, 7, '本序列号所有questions')
    ws.write(0, 8, '本序列号学习的所有知识点')
    ws.write(0, 9, '本序列号questions的数量')
    for user in userrecord:
        # 随机策略一的写方法：@deprecated
        # for question in user[1][0]:
        # 随机策略二的写方法：
        for question in user[1]:
            # 序列号
            ws.write(i, 0, user[0])
            # quesiotnid
            ws.write(i, 1, question[0])
            # 年级
            ws.write(i, 2, question[1])
            # 书本
            ws.write(i, 3, question[2])
            # 单元
            ws.write(i, 4, question[3])
            # 小节
            ws.write(i, 5, question[4])
            # 知识点
            ws.write(i, 6, question[5])
            questions.append(question[0])
            knowledges.append(question[5])
            i += 1
        stepandnum = len(questions)
        ws.write(j + stepandnum, 0, user[0])
        ws.write(j + stepandnum, 7, str(questions))
        ws.write(j + stepandnum, 8, str(set(knowledges)))
        ws.write(j + stepandnum, 9, stepandnum)
        j += stepandnum
        questions = []
        knowledges = []
    workbook.close()


def writeuserrecord_v2_1(userrecord, num):
    questions = []
    knowledges = []
    # 每条做题记录的步长
    i = 1
    # 每组做题记录的步长
    j = 0
    workbook = xlsxwriter.Workbook(os.path.join(DirPath_v2_content, str(EXPECTED_SEED) + '档位_序列号练习题记录.xlsx'))
    ws0 = writecompletetitle(workbook)
    for user in userrecord:
        # 随机策略一的写方法：@deprecated
        # for question in user[1][0]:
        # 随机策略二的写方法：
        for question in user[1]:
            # 序列号
            ws0.write(i, 0, user[0])
            # quesiotnid
            ws0.write(i, 1, question[0])
            # 年级
            ws0.write(i, 2, question[1])
            # 书本
            ws0.write(i, 3, question[2])
            # 单元
            ws0.write(i, 4, question[3])
            # 小节
            ws0.write(i, 5, question[4])
            # 知识点
            ws0.write(i, 6, question[5])
            questions.append(question[0])
            knowledges.append(question[5])
            i += 1
        stepandnum = len(questions)
        ws0.write(j + stepandnum, 0, user[0])
        ws0.write(j + stepandnum, 7, str(questions))
        ws0.write(j + stepandnum, 8, str(set(knowledges)))
        ws0.write(j + stepandnum, 9, stepandnum)
        j += stepandnum
        questions = []
        knowledges = []
    group1quesitons = []
    group2quesitons = []
    group3quesitons = []
    if num == 1:
        pass
    elif num == 2:
        ws_group1 = workbook.add_worksheet('group' + str(1))
        ws_group2 = workbook.add_worksheet('group' + str(2))
        ws_group1.write(0, 0, 'machineId')
        ws_group1.write(0, 1, 'questionId')
        ws_group2.write(0, 0, 'machineId')
        ws_group2.write(0, 1, 'questionId')
    else:
        ws_group1 = workbook.add_worksheet('group' + str(1))
        ws_group2 = workbook.add_worksheet('group' + str(2))
        ws_group3 = workbook.add_worksheet('group' + str(3))
        ws_group1.write(0, 0, 'machineId')
        ws_group1.write(0, 1, 'questionId')
        ws_group2.write(0, 0, 'machineId')
        ws_group2.write(0, 1, 'questionId')
        ws_group3.write(0, 0, 'machineId')
        ws_group3.write(0, 1, 'questionId')
    group1j = 1
    group2j = 1
    group3j = 1
    for user in userrecord:
        if num == 1:
            pass
        elif num == 2:
            rownum_1 = group1j
            for question in user[2]:
                ws_group1.write(rownum_1, 0, user[0])
                ws_group1.write(rownum_1, 1, question[0])
                group1quesitons.append(question[0])
                rownum_1 += 1
            stepandnum1 = len(group1quesitons)
            group1j += stepandnum1
            group1quesitons = []
            rownum_2 = group2j
            for question in user[3]:
                ws_group2.write(rownum_2, 0, user[0])
                ws_group2.write(rownum_2, 1, question[0])
                group2quesitons.append(question[0])
                rownum_2 += 1
            stepandnum2 = len(group2quesitons)
            group2j += stepandnum2
            group2quesitons = []
        else:
            rownum_1 = group1j
            for question in user[2]:
                ws_group1.write(rownum_1, 0, user[0])
                ws_group1.write(rownum_1, 1, question[0])
                group1quesitons.append(question[0])
                rownum_1 += 1
            stepandnum1 = len(group1quesitons)
            group1j += stepandnum1
            group1quesitons = []
            rownum_2 = group2j
            for question in user[3]:
                ws_group2.write(rownum_2, 0, user[0])
                ws_group2.write(rownum_2, 1, question[0])
                group2quesitons.append(question[0])
                rownum_2 += 1
            stepandnum2 = len(group2quesitons)
            group2j += stepandnum2
            group2quesitons = []
            rownum_3 = group3j
            for question in user[4]:
                ws_group3.write(rownum_3, 0, user[0])
                ws_group3.write(rownum_3, 1, question[0])
                group3quesitons.append(question[0])
                rownum_3 += 1
            stepandnum3 = len(group3quesitons)
            group3j += stepandnum3
            group3quesitons = []
    workbook.close()


def writecompletetitle(workbook):
    ws = workbook.add_worksheet('completelist')
    ws.write(0, 0, 'machineId')
    ws.write(0, 1, 'questionId')
    ws.write(0, 2, '年级')
    ws.write(0, 3, '书本Id')
    ws.write(0, 4, '单元Id')
    ws.write(0, 5, '小节Id')
    ws.write(0, 6, '本题知识点Id')
    ws.write(0, 7, '本序列号所有questions')
    ws.write(0, 8, '本序列号学习的所有知识点')
    ws.write(0, 9, '本序列号questions的数量')
    return ws


def graphDBjsonparse():
    """
    图数据库json文件，解析
    图数据库：
    最外层start - end
    question->学期（上下册）
    question->学科（不用统计，就只有数学）
    question->版本（第几版印刷、第几版印刷 不用）
    question->出版社
    question->年级

    segment 的顺序：
    题、知识点、节、单元、书

    提测的标签 (这6个标签)：
    *出版社*
    *年级*
    *学期*
    知识点
    节
    单元
    :return:
    """
    endvaluelist = []
    detailvaluelist = []
    with open(r'C:\Users\Administrator\Desktop\quesitonid对应关系\records.json', 'r', encoding='utf-8') as f:
        jsondata = f.read()
        if jsondata.startswith(u'\ufeff'):
            strdata = jsondata.encode('utf-8')[3:].decode('utf-8')
            objdata = demjson.decode(strdata)
            for item in objdata:
                endvaluelist.append({str(item['p']['end']['labels']).replace('[', '').replace(']', '') \
                                    .replace('\'', ''): str(item['p']['end']['properties']['name'])})
            print(objdata[0]['p'])
            # if 'segments' in objdata[0]['p']:
            #     print(type(objdata[0]['p']['segments']))
            #     print(objdata[0]['p']['segments'])
            #     print('----------------------')
            #     for item in objdata[0]['p']['segments']:
            #         print(item)
            #
            for detail in objdata[0]['p']['segments']:
                detailvaluelist.append({str(detail['end']['labels']).replace('[', '').replace(']', '').replace('\'',
                                                                                                               ''): str(
                    detail['end']['properties']['name'])})
    print('外层直接获取的信息有', endvaluelist)
    print('知识点、节、单元信息', detailvaluelist)

    # strtest =  '[{"name":"17394740","question_type":"1","difficult":"3"},{},{"name":"认识因数、质数、合数"},{"name":"认识因数、质数、合数"},{},{"name":"4 因数"},{"name":"4 因数"},{},{"name":"五 倍数和因数"},{"name":"五 倍数和因数"},{},{"name":"数学四年级上册冀教版"},{"name":"数学四年级上册冀教版"},{},{"name":"上册"}]'
    # objdata = demjson.decode(strtest)
    # for item in objdata:
    #     print(item)


def test():
    listnum = [1, 2, 3]
    listnum1 = [4, 5, 6]
    list3 = []
    for i in range(0, len(listnum)):
        list3.append(listnum[i])
        list3.append(listnum1[i])
    print(list3)


def preProcess(originallist_signle, originallist_muilt):
    """
    预处理数据  把精准匹配知识点id和正在匹配id的列表一一拼接起来，两份数据数量相同，各占50%
    :param originallist_signle:
    :param originallist_muilt:
    :return:
    """
    listmixture = []
    for i in range(0, len(originallist_signle)):
        listmixture.append(originallist_signle[i])
        listmixture.append(originallist_muilt[i])
    return listmixture


def wholeprocess():
    number = 300
    machineIdlist = generateMahineid(number)
    # v1版本 正则 + 精准匹配
    # originallist_signle = getoriginalData()
    # originallist_muilt = getoriginalData_csv()
    # originallist = getoriginalData_csv_v2()
    # originallist = preProcess(originallist_signle, originallist_muilt)
    # -------------------------------------
    # v2 版本 同一道题目对一个多个书本章节
    originallist = getoriginalData_csv_v2()
    # -------------------------------------
    processedlist = postProcess(originallist)
    userrecord = generagteUserRecord(machineIdlist, processedlist)
    # v1 版本写入用户记录
    # writeuserrecord(userrecord)
    # v2 版本写入用户记录
    # writeuserrecord_v2(userrecord)
    writeuserrecord_v2_1(userrecord, GroupNum)

def writemachineId():
    machinelist = generateMahineid(20)
    worbook = xlsxwriter.Workbook(os.path.join(DirPath,'machineidlist.xlsx'))
    ws = worbook.add_worksheet('Sheet1')
    for i in range(len(machinelist)):
        ws.write(i,0,machinelist[i])
    worbook.close()

if __name__ == '__main__':
    # totalrecord = generatecombine('123', [1, 2, 3, 4, 5, 6, 7], 3)
    # workbook = xlsxwriter.Workbook(os.path.join(DirPath, str(EXPECTED_SEED) + '档位_序列号练习题记录_test.xlsx'))
    # writetitle(workbook, 3)
    # workbook.close()
    wholeprocess()
    # writemachineId()
