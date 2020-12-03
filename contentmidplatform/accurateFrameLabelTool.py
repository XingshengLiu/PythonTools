# @File  : accurateFrameLabelTool.py
# @Author: LiuXingsheng
# @Date  : 2020/8/18
# @Desc  :

import os
import tkinter
import tkinter.messagebox
from tkinter import StringVar
from tkinter import END
import xlsxwriter
import xlrd

from PIL import Image, ImageTk

dirpaht = os.getcwd()
piclist = []
# 创建tkinter应用程序窗口
root = tkinter.Tk()
# 设置窗口的大小和位置
root.geometry('1200x700+40+30')
# 不允许改变窗口的大小
root.resizable(False, False)
# 设置窗口主题
root.title('使用Label显示图片')

# 获取当前文件夹中所有图片文件列表
suffix = ('.jpg', '.bmp', '.png')
pics = []
contentdata = xlrd.open_workbook(os.path.join(dirpaht,'test.xlsx'))
sheet = contentdata.sheets()[0]
rows = sheet.nrows
for row in range(rows):
    pics.append(sheet.cell_value(row, 0))
# pics = [p for p in os.listdir(dirpaht) if p.endswith(suffix)]
# pics.sort(key=lambda item: int(item[:item.index('.')]))


current = 0

v1 = StringVar()

# 标注内容的文本框
etext = tkinter.Entry(root, textvariable=v1)
etext.pack(padx=10, pady=10)
etext.place(x=700, y=550, width=80, height=30)



def changePic(flag):
    '''flag参数作为上下图片的调节 -1代表上一张 1代表下一个'''
    global current
    new = current + flag

    if new < 0:
        tkinter.messagebox.showerror('', '这已经是第一张图片了')
    elif new >= len(pics):
        tkinter.messagebox.showerror('', '这已经是最后一张图片了')
    else:
        # 获取要切换图片文件名
        pic = pics[new]

        # 创建Image对象并进行缩放
        im = Image.open(dirpaht + r'/{}'.format(pic))
        w, h = im.size

        # 这里假设用来显示图片的Label组件尺寸为 400x600
        # if w > 400:
        #     h = int(h * 400 / w)
        #     w = 400
        # if h > 600:
        #     w = int(w * 600 / h)
        #     h = 600
        im = im.resize((w, h))
        # 创建image对象，并设置Label组件图片
        im1 = ImageTk.PhotoImage(im)
        lbPic['image'] = im1
        lbPic.image = im1

        current = new


# 上一张的按钮
def btnPreClick():
    changePic(-1)

btnPre = tkinter.Button(root, text='上一张', command=btnPreClick)
btnPre.place(x=100, y=650, width=80, height=30)


# 下一张按钮
def btnNextClick():
    changePic(1)
    piclist.append([pics[current], str(v1.get())])
    with open(os.path.join(dirpaht,'label.txt'),'a') as fwrite:
        fwrite.write(pics[current] + '--->' + str(v1.get()) + '\n')
        fwrite.flush()
    etext.delete(0, END)


def writecontent():
    workbook = xlsxwriter.Workbook(dirpaht + '\\' + '图片名.xlsx')
    ws = workbook.add_worksheet(u'sheet1')
    for row in range(len(piclist)):
        for column in range(len(piclist[row])):
            ws.write(row, column, piclist[row][column])
    workbook.close()
    tkinter.messagebox.showinfo(title='来自窗口的消息', message='写入完成')


btnNext = tkinter.Button(root, text='下一张', command=btnNextClick)
btnNext.place(x=800, y=650, width=80, height=30)

btnOver = tkinter.Button(root, text='结束测试', command=writecontent)
btnOver.place(x=900, y=650, width=80, height=30)

# 用来显示图片的Label组件
lbPic = tkinter.Label(root, text='test', width=1000, height=300)
changePic(0)
lbPic.place(x=10, y=300, width=1000, height=300)


# 启动
root.mainloop()
