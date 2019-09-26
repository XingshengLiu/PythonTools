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
    test_dir = r'\\172.28.1.23\互联网技术部\AI技术平台科\图搜-平板\测试集'
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
                    for one_res in res['data']:
                        if str(one_res['bookId']) in img_file:
                            top_res = one_res
                            break
                    label = os.path.splitext(img_file)[0].split('#')
                    book_id = label[0]
                    page_id = label[1]
                    if int(top_res['bookId']) == int(book_id) and int(top_res["pageNo"]) == int(page_id):
                        print("True:{},Pred:{},Success".format(os.path.splitext(img_file)[0], str(top_res['bookId']) + "#" + str(top_res["pageNo"])))
                        correct_file += 1
                    else:
                        false_file.append(os.path.join(abs_img_file))
                        print("True:{},Pred:{},False".format(os.path.splitext(img_file)[0], str(top_res['bookId']) + "#" + str(top_res["pageNo"])))
                except KeyError:
                    print("True:{},Pred:-1,False".format(os.path.splitext(img_file)[0]))

                total_file += 1

    print("Predict result:{}".format(float(correct_file) / total_file))
    with open(r'F:\AI搜相关结果\test.txt', 'w') as f:
        for img_file in false_file:
            f.writelines(img_file)


if __name__ == '__main__':
    auto_test()


