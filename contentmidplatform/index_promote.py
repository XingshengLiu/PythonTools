# @File  : index_promote.py
# @Author: LiuXingsheng
# @Date  : 2020/9/28
# @Desc  : 内容中台小题库索引优化
import os
import requests
import xlrd
import demjson

Dirpath = r'H:\内容中台\精准搜题项目\测试集\索引优化'


def readExcel():
    datalist = []
    contentdata = xlrd.open_workbook(os.path.join(Dirpath, 'index_promote.xlsx'))
    sheet = contentdata.sheets()[0]
    for row in range(1, sheet.nrows):
        datalist.append(int(sheet.cell_value(row, 0)))
    return datalist


def addQuestions(questionlist, optype):
    url = 'http://testaliyun.eebbk.net/syn-content-platform/api/addQuestions'
    questionidlist = []
    for question in questionlist:
        questionidlist.append({"operateState": optype, "questionId": question, "synTable": "t_finish_questions"})
    result = requests.post(url=url, json=questionidlist)
    print(result.text)


def getQuestion(questionlist):
    questionnotexistlist = []
    datanulllist = []
    datanotexistlis = []
    errorlist = []
    for question in questionlist:
        url = 'http://testaliyun.eebbk.net/aiplatform/api/ai-makequestion-service-v1/v1/bookQuestionInfoProofread/getQuestion/' + str(
            question)
        result = requests.get(url=url)
        if result.status_code == requests.status_codes.codes.ok:
            if 'data' in result.text:
                objdata = demjson.decode(result.text)
                if objdata['data'] and ('questionId' in objdata['data']):
                    if objdata['data']['questionId'] == question and (objdata['data']['title']):
                        pass
                    else:
                        questionnotexistlist.append(question)
                else:
                    datanulllist.append(question)
            else:
                datanotexistlis.append(question)
        else:
            errorlist.append(question)
    print('questionnotexistlist: ',questionnotexistlist)
    print('datanulllist: ',datanulllist)
    print('datanotexistlis:',datanotexistlis)
    print('errorlist: ',errorlist)



def es_check_math(questionlist):
    idnotexist = []
    idnotsamelist = []
    for question in questionlist:
        url = 'http://39.108.125.133:8168/math_all_alias/doc/' + str(question)
        result = requests.get(url=url)
        if '_id' in result.text:
            objdata = demjson.decode(result.text)
            if objdata['_id'] == str(question) and objdata['found'] == False:
                pass
            else:
                idnotsamelist.append(question)
        else:
            idnotexist.append(question)
    print('idnotexist:',idnotexist)
    print('idnotsamelist:',idnotsamelist)


def es_check_third(questionlist):
    idnotexist = []
    idnotsamelist = []
    for question in questionlist:
        url = 'http://39.108.125.133:8168/third_math_alias/doc/' + str(question)
        result = requests.get(url=url)
        if '_id' in result.text:
            objdata = demjson.decode(result.text)
            if objdata['_id'] == str(question) and objdata['found'] == False:
                pass
            else:
                idnotsamelist.append(question)
        else:
            idnotexist.append(question)
    print('idnotexist:',idnotexist)
    print('idnotsamelist:',idnotsamelist)

def getEncryptQuestionById(questionlist):
    errorlist = []
    url = 'http://testaliyun.eebbk.net/syn-content-platform/api/getEncryptQuestionById'
    for question in questionlist:
        result = requests.get(url=url,params={'questionId':question})
        if result.text == '数据不存在':
            pass
        else:
            errorlist.append(question)
    print('errorlist',errorlist)

def addProcess(questionlist):
    print(questionlist)
    # addQuestions(questionlist, 2)
    print('------getQuestion-----------')
    # getEncryptQuestionById(questionlist)
    print('------es_check_math-----------')
    es_check_math(questionlist)
    print('------es_check_third-----------')
    es_check_third(questionlist)


def updateProcess():
    pass


def deleteProcess():
    pass


if __name__ == '__main__':
    questionlist = readExcel()
    addProcess(questionlist)
    # addQuestions(questionlist,2)
    # getQuestion()
    # questionlist = [60006233]
    # addQuestions(questionlist, 2)
    # getQuestion(questionlist)
    # es_check_math(questionlist)
