import sys
from Ui_calculator import Ui_mainWindow  # 调用ui模块中的Ui_MainWindow()类
from PyQt5 import QtWidgets
from functools import partial


class CalculatorMainWindow():
    def __init__(self):
        super(CalculatorMainWindow, self).__init__()
        app = QtWidgets.QApplication(sys.argv)
        self.mian_window = QtWidgets.QMainWindow()
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self.mian_window)
        self.mian_window.show()
        # 输入
        self.left_number = ""
        self.operator_type = ""
        self.right_number = ""

        # 绑定事件
        self.ui.button_1.clicked.connect(partial(self.calculator, self.ui.button_1.text()))
        self.ui.button_2.clicked.connect(partial(self.calculator, self.ui.button_2.text()))
        self.ui.button_3.clicked.connect(partial(self.calculator, self.ui.button_3.text()))
        self.ui.button_4.clicked.connect(partial(self.calculator, self.ui.button_4.text()))
        self.ui.button_5.clicked.connect(partial(self.calculator, self.ui.button_5.text()))
        self.ui.button_6.clicked.connect(partial(self.calculator, self.ui.button_6.text()))
        self.ui.button_7.clicked.connect(partial(self.calculator, self.ui.button_7.text()))
        self.ui.button_8.clicked.connect(partial(self.calculator, self.ui.button_8.text()))
        self.ui.button_9.clicked.connect(partial(self.calculator, self.ui.button_9.text()))
        self.ui.button_0.clicked.connect(partial(self.calculator, self.ui.button_0.text()))

        self.ui.button_o.clicked.connect(partial(self.calculator, self.ui.button_o.text()))
        self.ui.button_t.clicked.connect(partial(self.calculator, self.ui.button_t.text()))
        self.ui.button_s.clicked.connect(partial(self.calculator, self.ui.button_s.text()))
        self.ui.button_e.clicked.connect(partial(self.calculator, self.ui.button_e.text()))
        self.ui.button_l.clicked.connect(partial(self.calculator, self.ui.button_l.text()))
        self.ui.button_c.clicked.connect(partial(self.calculator, self.ui.button_c.text()))
        self.ui.button_ce.clicked.connect(partial(self.calculator, self.ui.button_ce.text()))
        self.ui.button_b.clicked.connect(partial(self.calculator, self.ui.button_b.text()))

        self.ui.pushButton_12.clicked.connect(partial(self.calculator, self.ui.pushButton_12.text()))
        self.ui.pushButton_16.clicked.connect(partial(self.calculator, self.ui.pushButton_16.text()))
        self.ui.pushButton_20.clicked.connect(partial(self.calculator, self.ui.pushButton_20.text()))
        self.ui.pushButton_21.clicked.connect(partial(self.calculator, self.ui.pushButton_21.text()))
        self.ui.pushButton_23.clicked.connect(partial(self.calculator, self.ui.pushButton_23.text()))

        sys.exit(app.exec_())

    def calculator(self, text):
        if text == "C":
            self.ui.label.setText("")
            self.ui.label_2.setText("")
            return
        if not self.left_number:
            if text.isdigit():
                self.left_number += text
                return self.ui.label_2.setText(self.left_number)
            if text in ("+", "-", "*", "/"):
                return
        if not self.operator_type:
            if text.isdigit():
                self.left_number += text
                return self.ui.label_2.setText(self.left_number)
            if text in ("+", "-", "*", "/"):
                self.operator_type = text
                self.ui.label_2.setText("0")
                return self.ui.label.setText(self.left_number + self.operator_type)
            if text in ("="):
                self.ui.label.setText(self.left_number + text)
                return self.ui.label_2.setText(self.left_number)
            if text in ("%"):
                result = "({0} * {1}) / 100".format(self.left_number, "0")
                self.ui.label.setText(result + "=")
                self.left_number = "0"
                return self.ui.label_2.setText(self.left_number)
        if not self.right_number:
            if text.isdigit():
                self.right_number += text
                return self.ui.label_2.setText(self.right_number)
            if text in ("+", "-", "*", "/", "=") and not self.right_number:
                return
        else:
            if text.isdigit():
                self.right_number += text
                return self.ui.label_2.setText(self.right_number)
            if text in ("+", "-", "*", "/", "="):
                self.ui.label.setText(self.left_number + self.operator_type + self.right_number + text)
                self.left_number = str(eval(self.left_number + self.operator_type + self.right_number))
                self.operator_type = ""
                self.right_number = ""
                return self.ui.label_2.setText(self.left_number)
        pass


if __name__ == "__main__":
    calculator = CalculatorMainWindow()
