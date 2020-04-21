# @File  : OCRtestLocal_Formula.py
# @Author: LiuXingsheng
# @Date  : 2019/10/28
# @Desc  : 云测平台公式OCR准确率测试脚本

import argparse
import datetime

import pandas as pd
import json
import numpy as np
import os
import re
import requests
import time
import xlsxwriter
from aitool.ailib import formula_ocr_test

latex_symbol_code_dict = dict()
latex_symbol_pattern = r'\\[A-Za-z][a-z]*'

PATH = r'H:\ocr本地自动化保存结果\OCRresult\Formula\OCR_resources_Path.txt'
SCENE = ['一维公式', '二维公式', '光线影响', '印刷质量不好', '图文结合', '多维公式', '手写和划线', '文字倾斜', '文本和公式', '模糊', '纯公式', '纯手写', '纸张不平整',
         '背景穿透', '表格、对话框']


def openResouce():
    with open(PATH, 'r')as f:
        allPath = f.read()
    pathList = allPath.split('@')
    resoutcePath = pathList[0]
    savePath = pathList[1]
    return resoutcePath, savePath


def get_latex_symbol_code(latex_symbol_str):
    if latex_symbol_str in latex_symbol_code_dict:
        return latex_symbol_code_dict[latex_symbol_str]
    else:
        code = len(latex_symbol_code_dict)
        latex_symbol_code_dict[latex_symbol_str] = code
        return code


def replace_latex_symbol_with_code(latex_str):
    result_str = latex_str
    for latex_symbol_str in re.findall(latex_symbol_pattern, latex_str):
        code = get_latex_symbol_code(latex_symbol_str)
        result_str = result_str.replace(latex_symbol_str, chr(code))

    return result_str


@DeprecationWarning
def regularize_latex(latex_str):
    """
    此方法已弃用，调用v2版本方法
    :param latex_str:
    :return:
    """
    # 基于有道的方法对公式做标准化
    # 将latex里面带有斜杠的元素，替换为一个字符
    result = replace_latex_symbol_with_code(latex_str)

    # 移除大括号{}
    result = result.replace('{', '').replace('}', '')
    # 移除空格
    result = result.replace(' ', '')
    return result


def edit_distance(pd_labels, gt_labels):
    l1 = len(pd_labels)
    l2 = len(gt_labels)
    t = np.zeros((l1 + 1, l2 + 1))
    for i in range(l1 + 1):
        t[i][0] = i
    for i in range(l2 + 1):
        t[0][i] = i
    for i in range(1, l1 + 1):
        for j in range(1, l2 + 1):
            m = min(t[i - 1][j], t[i][j - 1]) + 1
            t[i][j] = min(m, t[i - 1][j - 1] + (0 if pd_labels[i - 1] == gt_labels[j - 1] else 1))
    return t[l1][l2]


@DeprecationWarning
def ocr_use_bbk(img):
    # url = 'http://test.eebbk.net/ocr/api/recognizeLatexLocal'
    url = 'http://127.0.0.1:9080/ocr/api/recognizeLatexLocal'
    response = requests.post(url,
                             files={'url': img}
                             )
    if response.status_code != requests.codes.ok:
        print(response.content.decode('utf-8'))
        raise Exception(response.status_code)

    result = response.content.decode('utf-8')
    response.close()

    return result


def ocr_use_bbk_v_2(img):
    """
    此方法为正式环境地址，forula_ocr_test中的为测试环境
    :param img:
    :return:
    """
    # url = 'http://test.eebbk.net/ocr/api/recognizeLatexLocal'
    url = 'http://ocr-xtc.eebbk.net/ocr/api/v1.0'
    param = {
        'img_type': 1,
        'service_type': 'formula'
    }
    response = requests.post(url,
                             data=param,
                             files={
                                 'upl_img': img}
                             )
    if response.status_code != requests.codes.ok:
        print(response.content.decode('utf-8'))
        raise Exception(response.status_code)

    result = response.content.decode('utf-8')
    response.close()

    return result


