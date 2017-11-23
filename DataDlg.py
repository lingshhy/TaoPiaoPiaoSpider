import os
import sys
import qtmodern.styles
import qtmodern.windows
from PyQt5.QtCore import (QFile, QVariant, Qt, pyqtSlot)
from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QDialog, QDialogButtonBox, QMenu,
        QMessageBox, QTableView, QVBoxLayout, QComboBox, QPushButton)
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel)

from taopiaopiaoSpider import get_movie_table_name

MAC = True
try:
    from PyQt5.QtGui import qt_mac_set_native_menubar
except ImportError:
    MAC = False


ID, CINEMA_NAME, ONDATE, ONTIME, TYPE, MALL_NAME, SEAT_STATUS, PRICE = range(8)


class ReferenceDataDlg(QDialog):

    def __init__(self, parent=None):
        super(ReferenceDataDlg, self).__init__(parent)
        self.movie = ""

        self.resize(960, 600)
        self.setWindowTitle("淘票票数据")
        self.center()


        # 数据界面
        self.cmb_data_movie = QComboBox(self)
        self.cmb_data_movie.move(40, 80)
        self.cmb_data_movie.resize(300, 40)
        self.cmb_data_movie.activated.connect(self.cmb_current_movie_clicked)

        self.btn_show = QPushButton("显示数据", self)
        self.btn_show.move(380, 80)
        self.btn_show.resize(60, 40)
        self.btn_show.clicked.connect(self.show_data)

        self.bind_data_movie()

        self.model = QSqlTableModel(self)
        #self.model.setTable("movieslist")
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
        self.view.move(40,160)
        self.view.resize(200,160)
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setColumnHidden(ID, True)
        self.view.resizeColumnsToContents()

        buttonBox = QDialogButtonBox()
        addButton = buttonBox.addButton("&Add",
                QDialogButtonBox.ActionRole)
        deleteButton = buttonBox.addButton("&Delete",
                QDialogButtonBox.ActionRole)
        sortButton = buttonBox.addButton("&Sort",
                QDialogButtonBox.ActionRole)
        if not MAC:
            addButton.setFocusPolicy(Qt.NoFocus)
            deleteButton.setFocusPolicy(Qt.NoFocus)
            sortButton.setFocusPolicy(Qt.NoFocus)

        menu = QMenu(self)
        sortByCategoryAction = menu.addAction("Sort by &CINEMA_NAME")
        sortByDescriptionAction = menu.addAction("Sort by &ONDATE")
        sortByIDAction = menu.addAction("Sort by &ID")
        sortButton.setMenu(menu)
        closeButton = buttonBox.addButton(QDialogButtonBox.Close)

        # layout = QVBoxLayout()
        # layout.addWidget(self.view)
        # layout.addWidget(buttonBox)
        # self.setLayout(layout)

        addButton.clicked.connect(self.addRecord)
        deleteButton.clicked.connect(self.deleteRecord)
        sortByCategoryAction.triggered.connect(lambda:self.sort(CINEMA_NAME))
        sortByDescriptionAction.triggered.connect(lambda:self.sort(ONDATE))
        sortByIDAction.triggered.connect(lambda:self.sort(ID))
        closeButton.clicked.connect(self.accept)
        self.setWindowTitle("Reference Data")

    # 获取数据库中的电影表，绑定下拉单控件
    def bind_data_movie(self):
        movie_list = get_movie_table_name()
        if len(movie_list) > 0:
            self.movie = movie_list[0][0]
        for movie in movie_list:
            self.cmb_data_movie.addItem(movie[0])
        self.cmb_data_movie.addItem("movieslist")

    @pyqtSlot(int)
    def cmb_current_movie_clicked(self, index):
        self.movie = self.cmb_data_movie.itemText(index)

    @pyqtSlot()
    def show_data(self):
        print(self.movie)
        self.model.setTable(self.movie)
        self.model.select()

    # 居中
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def addRecord(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, CATEGORY)
        self.view.setCurrentIndex(index)
        self.view.edit(index)


    def deleteRecord(self):
        index = self.view.currentIndex()
        if not index.isValid():
            return
        record = self.model.record(index.row())
        category = record.value(CATEGORY)
        desc = record.value(SHORTDESC)
        if (QMessageBox.question(self, "Reference Data",
                ("Delete {0} from category {1}?"
                .format(desc,category)),
                QMessageBox.Yes|QMessageBox.No) ==
                QMessageBox.No):
            return
        self.model.removeRow(index.row())
        self.model.submitAll()
        self.model.select()


    def sort(self, column):
        self.model.setSort(column, Qt.AscendingOrder)
        self.model.select()


def main():
    app = QApplication(sys.argv)
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
    form = ReferenceDataDlg()
    qtmodern.styles.dark(app)
    mw=qtmodern.windows.ModernWindow(form)
    mw.show()
    sys.exit(app.exec_())

main()