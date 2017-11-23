import os
import sys
import qtmodern.styles
import qtmodern.windows
import time

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.Qt import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *

from taopiaopiaoSpider import get_current_movies
from taopiaopiaoSpider import get_res
from taopiaopiaoSpider import taopiaopiao_spider
from taopiaopiaoSpider import get_movie_table_name
from taopiaopiaoSpider import get_table

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False

ID, CINEMA_NAME, ONDATE, ONTIME, TYPE, MALL_NAME, SEAT_STATUS, PRICE = range(8)

# 获取上映电影列表线程
class MovieThread(QThread):
    update = pyqtSignal(list)

    def __init__(self, parent = None):
        super(MovieThread, self).__init__(parent)

    def run(self):
        movie_list = get_current_movies()
        self.update.emit(movie_list)

# 爬虫线程
class SpiderThread(QThread):
    update = pyqtSignal()

    def __init__(self, parent = None):
        super(SpiderThread, self).__init__(parent)
        self.movie = ""

    def start_movie(self, movie):
        self.movie = movie
        self.start()

    def run(self):
        taopiaopiao_spider(self.movie)
        self.update.emit()

# 发送显示数据信号线程
class ShowThread(QThread):
    update = pyqtSignal(str)

    def run(self):
        while True:
            self.update.emit(get_res())
            time.sleep(1)


# 界面类
class SpiderDlg(QDialog):
    def __init__(self):
        super().__init__()
        self.movie = ""
        self.table = ""
        self.initUI()


    # 初始化
    def initUI(self):
        self.resize(960, 600)
        self.setWindowTitle("淘票票爬虫")
        self.center()

        # 线程
        self.spider_thread = SpiderThread()
        self.spider_thread.update.connect(self.spider_end)

        self.movie_thread = MovieThread()
        self.movie_thread.update.connect(self.bind_current_movie)
        self.movie_thread.start()

        self.show_thread = ShowThread()
        self.show_thread.update.connect(self.update_lbl_print)


        # 爬虫界面
        self.lbl_head = QLabel("正在获取上映的电影信息...", self)
        self.lbl_head.move(40, 55)

        self.cmb_current_movie = QComboBox(self)
        self.cmb_current_movie.move(40, 80)
        self.cmb_current_movie.resize(300, 40)
        self.cmb_current_movie.activated.connect(self.cmb_current_movie_clicked)

        btn_spider = QPushButton("启动爬虫", self)
        btn_spider.move(380, 80)
        btn_spider.resize(60, 40)
        btn_spider.clicked.connect(self.spider)

        self.lbl_print = QLabel(self)
        self.lbl_print.move(480, 80)
        self.lbl_print.resize(200, 40)

        # 数据界面
        self.cmb_data_movie = QComboBox(self)
        self.cmb_data_movie.move(40, 160)
        self.cmb_data_movie.resize(300, 40)
        self.cmb_data_movie.activated.connect(self.cmb_data_movie_clicked)

        self.model = QSqlTableModel(self)
        self.model.setSort(ID, Qt.AscendingOrder)
        self.model.setHeaderData(ID, Qt.Horizontal, "ID")
        self.model.setHeaderData(CINEMA_NAME, Qt.Horizontal, "CINEMA_NAME")
        self.model.setHeaderData(ONDATE, Qt.Horizontal, "ONDATE")
        self.model.setHeaderData(ONTIME, Qt.Horizontal, "ONTIME")
        self.model.setHeaderData(TYPE, Qt.Horizontal, "TYPE")
        self.model.setHeaderData(MALL_NAME, Qt.Horizontal, "MALL_NAME")
        self.model.setHeaderData(SEAT_STATUS, Qt.Horizontal, "SEAT_STATUS")
        self.model.setHeaderData(PRICE, Qt.Horizontal, "PRICE")
        self.model.select()

        self.view = QTableView(self)
        self.view.move(40, 220)
        self.view.resize(880, 300)
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setColumnHidden(ID, True)
        self.view.resizeColumnsToContents()

        self.bind_data_movie()
    @pyqtSlot(str)
    def update_lbl_print(self, text):
        self.lbl_print.setText(text)

    @pyqtSlot(int)
    def cmb_current_movie_clicked(self, index):
        self.movie = self.cmb_current_movie.itemText(index)


    @pyqtSlot()
    def spider(self):
        self.spider_thread.start_movie(self.movie)
        self.show_thread.start()

    @pyqtSlot()
    def spider_end(self):
        self.bind_data_movie()
        self.show_thread.quit()

    @pyqtSlot(list)
    # 获取当前上映的电影列表，绑定下拉单控件
    def bind_current_movie(self, movie_list):
        self.cmb_current_movie.clear()
        self.lbl_head.setText("当前上映的电影")
        if len(movie_list) > 0:
            self.movie = movie_list[0][0]
        for movie in movie_list:
            self.cmb_current_movie.addItem(movie[0])

        self.bind_data_movie()

    @pyqtSlot(int)
    def cmb_data_movie_clicked(self, index):
        self.table = get_table(self.cmb_data_movie.itemText(index))
        self.model.setTable(self.table)
        self.model.select()

    def bind_data_movie(self):
        self.cmb_data_movie.clear()
        movie_list = get_movie_table_name()
        for movie in movie_list:
            self.cmb_data_movie.addItem(movie[0])
        if len(movie_list) > 0:
            self.table = get_table(movie_list[0][0])
            self.cmb_data_movie_clicked(0)


    # 居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)  # 创建app对象

    filename = os.path.join(os.path.dirname(__file__), "reference.db")
    db = QSqlDatabase.addDatabase("QMYSQL")
    db.setHostName("localhost")
    db.setUserName("root")
    db.setPassword("0000")
    db.setDatabaseName("TaoPiaoPiaoDB")
    db.open()
    if not db.open():
        QMessageBox.warning(None, "Reference Data",
                            "Database Error: {0}".format(db.lastError().text()))
        sys.exit(1)

    win = SpiderDlg()  # 创建对话框对象
    qtmodern.styles.dark(app)
    mw=qtmodern.windows.ModernWindow(win)
    mw.show()
    sys.exit(app.exec_())