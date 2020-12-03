# @File  : pyqt_boxlayout.py
# @Author: LiuXingsheng
# @Date  : 2020/8/21
# @Desc  :

import sys
from PyQt5.QtWidgets import  QWidget,QPushButton,QHBoxLayout,QVBoxLayout,QApplication
from PyQt5 import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()

    def initUi(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        hbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.setGeometry(300,300,300,150)
        self.setWindowTitle("Buttons")
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
