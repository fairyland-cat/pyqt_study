import sys

from PyQt5.QtCore import Qt
from Ui_manage import Ui_MainWindow  # 调用ui模块中的Ui_MainWindow()类
from PyQt5 import QtWidgets
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


class Manage():
    def __init__(self):
        super(Manage, self).__init__()
        app = QtWidgets.QApplication(sys.argv)
        self.mian_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mian_window)
        self.mian_window.show()
        # 创建/连接数据库
        self.create_database()
        # 创建model
        model = self.create_mode()
        self.ui.tableView.setModel(model)
        self.db.close()
        sys.exit(app.exec_())

    def create_database(self):
        # 指定数据库类型
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        # 设置数据库名称
        self.db.setDatabaseName("./study_manage/management_system.db")
        if not self.db.open():
            return QtWidgets.QMessageBox.critical(self.mian_window, "错误", "只可以输入长度12以内的数字！", QtWidgets.QMessageBox.Yes)
        self.query = QSqlQuery()
        # 创建专业表
        self.query.exec("""
                   CREATE TABLE
                    IF NOT EXISTS 'major'(
                        'id' integer PRIMARY KEY autoincrement,
                        'name' VARCHAR(100) NOT NULL,
                        'instructor' VARCHAR(40) NOT NULL,
                        'institute' VARCHAR(100),
                        'date_create' DATETIME,
                        'date_update' DATETIME,
                        'date_delete' DATETIME
                    );
                   """)
        # 创建学生表
        self.query.exec("""
                   CREATE TABLE
                    IF NOT EXISTS 'student'(
                        'id' integer PRIMARY KEY autoincrement,
                        'name' VARCHAR(100) NOT NULL,
                        'sex' VARCHAR(40) NOT NULL,
                        'age' integer,
                        'birthday 'DATE,
                        'major_id' VARCHAR(40) NOT NULL,
                        'date_create' DATETIME,
                        'date_update' DATETIME,
                        'date_delete' DATETIME,
                        FOREIGN KEY(major_id) REFERENCES major(id)
                    );
                   """)
        pass

    def create_mode(self):
        model = QSqlTableModel()
        model.setTable("student")
        # model.setEditStrategy()
        model.select()
        model.setHeaderData(0, Qt.Horizontal, "学号")
        model.setHeaderData(1, Qt.Horizontal, "姓名")
        model.setHeaderData(2, Qt.Horizontal, "性别")
        model.setHeaderData(3, Qt.Horizontal, "年龄")
        model.setHeaderData(4, Qt.Horizontal, "出生日期")
        return model


if __name__ == "__main__":
    Manage()
