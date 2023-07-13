# @File  : search_gui.py
# @Author: LiuXingsheng
# @Date  : 2020/12/11
# @Desc  :
import sys
from PyQt5 import QtWidgets
from  searchdiffcult import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot

class SearchDiffcult(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(SearchDiffcult, self).__init__()
        self.setupUi(self)


    @pyqtSlot
    def acc_onclick(self):
        print('')




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = SearchDiffcult()
    gui.show()
    sys.exit(app.exec_())