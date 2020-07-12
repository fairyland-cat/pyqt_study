import sys
from Ui_convert import Ui_MainWindow  # 调用ui模块中的Ui_MainWindow()类
from PyQt5 import QtWidgets
from functools import partial


class MyMainWindow():
    def __init__(self):
        super(MyMainWindow, self).__init__()
        app = QtWidgets.QApplication(sys.argv)
        self.mian_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mian_window)
        self.mian_window.show()
        self.ui.radioButton_3.pressed.connect(partial(self.update_text, self.ui.radioButton_3))
        self.ui.radioButton_2.pressed.connect(partial(self.update_text, self.ui.radioButton_2))
        self.ui.radioButton.pressed.connect(partial(self.update_text, self.ui.radioButton))

        self.ui.radioButton_3.pressed.connect(self.convert)
        self.ui.radioButton_2.pressed.connect(self.convert)
        self.ui.radioButton.pressed.connect(self.convert)

        self.ui.lineEdit.returnPressed.connect(self.convert)
        sys.exit(app.exec_())

    def update_text(self, radioButton):
        self.ui.label_2.setText(radioButton.text() + "数")
        pass

    def convert(self):
        input_text = self.ui.lineEdit.text()
        if not input_text:
            return
        if len(input_text) > 12:
            return QtWidgets.QMessageBox.critical(self.mian_window, "错误", "只可以输入长度12以内的数字！", QtWidgets.QMessageBox.Yes)
        if not input_text.isdigit():
            return QtWidgets.QMessageBox.critical(self.mian_window, "错误", "只可以输入数字！", QtWidgets.QMessageBox.Yes)

        input_text = int(input_text)
        convert_model = self.ui.label_2.text()
        if convert_model == "八进制数":
            self.ui.lineEdit_2.setText("{0:o}".format(input_text))
        if convert_model == "二进制数":
            self.ui.lineEdit_2.setText("{0:b}".format(input_text))
        if convert_model == "十六进制数":
            self.ui.lineEdit_2.setText("{0:x}".format(input_text))
        pass


if __name__ == "__main__":
    mian_window = MyMainWindow()