def get_bbk_latex_result(jstr):
    jobj = json.loads(jstr)
    if 'data' not in jobj:
        return ''

    data = jobj['data']
    if data is None:
        return ''

    regions = data['regions']
    if regions is None:
        return ''

    result_str = ''
    for region in regions:
        lines = region['lines']
        for line in lines:
            if line['type'] == 'formula':
                # print(line['text'])
                result_str += ' %s' % line['text']

    return result_str


def ocr_use_youdao_newVersion(img):
    url = 'http://test.eebbk.net/pointquestion-app/app/ocrtest/ocrIdentify1/customizationAllOcr?ocrType=formula'
    response = requests.post(url=url, files={'file': img})
    if response.status_code != requests.codes.ok:
        print(response.text)
        raise Exception(response.status_code)

    result = response.content.decode('utf-8')
    response.close()
    return result


def get_youdao_newVersion_latex_result(rjstr):
    jobj = json.loads(rjstr)
    data = jobj['data']
    if data is None:
        return ''
    regions = data['regions']
    if regions is None:
        return ''
    result = ''
    for region in regions:
        lines = region['lines']
        if lines is None:
            continue
        for line in lines:
            for one_line in line:
                if one_line['type'] == 'formula':
                    result += ' %s' % one_line['text']
    return result


def ocr_use_youdao(img, xPoint=-1, yPoint=-1, mode='ocr'):
    url = 'http://test.eebbk.net/social-scan/ocr/customizationOcr'
    param = {
        'xPoint': str(xPoint),
        'yPoint': str(yPoint),
        'serviceType': mode,
    }

    response = requests.post(url,
                             data=param,
                             files={'file': img}
                             )
    if response.status_code != requests.codes.ok:
        print(response.content.decode('utf-8'))
        raise Exception(response.status_code)

    result = response.content.decode('utf-8')
    response.close()

    return result


def get_youdao_latex_result(rjstr):
    jobj = json.loads(rjstr)
    data = jobj['data']
    if data is None:
        return ''
    regions = data['regions']
    if regions is None:
        return ''

    result = ''
    for region in regions:
        lines = region['lines']
        if lines is None:
            continue

        for line in lines:
            for one_line in line:
                if one_line['type'] == 'formula':
                    result += ' %s' % one_line['text']

    return result


def ocr_use_hanvon(img):
    url = 'http://test.eebbk.net/questionanswer/m1000/search/ocrPicGs'
    response = requests.post(url,
                             files={'imgFile': img})
    if response.status_code != requests.codes.ok:
        print(response.content.decode('utf-8'))
        raise Exception(response.status_code)

    result = response.content.decode('utf-8')
    response.close()

    return result


def get_hanvon_latex_result(jstr):
    jobj = json.loads(jstr)
    data = jobj['data']
    if data is None:
        return ''

    result = ''
    for elem in data:
        if elem['latexStr'] is not None:
            result += ' %s' % elem['latexStr']

    return result


OCR_METHOD_YOUDAO_NEW = 0
OCR_METHOD_HANVON = 1
OCR_METHOD_YOUDAO = 2
OCR_METHOD_BBK = 3
OCR_METHOD_ALL = 4


def ocr_formula(img, method):
    if method == OCR_METHOD_HANVON:
        ocr_func = ocr_use_hanvon
        get_func = get_hanvon_latex_result
    elif method == OCR_METHOD_YOUDAO:
        ocr_func = lambda x: ocr_use_youdao(x, mode='formula')
        get_func = get_youdao_latex_result
    elif method == OCR_METHOD_BBK:
        # ocr_func = ocr_use_bbk
        ocr_func = formula_ocr_test.ocr_use_bbk_v_2
        get_func = get_bbk_latex_result
    elif method == OCR_METHOD_YOUDAO_NEW:
        ocr_func = ocr_use_youdao_newVersion
        get_func = get_youdao_newVersion_latex_result
    else:
        raise Exception('invalid paramter method, value: %d' % method)

    try:
        jstr = ocr_func(img)
        if jstr is None or jstr == '':
            return ''

        latex_str = get_func(jstr)
    except Exception:
        latex_str = ''

    return latex_str


def getPicDir(dir):
    dirList = []
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            path = os.path.join(root, dir)
            dirList.append(path)
    return dirList


