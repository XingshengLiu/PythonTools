# @File  : ocr_test_local.py
# @Author: LiuXingsheng
# @Date  : 2019/10/22
# @Desc  : 云测平台英文OCR准确率测试脚本

import argparse
import base64
import codecs
import json
import os
import datetime

import pandas as pd
import requests

PATH = r'H:\ocr本地自动化保存结果\OCRresult\English\OCR_resources_Path.txt'

parser = argparse.ArgumentParser(description='')
parser.add_argument('--test_dir', dest='test_dir')
parser.add_argument('--label_file', dest='label_file', default='label.xlsx')
parser.add_argument('--compare_mode', dest='compare_mode', default='c')
args = parser.parse_args()


def openResouce():
    with open(PATH, 'r')as f:
        allPath = f.read()
    pathList = allPath.split('@')
    resoutcePath = pathList[0]
    savePath = pathList[1]
    return resoutcePath, savePath


def comp_str(str1, str2):
    # str1: 标注字符串
    # str2: 模型预测字符串
    len1 = len(str1)
    len2 = len(str2)

    comp_list = []
    for i in range(len1 + 1):
        one_comp_list = [0 for i in range(len2 + 1)]
        comp_list.append(one_comp_list)

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if str1[i - 1] == str2[j - 1]:
                comp_list[i][j] = comp_list[i - 1][j - 1] + 1
            else:
                comp_list[i][j] = max(comp_list[i][j - 1], comp_list[i - 1][j])
    if (len1 + len2) == 0:
        similar = 0
    else:
        similar = 1 - (len1 + len2 - 2 * comp_list[len1][len2]) / (len1 + len2)

    return similar


def get_ocr_result(file_name):
    with open(file_name, "rb") as img_file:
        img_data = img_file.read()

    # url = 'http://39.108.125.133:8080/ocr/api/v1.0'
    url = 'http://bbkocr.eebbk.net/ocr/api/v1.0'
    param = {
        'img_type': 1,
        'service_type': 'formula'
    }

    try:
        r = requests.request("POST", url=url, files={'upl_img': img_data}, data=param, timeout=100)
    except requests.exceptions.ConnectionError:
        raise requests.exceptions.ConnectionError("ConnectionError")

    r_str = ''
    try:
        region_list = r.json()['data']['regions']
        for region in region_list:
            line_list = region['lines']
            for line in line_list:
                r_str += line['text']
    except json.JSONDecodeError:
        r_str = ""
    except KeyError:
        r_str = ''
    except TypeError:
        r_str = ''

    return r_str


def get_youdao_result(file_name):
    url = 'http://test.eebbk.net/social-scan/ocr/customizationOcr'
    param = {
        'xPoint': str(-1),
        'yPoint': str(-1),
        'serviceType': 'formula',
    }
    response = requests.post(url,
                             data=param,
                             files={'file': open(file_name, 'rb')}
                             )
    if response.status_code != requests.codes.ok:
        print(response.content.decode('utf-8'))
        return '服务器报错'

    strdata = response.content.decode('utf-8')
    jobj = json.loads(strdata)
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
                result += one_line['text']
    return result


def get_hanwang_result_online(file_name):
    with open(file_name, "rb") as img_file:
        img_data = img_file.read()
    img_data = base64.b64encode(img_data)
    img_key = "HanvonTestBuBuGao"
    body_data = {
        'key': img_key,
        'base64img': img_data
    }

    body_header = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Content-Length': 'length'
    }

    api_url = "http://39.96.18.12:8151/HanvonOCR.asmx/DocReco"

    r = requests.request("POST", url=api_url, headers=body_header, data=body_data, timeout=100)

    try:
        res_list = r.json()['result']
        raw_str = ""
        for res in res_list:
            if isinstance(res, dict):
                if res['text'] is not None:
                    raw_str += res['text']
    except KeyError:
        raw_str = ""

    return raw_str


def get_hanwang_result(file_name):
    with open(file_name, "rb") as img_file:
        img_data = img_file.read()

    url = 'http://test.eebbk.net/questionanswer/m1000/search/ocrPicGs'
    file_data = {'imgFile': img_data}

    r_str = ''
    try:
        r = requests.request("POST", url=url, files=file_data, timeout=100)
    except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
        return '服务器错误'

    try:
        for line in r.json()['data']:
            if line['strResult'] is not None:
                r_str += line['strResult']
    except KeyError:
        r_str += ''

    return r_str


def getPicDir(dir):
    dirList = []
    for root, dirs, files in os.walk(dir):
        for dir in dirs:
            path = os.path.join(root, dir)
            dirList.append(path)
    return dirList


