import os
import sys
import qtmodern.styles
import qtmodern.windows

from PyQt5.QtCore import (QFile, QVariant, Qt, pyqtSlot)
from PyQt5.QtWidgets import QDialog, QApplication, QDesktopWidget, QPushButton,\
    QComboBox, QMenuBar, QMenu, QAction, QTableWidget, QTableWidgetItem, QLabel, QMessageBox
from PyQt5 import QtGui, QtCore

from taopiaopiaoSpider import get_current_movies
from taopiaopiaoSpider import taopiaopiao_spider

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

# 界面类
class SpiderDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.movie = ""
        self.initUI()


    # 初始化
    def initUI(self):
        self.resize(960, 600)
        self.setWindowTitle("淘票票爬虫")
        self.center()


        # 爬虫界面
        self.cmb_current_movie = QComboBox(self)
        self.cmb_current_movie.move(40, 80)
        self.cmb_current_movie.resize(300, 40)
        self.cmb_current_movie.activated.connect(self.cmb_current_movie_clicked)

        btn_spider = QPushButton("启动爬虫", self)
        btn_spider.move(380, 80)
        btn_spider.resize(60, 40)
        btn_spider.clicked.connect(self.spider)

        lbl_print = QLabel(self)
        lbl_print.move(40, 160)
        lbl_print.resize(200, 300)

        self.bind_current_movie()


    @pyqtSlot(int)
    def cmb_current_movie_clicked(self, index):
        self.movie = self.cmb_current_movie.itemText(index)


    @pyqtSlot()
    def spider(self):
        taopiaopiao_spider(self.movie)

    # 获取当前上映的电影列表，绑定下拉单控件
    def bind_current_movie(self):
        movie_list = get_current_movies()
        if len(movie_list) > 0:
            self.movie = movie_list[0][0]
        for movie in movie_list:
            self.cmb_current_movie.addItem(movie[0])

    # 居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建app对象
    win = SpiderDlg()  # 创建对话框对象
    qtmodern.styles.dark(app)
    mw=qtmodern.windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())