def read_formula_annotation_excel(annotation_file_path):
    df = pd.read_excel(annotation_file_path)
    result_list = []

    prev_file_name = None
    latex_str = ''
    for idx, row in df.iterrows():
        curr_file_name = row['原图文件名']
        curr_latex_str = row['LaTex公式']

        if type(curr_file_name) == float or curr_file_name.lstrip().rstrip() == '':
            continue

        if prev_file_name is None:
            prev_file_name = curr_file_name

        if prev_file_name == curr_file_name:
            latex_str += ' %s' % str(curr_latex_str)
        else:
            result_list.append((prev_file_name, latex_str))

            prev_file_name = curr_file_name
            latex_str = str(curr_latex_str)

    result_list.append((prev_file_name, latex_str))

    return result_list


def read_formula_anotation_single(excelFile):
    df = pd.read_excel(excelFile)
    res_dict = {}

    prev_file_name = None
    latex_str = ''
    for idx, row in df.iterrows():
        curr_file_name = row['原图文件名']
        curr_latex_str = row['LaTex公式']

        if type(curr_file_name) == float or curr_file_name.lstrip().rstrip() == '':
            continue

        if prev_file_name is None:
            prev_file_name = curr_file_name

        if prev_file_name == curr_file_name:
            latex_str += ' %s' % str(curr_latex_str)
        else:
            res_dict[prev_file_name] = latex_str

            prev_file_name = curr_file_name
            latex_str = str(curr_latex_str)
    res_dict[prev_file_name] = latex_str
    return res_dict


def getProcessedTypeAssemble(resoucePath, savePath):
    allList = []
    dirList = getPicDir(resoucePath)
    for item in dirList:
        typeList = []
        for file in os.listdir(item):
            filePath = os.path.join(item, file)
            if (os.path.isfile(filePath)) and (
                    filePath.endswith(".jpg") or filePath.endswith(".png") or filePath.endswith(".bmp")):
                typeList.append(filePath)
            else:
                pass
        if typeList:
            allList.append(typeList)
        else:
            pass
    return allList


def latexprocess(use_ocr):
    """
    预处理latex及规范化
    :param use_ocr:
    :return:
    """
    standardize_latex_use_ocr = formula_ocr_test.latex_preprocess(use_ocr)
    rg_latex_str_use_ocr = formula_ocr_test.regularize_latex_v2(standardize_latex_use_ocr)
    return rg_latex_str_use_ocr


