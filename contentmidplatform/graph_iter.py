# @File  : graph_iter.py
# @Author: LiuXingsheng
# @Date  : 2020/9/21
# @Desc  :
import requests
import demjson

edition = ['人教版','北师大版','苏教版','青岛版','冀教版']
grade = ['一年级','二年级','三年级','四年级','五年级','六年级']
term = ['上册','下册']

errorlist = []
nulllist = []
datanulllist = []
titlesnulllist = []
titlelist = []
for ed in edition:
    for grd in grade:
        for tm in term:
            result = requests.post(url='http://172.28.162.11:8088/relationCommend_demo/getAllChapterAndTitle',json={'grade':grd,'publisher':ed,'semester':tm})
            print(result.text)
            if result.status_code != requests.codes.ok:
                print('enter')
                errorlist.append([ed,grd,tm])
            else:
                print('correct')
                objdata = demjson.decode(result.text)
                if 'data' in objdata:
                    if objdata['data']:
                        for item in objdata['data']:
                            if 'titles' in item:
                                for title in item['titles']:
                                    titlelist.append(title['title_id'])
                            else:
                                titlesnulllist.append([ed,grd,tm])
                    else:
                        datanulllist.append([ed,grd,tm])
                else:
                    nulllist.append([ed,grd,tm])

with open('chapter错误记录','w')as fwrite:
    fwrite.write('请求错误的参数有----->\n' + str(errorlist) + '\n')
    fwrite.write('未返回data字段的参数有----->\n' + str(nulllist) + '\n')
    fwrite.write('data字段为空的参数有----->\n' + str(datanulllist) + '\n')
    fwrite.write('未返回chapter_id字段的参数有----->\n' + str(titlesnulllist) + '\n')
    fwrite.flush()

patherrorlist = []
pathdatanotexistlist = []
pathdatanulllist = []
pathnodenotexistlist = []
pathnodenulllist = []
for chapter in titlelist:
    result = requests.post(url='http://172.28.162.11:8088/relationCommend_demo/getKnowledgePath',
                           json={'catalog_id': chapter})
    if result.status_code != requests.codes.ok:
        print('enter')
        errorlist.append(chapter)
    else:
        objdata = demjson.decode(result.text)
        if 'data' in objdata:
            if objdata['data']:
                if 'nodeVoList' in objdata['data'] and 'edgeVoList' in objdata['data']:
                    if (objdata['data']['nodeVoList']) and (objdata['data']['edgeVoList']):
                        pass
                    else:
                        pathnodenulllist.append(chapter)
                else:
                    pathnodenotexistlist.append(chapter)
            else:
                pathdatanulllist.append(chapter)
        else:
            pathdatanotexistlist.append(chapter)
with open('KnowledgePath错误记录','w')as fwrite:
    fwrite.write('请求错误的参数有----->\n' + str(patherrorlist) + '\n')
    fwrite.write('未返回data字段的参数有----->\n' + str(pathdatanotexistlist) + '\n')
    fwrite.write('data字段为空的参数有----->\n' + str(pathdatanulllist) + '\n')
    fwrite.write('未返回nodeVoList或edgeVoList字段的参数有----->\n' + str(pathnodenotexistlist) + '\n')
    fwrite.write('nodeVoList或edgeVoList字段内容为空的参数有----->\n')
    for ite in pathnodenulllist:
        fwrite.write(str(ite) + '\n')
    fwrite.flush()


