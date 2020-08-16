import sys

from PyQt5 import QtCore
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery, QSqlRelationalTableModel, QSqlRelationalDelegate)
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QTableView, QHBoxLayout, QVBoxLayout)


class Wishlist(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setMinimumSize(500, 400)
        self.setWindowTitle("My Wishlist")
        self.createConnection()
        self.createTable()
        self.setupWidgets()

        self.show()

    def createConnection(self):
        database = QSqlDatabase.addDatabase("QSQLITE")
        database.setDatabaseName("w_list.db")

        if not database.open():
            print("Unable to open")
            sys.exit(1)

    def createTable(self):
        self.model = QSqlRelationalTableModel()
        self.model.setTable("w_list")
        self.model.setHeaderData(self.model.fieldIndex('id'), QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(self.model.fieldIndex('title'), QtCore.Qt.Horizontal, "Title")
        self.model.setHeaderData(self.model.fieldIndex('price'), QtCore.Qt.Horizontal, "Price")
        self.model.setHeaderData(self.model.fieldIndex('comment'), QtCore.Qt.Horizontal, "Comment")
        self.model.setHeaderData(self.model.fieldIndex('website'), QtCore.Qt.Horizontal, "Website")

        self.model.select()

    def setupWidgets(self):
        add_button = QPushButton("Add wish")
        add_button.clicked.connect(self.addWish)

        del_button = QPushButton("Delete wish")
        del_button.clicked.connect(self.delWish)

        button_h_box = QHBoxLayout()
        button_h_box.addWidget(add_button)
        button_h_box.addWidget(del_button)
        button_h_box.addStretch()

        edit_buttons = QWidget()
        edit_buttons.setLayout(button_h_box)

        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        # self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSelectionMode(QTableView.SingleSelection)
        self.table_view.setSelectionBehavior(QTableView.SelectRows)
        # Instantiate the delegate
        delegate = QSqlRelationalDelegate(self.table_view)
        self.table_view.setItemDelegate(delegate)

        main_v_box = QVBoxLayout()
        main_v_box.addWidget(edit_buttons)
        main_v_box.addWidget(self.table_view)
        self.setLayout(main_v_box)

    def addWish(self):
        last_row = self.model.rowCount()
        self.model.insertRow(last_row)

        id = 0
        query = QSqlQuery()
        query.exec_("SELECT MAX (id) FROM w_list")
        if query.next():
            id = int(query.value(0))

    def delWish(self):
        current_item = self.table_view.selectedIndexes()
        for index in current_item:
            self.model.removeRow(index.row())
        self.model.select()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Wishlist()
    sys.exit(app.exec_())