def test_formula(resoucePath, savePath):
    res_dict = {}
    all_detail_list = []
    comprehensiveList = []

    allpicList = getProcessedTypeAssemble(resoucePath, savePath)

    for file in os.listdir(resoucePath):
        if file.endswith('.xlsx'):
            res_dict = read_formula_anotation_single(os.path.join(resoucePath, file))

    for typePicItem in allpicList:
        total_file = 0
        ocr_total_recognize_rate = 0.0
        youdao_total_recognize_rate = 0.0
        typeName, sceneName = typePicItem[0].split('\\')[-3], typePicItem[0].split('\\')[-2]
        for singleAbsPic in typePicItem:
            picName = singleAbsPic.split('\\')[-1]
            try:
                org_latex_str = res_dict[picName]
                gt_latex_str = formula_ocr_test.latex_preprocess(org_latex_str)
            except KeyError:
                continue

            print('dealing file:%s' % singleAbsPic)

            # 将标注的latex格式化，三种识别接口都可以使用
            rg_latex_label_ocr = formula_ocr_test.regularize_latex_v2(gt_latex_str)
            with open(singleAbsPic, 'rb') as f:
                img_data = f.read()

            ocr_formula_word_bbk = ocr_formula(img_data, 3)
            rg_latex_recog_bbk_str = latexprocess(ocr_formula_word_bbk)
            edit_dist = edit_distance(rg_latex_recog_bbk_str, rg_latex_label_ocr)
            bbk_acc = getaccuracy(rg_latex_label_ocr, rg_latex_recog_bbk_str, edit_dist)
            ocr_total_recognize_rate += bbk_acc
            # print("【标注结果】{}".format(gt_latex_str))
            # print("【自研结果】{}".format(ocr_formula_word_bbk))
            # print("【自研准确率】{}".format(bbk_acc))

            ocr_formula_word_yd = ocr_formula(img_data, 2)
            rg_latex_recog_yd_str = latexprocess(ocr_formula_word_yd)
            edit_dist = edit_distance(rg_latex_recog_yd_str, rg_latex_label_ocr)
            yd_acc = getaccuracy(rg_latex_label_ocr, rg_latex_recog_yd_str, edit_dist)
            youdao_total_recognize_rate += yd_acc
            # print("【标注结果】{}".format(gt_latex_str))
            # print("【有道结果】{}".format(ocr_formula_word_yd))
            # print("【有道准确率】{}".format(yd_acc))

            one_res_list = [picName, gt_latex_str, ocr_formula_word_bbk, ocr_formula_word_yd, bbk_acc, yd_acc, typeName,
                            sceneName]
            all_detail_list.append(one_res_list)
            total_file += 1

        print('------DONE--------\n type is {0}, totalfile is {1} 有道识别率总和：{2} 自研识别率总和：{3}'.
              format(typeName, total_file, youdao_total_recognize_rate, ocr_total_recognize_rate))
        if total_file == 0:
            typeResult = ['\\', '\\', typeName, sceneName]
        else:
            typeResult = ['%.2f%%' % ((ocr_total_recognize_rate / total_file) * 100),
                          '%.2f%%' % ((youdao_total_recognize_rate / total_file) * 100), typeName, sceneName]
        print('类型是:{0} 场景是:{1} 有道识别率结果:{2} 自研识别率结果:{3}'.format(typeResult[2], typeResult[3], typeResult[0],
                                                               typeResult[1], ))
        comprehensiveList.append(typeResult)

    # output_df = pd.DataFrame(all_list, columns=['自研准确率', '有道准确率', '图片类型', '科目'])
    dt = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = '{0}{1}{2}'.format('ocrResult_Fuormula_', str(dt), '.xlsx')
    writeContent2Excel(comprehensiveList, all_detail_list, filename, savePath)
    # return filename
    # output_df.to_excel(os.path.join(savePath, filename), encoding='utf-8', sheet_name='详细统计')


def setTitleProperty():
    return {
        'font_size': 11,
        'font_color': '#FFFFFF',
        'bold': True,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': u'微软雅黑',
        'text_wrap': False,
        'fg_color': '#00B0F0'
    }


def setContentProperty():
    return {
        'font_size': 11,
        'font_color': '#000000',
        'bold': False,
        'align': 'center',
        'valign': 'vcenter',
        'font_name': u'微软雅黑',
        'text_wrap': False,
    }


def writeContent2Excel(comprehensiveList, all_detail_list, filename, savePath):
    workbook = xlsxwriter.Workbook(os.path.join(savePath, filename))
    titleform = workbook.add_format(setTitleProperty())
    contentform = workbook.add_format(setContentProperty())
    wsSum = workbook.add_worksheet(u'统计')
    wsDetail = workbook.add_worksheet(u'测试详情')
    wsDetail.set_column('A:H', 15)
    wsSum.set_column('A:A', 30)
    wsSum.merge_range('A1:A2', '场景', titleform)
    wsSum.merge_range('B1:C1', '数学', titleform)
    wsSum.merge_range('D1:E1', '物理', titleform)
    wsSum.merge_range('F1:G1', '化学', titleform)
    wsSum.write('B2', '自研', contentform)
    wsSum.write('C2', '有道', contentform)
    wsSum.write('D2', '自研', contentform)
    wsSum.write('E2', '有道', contentform)
    wsSum.write('F2', '自研', contentform)
    wsSum.write('G2', '有道', contentform)
    row = 2
    for item in SCENE:
        wsSum.write(row, 0, item, contentform)
        row += 1

    print('======================')
    print(comprehensiveList)
    for single in comprehensiveList:
        rownum = getLocation(single[-1])
        if '数学' == single[-2]:
            wsSum.write('B%s' % rownum, single[0], contentform)
            wsSum.write('C%s' % rownum, single[1], contentform)
        elif '物理' == single[-2]:
            wsSum.write('D%s' % rownum, single[0], contentform)
            wsSum.write('E%s' % rownum, single[1], contentform)
        else:
            wsSum.write('F%s' % rownum, single[0], contentform)
            wsSum.write('G%s' % rownum, single[1], contentform)
    wsDetail.write(0, 0, '图片名', titleform)
    wsDetail.write(0, 1, '标注latex', titleform)
    wsDetail.write(0, 2, '自研识别结果', titleform)
    wsDetail.write(0, 3, '有道是被结果', titleform)
    wsDetail.write(0, 4, '自研准确率', titleform)
    wsDetail.write(0, 5, '有道准确率', titleform)
    wsDetail.write(0, 6, '科目', titleform)
    wsDetail.write(0, 7, '图片类型', titleform)
    row_detail = 1
    for sigleRecord in all_detail_list:
        wsDetail.write(row_detail, 0, sigleRecord[0], contentform)
        wsDetail.write(row_detail, 1, sigleRecord[1], contentform)
        wsDetail.write(row_detail, 2, sigleRecord[2], contentform)
        wsDetail.write(row_detail, 3, sigleRecord[3], contentform)
        wsDetail.write(row_detail, 4, sigleRecord[4], contentform)
        wsDetail.write(row_detail, 5, sigleRecord[5], contentform)
        wsDetail.write(row_detail, 6, sigleRecord[6], contentform)
        wsDetail.write(row_detail, 7, sigleRecord[7], contentform)
        row_detail += 1
    workbook.close()