def accuracy_test(resoucePath, savePath, compare_mode='c'):
    dt = datetime.datetime.now().strftime('%Y_%m_%d')
    filename = '{0}{1}{2}'.format('ocrResult_English_', str(dt), '.xls')
    writer = pd.ExcelWriter(os.path.join(savePath, filename))
    dirList = getPicDir(resoucePath)
    comprehensiveList = []
    all_res_list = []
    ocr_total_recognize_rate = 0.0
    youdao_total_recognize_rate = 0.0
    hanwang_total_recognize_rate = 0.0
    total_file = 0

    res_dict = {}
    for dir in dirList:
        for img_path in os.listdir(dir):
            if img_path.endswith('.xlsx'):
                label_df = pd.read_excel(os.path.join(dir, img_path))
                for _, label in label_df.iterrows():
                    res_dict[label['图片名称']] = str(label['核对文本']).replace("“", "\"").replace("”", "\"").replace(",",
                                                                                                               "，").replace(
                        "（",
                        "(").replace(
                        "）", ")").replace("？", "?")

    for dir in dirList:
        for img_path in os.listdir(dir):
            if img_path.endswith(".jpg") or img_path.endswith(".png") or img_path.endswith(".bmp"):
                print(img_path + "----------------------------------------")

                abs_img_path = os.path.join(dir, img_path)
                try:
                    correct_word = res_dict[img_path]
                except KeyError:
                    continue

                ocr_word = get_ocr_result(abs_img_path).replace("“", "\"").replace("”", "\"").replace(",",
                                                                                                      "，").replace(
                    "（", "(").replace("）", ")").replace("？", "?")
                ocr_recognize_rate = comp_str(correct_word, ocr_word)
                ocr_total_recognize_rate += ocr_recognize_rate

                # print("【标注结果】{}".format(correct_word))
                # print("【自研结果】{}".format(ocr_word))
                # print("【自研准确率】{}".format(ocr_recognize_rate))

                if compare_mode == 'c':
                    youdao_word = get_youdao_result(abs_img_path).replace("“", "\"").replace("”", "\"").replace(",",
                                                                                                                "，").replace(
                        "（", "(").replace("）", ")").replace("？", "?")
                    youdao_recognize_rate = comp_str(correct_word, youdao_word)
                    youdao_total_recognize_rate += youdao_recognize_rate

                    # print("【有道结果】{}".format(youdao_word))
                    # print("【有道准确率】{}".format(youdao_recognize_rate))

                    hanwang_word = get_hanwang_result(abs_img_path).replace("“", "\"").replace("”", "\"").replace(",",
                                                                                                                  "，").replace(
                        "（", "(").replace("）", ")").replace("？", "?")
                    hanwang_recognize_rate = comp_str(correct_word, hanwang_word)
                    hanwang_total_recognize_rate += hanwang_recognize_rate

                    # print("【汉王结果】{}".format(hanwang_word))
                    # print("【汉王准确率】{}".format(hanwang_recognize_rate))
                else:
                    youdao_word = '-'
                    youdao_recognize_rate = 0

                    hanwang_word = '-'
                    hanwang_recognize_rate = 0

                one_res_list = [img_path, correct_word, ocr_word, youdao_word, hanwang_word, ocr_recognize_rate,
                                youdao_recognize_rate, hanwang_recognize_rate]
                all_res_list.append(one_res_list)

                print()

                total_file += 1
        print("Done!")
        typeName = splitName(dir)
        res_type_all = pd.DataFrame(all_res_list,
                                    columns=["图片编号", "标注文本", "自研结果", "有道结果", "汉王结果", "自研准确率", "有道准确率", "汉王准确率"])
        res_type_all.to_excel(writer, encoding="utf-8", sheet_name=typeName)
        typeResult = [typeName, '%.2f%%' % ((youdao_total_recognize_rate / total_file) * 100),
                      '%.2f%%' % ((hanwang_total_recognize_rate / total_file) * 100),
                      '%.2f%%' % ((ocr_total_recognize_rate / total_file) * 100)]
        comprehensiveList.append(typeResult)
        all_res_list.clear()
    for item in comprehensiveList:
        print(item)
    res_df = pd.DataFrame(comprehensiveList, columns=["图片类型", "有道准确率", "汉王准确率", "自研准确率"])
    res_df.to_excel(writer, encoding="utf-8", sheet_name='汇总统计')
    writer.save()
    return filename


def excel2Html(savePath, filename):
    xd = pd.ExcelFile(os.path.join(savePath, filename))
    pd.set_option('colheader_justify', 'center')
    df = xd.parse()
    htmlFileName = '{0}{1}{2}{3}'.format(savePath, '\\', 'htmlresult', '.html')
    with codecs.open(htmlFileName, 'w')as html_file:
        html_file.write(df.to_html(header=True, index=False))


def accuracy_test_dir(scene_dir, compare_mode):
    img_dirs = os.listdir(scene_dir)
    for img_dir in img_dirs:
        abs_img_dir = os.path.join(scene_dir, img_dir)
        label_file = None
        for img_path in os.listdir(abs_img_dir):
            if img_path.endswith('.xlsx'):
                label_file = os.path.join(abs_img_dir, img_path)
            if label_file is not None:
                accuracy_test(abs_img_dir, label_file, compare_mode)


def splitName(str):
    picNameList = str.split('\\')
    return picNameList[-1]


def findnewestfile(file_path):
    filenames = os.listdir(file_path)
    print(filenames)
    name_ = []
    time_ = []
    for filename in filenames:
        if '.xls' == filename[-4:]:  ##因我只想查询png类的文件，不用的可以删除
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
    accuracy_test(resourcePath, savePath)
    latestfilename = findnewestfile(savePath)
    return str(os.path.join(savePath, latestfilename))

if __name__ == '__main__':
    resourcePath, savePath = openResouce()
    filename = accuracy_test(resourcePath, savePath)
    # excel2Html(savePath,filename)
