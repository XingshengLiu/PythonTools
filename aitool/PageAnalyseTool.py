# @File  : PageAnalyseTool.py
# @Author: LiuXingsheng
# @Date  : 2019/7/24
# @Desc  :

import os
import cv2


def show_test(img, img_name='img', is_resized=False):
    # show image
    # if is_resized:
    #     img = cv2.resize(img, (1000, 1000), interpolation=cv2.INTER_CUBIC)
    cv2.imshow(img_name, img)


if __name__ == '__main__':
    imgPath = 'test'
    imgs = os.listdir(imgPath)
    num = 1
    for item in imgs:
        picPath = imgPath + '/' + item
        print(picPath)
        img = cv2.imread(picPath)
        show_test(img, img_name='img', is_resized=True)
        while True:
            key = cv2.waitKey()
            line = item
            if key == 32:  # 空格 框对
                line += '--->' + '框对' + '\n'
                print('[{}]:{}'.format(num, line))
                break
            elif key == 120:  # 小写x 下边界
                line += '--->' + '下边界' + '\n'
                print('[{}]:{}'.format(num, line))
                break
            elif key == 100:  # 小写d 框多
                line += '--->' + '框多' + '\n'
                print('[{}]:{}'.format(num, line))
                break
            elif key == 115:  # 小写s 框少
                line += '--->' + '框少' + '\n'
                print('[{}]:{}'.format(num, line))
                break
            elif key == 119:  # 小写w 无效点击
                line += '--->' + '无效点击' + '\n'
                print('[{}]:{}'.format(num, line))
                break
            elif key == 99:  # 小写c 框错
                line += '--->' + '框错' + '\n'
                print('[{}]:{}'.format(num, line))
                break
            else:
                print('点击错误请重新输入：空格-->框对  小写x-->下边界   小写d-->框多   小写s-->框少 小写w-->无效点击 小写c-->框错 ')
        num = num + 1
        with open('test_report_relabel.txt', 'a') as fp:
            fp.write(line)
