# @File  : pyqttest.py
# @Author: LiuXingsheng
# @Date  : 2019/7/30
# @Desc  :

import sys, os
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *
from PyQt5 import QtCore


# 定义窗口函数window
def window():
    # # 我事实上不太明白干嘛要这一句话，只是pyqt窗口的建立都必须调用QApplication方法
    # app = QtWidgets.QApplication(sys.argv)
    # # 新建一个窗口，名字叫做w
    # w = QtWidgets.QWidget()
    # # 定义w的大小
    # w.setGeometry(100, 100, 500, 500)
    # # 给w一个Title
    # w.setWindowTitle('lesson 2')
    # 在窗口w中，新建一个lable，名字叫做l1
    btn = QtWidgets.QPushButton(w)
    btn.clicked.connect(btn_click)
    btn.setGeometry(10, 10, 40, 20)
    l1.setGeometry(50, 50, 200, 200)
    # 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
    w.show()
    app.exit(app.exec_())


def btn_click(flag):
    with open('result_test.txt', 'r')as f:
        result = f.readline()
    if int(result) < 4:
        print(result)
        showpic('test/' + pics[int(result)], int(result))
    else:
        pass


def showpic(pic, flag):
    print(pic)
    png = QtGui.QPixmap(pic)
    myScaledPixmap = png.scaled(l1.size(), QtCore.Qt.KeepAspectRatio)
    # 在l1里面，调用setPixmap命令，建立一个图像存放框，并将之前的图像png存放在这个框框里。
    l1.setPixmap(myScaledPixmap)
    with open('result_test.txt', 'w')as f:
        f.write(str(flag + 1))


with open('result_test.txt', 'w')as f:
    f.write('0')
pics = os.listdir('test/')
app = QtWidgets.QApplication(sys.argv)
# 新建一个窗口，名字叫做w
w = QtWidgets.QWidget()
# 定义w的大小
w.setGeometry(100, 100, 1000, 1000)
# 给w一个Title
w.setWindowTitle('lesson 2')
l1 = QtWidgets.QLabel(w)
btn = QtWidgets.QPushButton(w)
btn.clicked.connect(btn_click)
btn.setGeometry(10, 10, 40, 20)
l1.setGeometry(50, 50, 500, 500)
# 调用QtGui.QPixmap方法，打开一个图片，存放在变量png中
w.show()
app.exit(app.exec_())
# window()
