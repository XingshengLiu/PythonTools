import os
import shutil

import requests


def get_search_results(path):
    url = "http://172.28.195.130:8081/padSearch/uploadFile"
    # url = 'http://106.75.114.75:5000/encode'
    with open(path, 'rb') as f:
        img_data = f.read()
    file_obj = {'img_stream': img_data}
    r = requests.post(url, files=file_obj)

    return r.json()


def get_boyun_results(path):
    url = "http://47.103.71.100:18080/Ise/cloudAtlas/retrieve_image_bbk"
    with open(path, 'rb') as f:
        img_data = f.read()
    file_obj = {'img_stream': img_data}

    data_obj = {'db_uid': "ise_bbk_01",
                'db_seckey': "ise_bbk_01",
                'pt_x': -1,
                'pt_y': -1,
                'wp': 'bookId',
                'ws': '',
                'searchType': 2}

    r = requests.post(url, data=data_obj, files=file_obj)

    return r.json()


def auto_test():
    test_dir = r'\\172.28.1.23\教育电子事业部-软件项目\APP产品项目【家教机】\2 学习类\01【学习类·同步业务】\#一点一问项目\英语点读\04 测试\专项测试\测试素材\标准测试集\测试集'
    correct_file = 0
    false_file = []
    total_file = 0

    for file_tuple in os.walk(test_dir):
        for img_file in file_tuple[-1]:
            if img_file.endswith('.jpg'):
                abs_img_file = os.path.join(file_tuple[0], img_file)
                res = get_search_results(abs_img_file)
                try:
                    top_res = res['data'][0]
                    # for one_res in res['data']:
                    #     if str(one_res['bookId']) in img_file:
                    #         top_res = one_res
                    #         break
                    label = os.path.splitext(img_file)[0].split('#')
                    book_id = label[0]
                    page_id = label[1]
                    try:
                        if int(top_res['bookId']) == int(book_id) and int(top_res["pageNo"]) == int(page_id):
                            print("True:{},Pred:{},Success".format(os.path.splitext(img_file)[0], str(top_res['bookId']) + "#" + str(top_res["pageNo"])))
                            correct_file += 1
                        else:
                            false_file.append(os.path.join(abs_img_file))
                            print("True:{},Pred:{},False".format(os.path.splitext(img_file)[0], str(top_res['bookId']) + "#" + str(top_res["pageNo"])))
                    except ValueError:
                        false_file.append(os.path.join(abs_img_file))
                        print("True:{},Pred:{},False".format(os.path.splitext(img_file)[0], str(top_res['bookId']) + "#" + str(top_res["pageNo"])))
                except KeyError:
                    print("True:{},Pred:-1,False".format(os.path.splitext(img_file)[0]))

                total_file += 1

    print("Predict result:{}".format(float(correct_file) / total_file))
    with open(r'D:\12306Bypass\test.txt', 'w') as f:
        for img_file in false_file:
            f.writelines(img_file)


def get_fail_list(fail_txt):
    with open(fail_txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            src_path = line.replace('\n', '').replace('\r', '')
            if src_path.endswith('.jpg'):
                print(src_path)
                file_name = os.path.split(src_path)[-1]
                shutil.copyfile(src_path, os.path.join(r'C:\Users\20258552\Desktop\fail', file_name))


def exist_book(path):
    exist_book_list = []
    for _, _, page_list in os.walk(path):
        if len(page_list) > 0:
            name_list = page_list[0].split('#')
            if len(name_list) > 1:
                exist_book_list.append(name_list[0])


    print(set(exist_book_list))


def rename_data():
    import pandas as pd
    df = pd.read_excel(r"C:\Users\20258552\Desktop\入库列表.xls")

    root_dir = r"\\172.28.1.23\互联网技术部\AI技术平台科\图搜-平板\测试集\05-左旋转"
    for sub_dir in os.listdir(root_dir):
        abs_sub_dir = os.path.join(root_dir, sub_dir)
        if os.path.isdir(abs_sub_dir):
            for book_dir in os.listdir(abs_sub_dir):
                book_name = book_dir.split("#")[-1]
                book_id = df[df['书本名'] == book_name]['书本ID'].values[0]

                new_dir = str(book_id) + "#" + book_name
                abs_new_dir = os.path.join(abs_sub_dir, new_dir)
                os.rename(os.path.join(abs_sub_dir, book_dir), abs_new_dir)

                for img_path in os.listdir(abs_new_dir):
                    if img_path.endswith('.jpg') or img_path.endswith('.txt'):
                        new_path_list = img_path.split("#")[1:]
                        new_path_list.insert(0, str(book_id))
                        new_path = "#".join(new_path_list)

                        os.rename(os.path.join(abs_new_dir, img_path), os.path.join(abs_new_dir, new_path))


if __name__ == '__main__':
    auto_test()

    # import shutil
    # book_name = "809 清华小学英语三年级上册(一年级起点)(通用2014-2018年)"
    # root_src_dir = r"\\172.28.1.23\ai数据素材\AI测试素材库\已标注素材\图像\以图搜书\已裁剪"
    # root_dst_dir = r"G:\test_set\以图搜书测试集"
    #
    # for s_dir in os.listdir(root_src_dir):
    #     src_dir = os.path.join(os.path.join(root_src_dir, s_dir), book_name)
    #     dst_dir = os.path.join(os.path.join(root_dst_dir, s_dir), book_name)
    #
    #     for f in os.listdir(src_dir):
    #         f_list = f.split("#")
    #         if int(f_list[1]) - 3 >= 0:
    #             new_f = f_list[0] + "#" + str(int(f_list[1]) - 3) + "#" + f_list[2]
    #             shutil.copyfile(os.path.join(src_dir, f), os.path.join(dst_dir, new_f))


