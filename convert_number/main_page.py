import sys
from Ui_convert import Ui_MainWindow  # 调用ui模块中的Ui_MainWindow()类
from PyQt5 import QtWidgets
# Qt设计师上第一步创建时选择了Main Window时选择QMainWindow
# from PyQt5.QtWidgets import QApplication, QMainWindow
# Qt设计师上第一步创建时选择了Dialog时选择QDialog
# Qt设计师上第一步创建时选择了Widget时选择QWidget


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
