# @File  : index_syn_test.py
# @Author: LiuXingsheng
# @Date  : 2021/1/22
# @Desc  : 索引同步测试

import requests
import os
import demjson
from pymysql import connect
import pymysql
from aitool.copyfile import writecontent
# 是否是网络题库
Is_Network = 0

def getdatacon():
    return connect(
        host='113.108.235.182',
        port=8406,
        user='test',
        password='123456',
        db='server_library_test',
        charset='utf8'
    )


def querydata(flag):
    con = getdatacon()
    if flag:
        querysql = 'select question_id from t_lingzhi_questions_update where syn_state = 1 and is_image_question = 1 ' \
                   'and image_upload_state = 1 and syn_tusou_state = 1'
    else:
        querysql = 'select question_id from t_lingzhi_questions_update ' \
                   'where (syn_state = 0 or image_upload_state = 0 or syn_tusou_state = 0) and (is_image_question = 1)'
    try:
        # 执行sql语句
        with con.cursor() as cursor:
            cursor.execute(querysql)
            # 提交到数据库执行
            con.commit()
            alldata = cursor.fetchall()
            # print(type(alldata), list(alldata))
            return alldata
    except pymysql.Error:
        # 如果发生错误则回滚
        print('error', pymysql.Error)
        con.rollback()
    finally:
        # 关闭数据库连接
        con.close()


def cleanid(questionId):
    return str(questionId).replace('(', '').replace(')', '').replace(',', '')

def getSelfCrawlQuestionByIdOld(idslist):
    """
    netwokr网络题库需要根据数据库中查询出的questionID查询出es中id才可进行以下的流程，剩余两个题库无需词操作
    :param idslist:
    :return:
    """
    datalist = []
    datanulllist = []
    noquestionlist = []
    for id in idslist:
        quesiotnId = cleanid(id)
        result = requests.get(url='http://test-all.eebbk.net/content-sync-platform/network/getSelfCrawlQuestionByIdOld',
                     params={'idOld':quesiotnId})
        if result.status_code == requests.status_codes.codes.ok:
            objdata = demjson.decode(result.text)
            if 'questionId' in result.text:
                if objdata['data']['questionId']:
                    datalist.append(objdata['data']['questionId'])
                else:
                    datanulllist.append(quesiotnId)
            else:
                noquestionlist.append(quesiotnId)
    print('数据库查询出questionid数量{0},用于查询ES的ID数量{1},返回questionId为空的数据有{2}个，分别是{3},未返回quesntionId的数量有'
          '{4},分别是{5}'.format(len(idslist),len(datalist),len(datanulllist),datanulllist,
                              len(noquestionlist),noquestionlist))
    return datalist

def gettopicinfo(tablename, datalist):
    """
    :param tablename:非mysql中表名，是syn_table字段中的表名
    :param datalist:
    :return:
    """
    urllist = []
    featurelist = []
    withoutfeaturelist = []
    synfaillist = []
    synsuccesscount = 0
    url = 'https://test-all.eebbk.net/image-sync-platform/question/index'
    for data in datalist:
        quesiotnId = cleanid(data)
        result = requests.get(url=url, params={'questionId': quesiotnId, 'syncTable': tablename})
        if result.status_code == requests.status_codes.codes.ok:
            objdata = demjson.decode(result.text)
            if 'containFeature' in result.text and 'feature64IndexVo' in result.text:
                if objdata['data']['feature64IndexVo'] and objdata['data']['containFeature'] == True:
                    featurelist.append({'quesiotnid': quesiotnId, 'imgIndexName': objdata['data']['imgIndexName']})
                    urllist.append([quesiotnId,str(objdata['data']['urls']).replace('[','').replace(']','').replace('\'','')])
                else:
                    withoutfeaturelist.append(quesiotnId)
            else:
                print('未返回 containFeature 或 feature64IndexVo')
    print('原符合查询条件数据共{0},具有特征值的数据共{1},分别是{2}'.format(len(datalist), len(featurelist), featurelist))
    for featureitem in featurelist:
        result = requests.get(
            url='http://47.112.238.105:8012/' + featureitem['imgIndexName'] + '/doc/' + featureitem['quesiotnid'])
        if result.status_code == requests.status_codes.codes.ok:
            objdata = demjson.decode(result.text)
            if 'found' in result.text:
                if objdata['found']:
                    synsuccesscount += 1
                else:
                    synfaillist.append(featureitem)
            else:
                print('不包含found字段', featureitem['quesiotnid'])
                synfaillist.append(featureitem)
        else:
            print('请求失败', featureitem['quesiotnid'])
            synfaillist.append(featureitem)
    print('存在特征值数据共有{0},同步成功数据共有{1},同步失败数据共有{2},失败的数据有{3}'.format(len(featurelist), synsuccesscount,
                                                                  len(synfaillist), synfaillist))
    writecontent(os.getcwd(),tablename+'_url记录20210125',urllist)

