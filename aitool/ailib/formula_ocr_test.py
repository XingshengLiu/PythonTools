import argparse
import pandas as pd
import json
import numpy as np
import os
import re
import requests
import time


latex_symbol_code_dict = dict()
latex_symbol_pattern = r'\\[A-Za-z][a-z]*'


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


def regularize_latex(latex_str):
    # 基于有道的方法对公式做标准化
    # 将latex里面带有斜杠的元素，替换为一个字符
    result = replace_latex_symbol_with_code(latex_str)

    # 移除大括号{}
    result = result.replace('{', '').replace('}','')
    # 移除空格
    result = result.replace(' ', '')
    return result


latex_symbols = "\% \Delta \Gamma \Lambda \Leftrightarrow \Omega \Phi \Rightarrow \Theta \\\\ \\alpha \\angle \\approx \\ast \\because \\begin \\beta \cap \cdot \cdots \circ \cong \cos \cot \cup \div \dot \dots \downarrow \emptyset \end \equiv \eta \exists \\forall \\frac \gamma \geq \hat \hline \in \infty \int \lambda \langle \leq \lim \limits \ln \lnot \log \longdiv \mu \\neq \\notin \\nu \odot \omega \oplus \otimes \overline \overrightarrow \perp \phi \pi \pm \psi \\rangle \\rho \\rightarrow \sigma \sim \sin \sqrt \square \stackrel \subset \subseteq \sum \\tan \\tau \\therefore \\theta \\times \\triangle \\unknown \\uparrow \\varphi \\vee \wedge \widehat \\xi \{ \} matrix \\textcircled \overset \\underset \\bar \\upsilon \\rightleftharpoons \\underbrace \epsilon \\bigcirc \\underline \parallelogram \overarc \\backslash \left \\right \\not"
latex_symbols = latex_symbols.split(" ")
latex_symbols_list = sorted(latex_symbols, key=lambda x: len(x), reverse=True)

latex_symbol_code_dict_v1 = {latex_symbols[i]: 128 + i for i in range(len(latex_symbols))}


def replace_latex_symbol_with_code_v2(latex_str):
    """
    完全弃用之前的方法，修复 字符 替换的问题 以及 latex 字符和小写字母粘连的问题(\timesb)
    :param latex_str:
    :return:
    """
    result_str = latex_str
    for latex_symbol_str in latex_symbols_list:
        if latex_symbol_str in latex_str:
            result_str = result_str.replace(latex_symbol_str, chr(latex_symbol_code_dict_v1[latex_symbol_str]))

    # 由于测试集和训练集的标注规范不统一，测试集中 可能有 比如 \left 不在字典当中的 字符
    # result_str = replace_latex_symbol_with_code(result_str)

    return result_str


def regularize_latex_v2(latex_str):
    """
    # 使用 replace_latex_symbol_with_code_v2
    :param latex_str:
    :return:
    """
    # latex_str = latex_str
    result = replace_latex_symbol_with_code_v2(latex_str)

    # 移除大括号{}
    result = result.replace('{', '').replace('}', '')
    # 移除空格
    result = result.replace(' ', '')
    # print(len(result))
    return result


def replace_if_contains(s, latex_str, s1):
    if s in latex_str:
        # print("@@@{}@@@ is in >>>{}<<< and will be replaced with @@@{}@@@".format(s, latex_str, s1))
        latex_str = latex_str.replace(s, s1)
        # print("final form: >>>{}<<<".format(latex_str))
    return latex_str