def getLocation(strItem):
    rownum = 2 + SCENE.index(strItem) + 1
    return rownum


def splitName(str):
    picNameList = str.split('\\')
    return picNameList[-1], picNameList[-2]


def getaccuracy(rg_latex_label_ocr, rg_latex_recog_str, edit_dist):
    gt_len = len(rg_latex_label_ocr)
    predict_len = len(rg_latex_recog_str)
    max_len = gt_len if gt_len > predict_len else predict_len
    acc = 1 - edit_dist / max_len
    return acc


def get_method_name(method_id):
    if method_id == OCR_METHOD_HANVON:
        method_name = '汉王'
    elif method_id == OCR_METHOD_YOUDAO:
        method_name = '有道'
    elif method_id == OCR_METHOD_BBK:
        method_name = '步步高自研'
    elif method_id == OCR_METHOD_YOUDAO_NEW:
        method_name = '有道优化'
    else:
        raise Exception('unsupported method id, value: %d' % method_id)

    return method_name


def get_output_excel_name(method_id):
    current_time = time.time()
    return '%d_%s.xls' % (current_time, get_method_name(method_id))


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('method_id', type=int,
                        help='methodId可为0,1,2,3,4。0为有道优化后公示ocr,1表示使用汉王的公式OCR，2为有道公式OCR，3为BBK自研OCR，4为测试所有')
    parser.add_argument('src_excel_path', type=str,
                        help='标注的excel文件地址')
    parser.add_argument('output_dir', type=str,
                        help='详情excel文件输出目录')
    parser.add_argument('img_base_path', type=str,
                        default='./',
                        help='可选参数，表示存放图片文件的目录路径，默认为当前目录')

    args = parser.parse_args()
    return args


def findnewestfile(file_path):
    filenames = os.listdir(file_path)
    print(filenames)
    name_ = []
    time_ = []
    for filename in filenames:
        if '.xlsx' == filename[-5:]:  ##因我只想查询png类的文件，不用的可以删除
            # print filename
            c_time = os.path.getctime(file_path + '\\' + filename)

            # print type(mtime)
            name_.append(file_path + '\\' + filename)
            time_.append(c_time)
            # print filename,mtime
    newest_file = name_[time_.index(max(time_))]
    return newest_file


def startFunction():
    resourcePath, savePath = openResouce()
    test_formula(resourcePath, savePath)
    latestfilename = findnewestfile(savePath)
    return str(os.path.join(savePath, latestfilename))


def testfunc():
    filter = ['.jpg']
    teststr = ['/usr/jmeter/test.wav', '/usr/jmeter/test.tiff', '/usr/jmeter/test.jpg']
    for item in teststr:
        if os.path.splitext(item)[1] not in filter:
            print(item)


if __name__ == '__main__':
    testfunc()
    # resourcePath, savePath = openResouce()
    # test_formula(resourcePath, savePath)

listest = []
import queue

web = queue.Queue()
web.empty()