def gettopicinfo_undercarriage(tablename, datalist):
    illegallist = []
    gettopicinfo_undercarriage_counter = 0
    url = 'https://test-all.eebbk.net/image-sync-platform/question/index'
    for data in datalist:
        quesiotnId = cleanid(data)
        result = requests.get(url=url, params={'questionId': quesiotnId, 'syncTable': tablename})
        if result.status_code == requests.status_codes.codes.ok:
            objdata = demjson.decode(result.text)
            if 'urls' in result.text and 'imageNames' in result.text:
                if (not objdata['data']['urls']) and (not objdata['data']['imageNames']):
                    pass
                    gettopicinfo_undercarriage_counter += 1
                else:
                    illegallist.append(quesiotnId)
            else:
                print('未返回 urls 或 imageNames')
    print('原符合查询条件数据共{0},接口无url和images字段数据共{1},未成功下架共{2}，questionID分别是{3}'.format(len(datalist),
                                                                                  gettopicinfo_undercarriage_counter, len(illegallist),illegallist))


def getExceptionInfo(tablename,datalist):
    if datalist:
        errorinfolist = []
        url = 'https://test-all.eebbk.net/image-sync-platform/exceptionInfo/getExceptionInfo'
        for data in datalist:
            quesiotnId = cleanid(data)
            result = requests.get(url=url, params={'questionId': quesiotnId})
            errorinfolist.append([quesiotnId, result.text])
        writecontent(os.getcwd(), tablename + '_失败原因统计20210125', errorinfolist)
    else:
        pass
    print('原符合查询条件同步失败数据共{0}'.format(len(datalist)))


def update_testprocess(networkflag):
    print('同步成功数据测试，查询条件（与）syn_state=1 is_image_question=1 image_upload_state=1 syn_tusou_state=1')
    if networkflag:
        idslist = querydata(1)
        datalist = getSelfCrawlQuestionByIdOld(idslist)
    else:
        datalist = querydata(1)
    gettopicinfo('t_questions_workbook_online', datalist)
    print('同步失败数据测试，查询条件（或）syn_state=0 is_image_question=1 image_upload_state=0 syn_tusou_state=0')
    errordatalist = querydata(0)
    getExceptionInfo('t_questions_workbook_online', errordatalist)

def delete_testprocess(networkflag):
    print('同步成功数据测试，查询条件（与）syn_state=1 is_image_question=1 image_upload_state=1 syn_tusou_state=1')
    if networkflag:
        idslist = querydata(1)
        datalist = getSelfCrawlQuestionByIdOld(idslist)
    else:
        datalist = querydata(1)
    gettopicinfo_undercarriage('t_questions_self_crawl', datalist)
    print('同步失败数据测试，查询条件（或）syn_state=0 is_image_question=1 image_upload_state=0 syn_tusou_state=0')
    errordatalist = querydata(0)
    getExceptionInfo('下架t_questions_self_crawl', errordatalist)


if __name__ == '__main__':
    update_testprocess(Is_Network)
    # delete_testprocess(Is_Network)