def latex_preprocess(latex_str):
    """
    替换存在多种Latex表示的字符为统一的Latex表示
    :param latex_str:
    :return:
    """
    # 替换中文
    # latex_str = re.sub(u"[\\u4e00-\\u9fa5]", "\\unknown", latex_str)


    # todo: 操作的顺序还可以再考虑下
    # 替换
    latex_str = replace_if_contains("×", latex_str, "\\times")
    latex_str = replace_if_contains("÷", latex_str, "\\div")
    latex_str = replace_if_contains("℃", latex_str, "^ { \circ } C")
    latex_str = replace_if_contains("\degree", latex_str, "^ { \circ }")
    latex_str = replace_if_contains("\geqslant", latex_str, "\geq")
    latex_str = replace_if_contains("\leqslant", latex_str, "\leq")
    latex_str = replace_if_contains("\le ", latex_str, "\leq ")  # todo "\le"位于字符串末尾替换不了，要单独写个正则匹配
    latex_str = replace_if_contains("^ { \prime }", latex_str, "'")
    latex_str = replace_if_contains("^ { \prime \prime }", latex_str, "' '")
    latex_str = replace_if_contains("—", latex_str, "-")
    latex_str = replace_if_contains("a r r a y", latex_str, "matrix")
    latex_str = replace_if_contains("a r r o w", latex_str, "\\rightarrow")  # v2
    latex_str = replace_if_contains("*", latex_str, "\\ast")
    latex_str = replace_if_contains("\\varnothing", latex_str, "\emptyset")
    latex_str = replace_if_contains("\O ", latex_str, "\emptyset ")  # todo "\O"位于字符串末尾替换不了，要单独写个正则匹配
    latex_str = replace_if_contains("\o ", latex_str, "\emptyset ")  # todo "\o"位于字符串末尾替换不了，要单独写个正则匹配
    latex_str = replace_if_contains("\parallel ", latex_str, "| | ")  # todo "\parallel"位于字符串末尾替换不了，要单独写个正则匹配,加空格是为了与 \parallelogram 区分
    latex_str = replace_if_contains("\\to", latex_str, "\\rightarrow")
    latex_str = replace_if_contains("\ldots", latex_str, "\dots")
    latex_str = replace_if_contains("~", latex_str, "\sim")  # 貌似训练集中 ~ 的标注都是错误的
    latex_str = replace_if_contains("\Box", latex_str, "\square")
    latex_str = replace_if_contains("\\not =", latex_str, "\\neq")
    latex_str = replace_if_contains("\\bigodot", latex_str, "\odot")
    latex_str = replace_if_contains("\\bot", latex_str, "\perp")
    latex_str = replace_if_contains("\\vec", latex_str, "\\overrightarrow")  # 和测试集统一 v2
    latex_str = replace_if_contains("，", latex_str, ",")
    latex_str = replace_if_contains("、", latex_str, ",")  # v2
    latex_str = replace_if_contains("。", latex_str, ".")  #  v2
    latex_str = replace_if_contains("（", latex_str, "(")
    latex_str = replace_if_contains("）", latex_str, ")")
    latex_str = replace_if_contains("〃", latex_str, '"')
    latex_str = replace_if_contains("′", latex_str, "'")
    latex_str = replace_if_contains("”", latex_str, '"')
    latex_str = replace_if_contains("＂", latex_str, '"')
    latex_str = replace_if_contains("“", latex_str, '"')
    latex_str = replace_if_contains("⌝", latex_str, "\lnot")
    latex_str = replace_if_contains("\ell", latex_str, "l")
    latex_str = replace_if_contains("\l ", latex_str, "l ")  # todo "\l"位于字符串末尾替换不了，要单独写个正则匹配

    latex_str = replace_if_contains("\\ \\ ", latex_str, "\\\\ ")  # 不知道有没有问题: \ \sqrt
    latex_str = re.sub(r'''\\ \\$''', "\\\\", latex_str)

    # 删除
    # latex_str = replace_if_contains("\prime", latex_str, "")  # 不能直接删除
    latex_str = replace_if_contains("\mathbf", latex_str, "")
    latex_str = replace_if_contains("\mathbf", latex_str, "")
    latex_str = replace_if_contains("\mathrm", latex_str, "")
    latex_str = replace_if_contains("\operatorname", latex_str, "")
    latex_str = replace_if_contains("\\textrm", latex_str, "")
    latex_str = replace_if_contains("\mathcal", latex_str, "")

    # 针对测试集合
    latex_str = replace_if_contains("\\mid", latex_str, "|")  # 训练集中都是 |，测试集中含有 mid 和 |, v2
    latex_str = replace_if_contains("{ m a t r i x }", latex_str, "{ matrix }")  # v2


    return latex_str


def edit_distance(pd_labels,gt_labels):
    l1 = len(pd_labels)
    l2 = len(gt_labels)
    t = np.zeros((l1+1,l2+1))
    for i in range(l1+1):
        t[i][0] = i
    for i in range(l2+1):
        t[0][i] = i
    for i in range(1,l1+1):
        for j in range(1,l2+1):
            m = min(t[i-1][j],t[i][j-1]) + 1
            t[i][j] = min(m, t[i-1][j-1] + (0 if pd_labels[i-1]==gt_labels[j-1] else 1))
    return t[l1][l2]


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


def ocr_use_bbk(img):
    url = 'http://test.eebbk.net/ocr/api/recognizeLatexLocal'
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
    url = 'http://bbkocr.eebbk.net/ocr/api/v1.0'
    # 测试环境ocr
    # url = 'http://test.eebbk.net/ocr/api/v1.0'
    # url = 'http://106.75.84.150:8258/ocr/api/v1.0'
    # url = 'http://39.108.125.133:8061/ocr/api/v1.0'
    # url = 'http://ocr-xtc.eebbk.net/ocr/api/v1.0'
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
                print(line['text'])
                result_str += ' %s' % line['text']

    return result_str


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


