# @File  : ocrTool.py
# @Author: LiuXingsheng
# @Date  : 2019/3/7
# @Desc  :
import requests, os, demjson


def recognizeLocal():
    """
    自研Ocr接口
    :return:
    """
    picList = []
    fileList = os.listdir(os.getcwd())
    for file in fileList:
        if file.endswith('.bmp'):
            picList.append(file)
        else:
            continue
    url = 'http://test.eebbk.net/ocr/api/recognizeLocal'
    for file in picList:
        fileparam = {'url': open(file, 'rb')}
        result = requests.post(url=url, files=fileparam)
        print(result.text)


def not_empty(s):
    return s and s.strip()


def test():
    s = 'q'
    t = 'w'
    print('--------------')
    print(t and s)
    print('--------------')
    var = (s and s.strip())
    # print(var)
    n = 3
    vair = (n % 2 == 1)
    # print(vair)


def main():
    # recognizeLocal()
    test()
    print(list(filter(not_empty, ['a', '', 'c'])))


if __name__ == '__main__':
    main()