OCR_METHOD_HANVON = 1
OCR_METHOD_YOUDAO = 2
OCR_METHOD_BBK = 3
OCR_METHOD_ALL = 4


def ocr_formula(img, method):
    if method == OCR_METHOD_HANVON:
        ocr_func = ocr_use_hanvon
        get_func = get_hanvon_latex_result
    elif method == OCR_METHOD_YOUDAO:
        ocr_func = lambda x:ocr_use_youdao(x, mode='formula')
        get_func = get_youdao_latex_result
    elif method == OCR_METHOD_BBK:
        # ocr_func = ocr_use_bbk
        ocr_func = ocr_use_bbk_v_2
        get_func = get_bbk_latex_result
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


def test_formula(method_id, annotation_excel_path, output_dir, img_base_path):
    fn_and_labels = read_formula_annotation_excel(annotation_excel_path)

    detail_list = []
    acc_list = []
    for elem in fn_and_labels:
        fn = elem[0]
        gt_latex_str = latex_preprocess(elem[1])
        with open(os.path.join(img_base_path, fn), 'rb') as f:
            img_data = f.read()

        print('======')
        print('\tdealing file:%s' % fn)

        latex_str_use_ocr = ocr_formula(img_data, method_id)

        # 二义字符标准化
        standardize_latex_str_use_ocr = latex_preprocess(latex_str_use_ocr)

        rg_gt_latex_str = regularize_latex_v2(gt_latex_str)
        rg_latex_str_use_ocr = regularize_latex_v2(standardize_latex_str_use_ocr)

        edit_dist = edit_distance(rg_latex_str_use_ocr, rg_gt_latex_str)
        gt_len = len(rg_gt_latex_str)
        predict_len = len(rg_latex_str_use_ocr)
        max_len = gt_len if gt_len > predict_len else predict_len
        acc = 1 - edit_dist / max_len

        acc_list.append(acc)
        detail_list.append((fn, gt_latex_str, latex_str_use_ocr, standardize_latex_str_use_ocr, acc*100))

        print('------')
        print('\t%s' % fn)
        print('\t标准Latex: %s' % gt_latex_str)
        print('\t识别结果: %s' % latex_str_use_ocr)
        print('\t标准化的识别结果：%s' % standardize_latex_str_use_ocr)
        print('\t识别率: %f%%' % (acc * 100))

    print('------')
    print('%s 公式OCR平均绝对识别率为%f%%' % (get_method_name(method_id), np.average(acc_list) * 100))

    output_df = pd.DataFrame(detail_list, columns=['图片文件名', '标准Latex', '识别结果', '标准化的识别结果', '准确率'])

    output_df.to_excel(
        os.path.join(output_dir, get_output_excel_name(method_id)),
        encoding='utf-8'
    )


def get_method_name(method_id):
    if method_id == OCR_METHOD_HANVON:
        method_name = '汉王'
    elif method_id == OCR_METHOD_YOUDAO:
        method_name = '有道'
    elif method_id == OCR_METHOD_BBK:
        method_name = '步步高自研'
    else:
        raise Exception('unsupported method id, value: %d' % method_id)

    return method_name


def get_output_excel_name(method_id):
    current_time = time.time()
    return '%d_%s.xls' % (current_time, get_method_name(method_id))


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('method_id', type=int,
                        help='methodId可为1,2,3,4。1表示使用汉王的公式OCR，2为有道公式OCR，3为BBK自研OCR，4为测试所有')
    parser.add_argument('src_excel_path', type=str,
                        help='标注的excel文件地址')
    parser.add_argument('output_dir', type=str,
                        help='详情excel文件输出目录')
    parser.add_argument('img_base_path', type=str,
                        default='./',
                        help='可选参数，表示存放图片文件的目录路径，默认为当前目录')

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    if args.method_id == OCR_METHOD_HANVON:
        test_formula(OCR_METHOD_HANVON, args.src_excel_path, args.output_dir, args.img_base_path)
    elif args.method_id == OCR_METHOD_YOUDAO:
        test_formula(OCR_METHOD_YOUDAO, args.src_excel_path, args.output_dir, args.img_base_path)
    elif args.method_id == OCR_METHOD_BBK:
        test_formula(OCR_METHOD_BBK, args.src_excel_path, args.output_dir, args.img_base_path)
    elif args.method_id == OCR_METHOD_ALL:
        test_formula(OCR_METHOD_HANVON, args.src_excel_path, args.output_dir, args.img_base_path)
        test_formula(OCR_METHOD_YOUDAO, args.src_excel_path, args.output_dir, args.img_base_path)
        test_formula(OCR_METHOD_BBK, args.src_excel_path, args.output_dir, args.img_base_path)