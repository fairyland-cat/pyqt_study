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
        # 清除所有痕迹
        if text == "C":
            self.ui.label.setText("")
            self.ui.label_2.setText("")
            self.left_number = ""
            self.operator_type = ""
            self.right_number = ""
            return
        # 清除当前输入的数
        if text == "CE":
            self.ui.label_2.setText("0")
            if self.operator_type:
                self.right_number = ""
            else:
                self.left_number = ""
            return
        # 回退删除一位数
        if text == "Backspace":
            if self.operator_type:
                input_list = list(self.right_number)
                if input_list:
                    input_list.pop()
                    self.right_number = "".join(input_list)
            else:
                input_list = list(self.left_number)
                if input_list:
                    input_list.pop()
                    self.left_number = "".join(input_list)
            surplus = "".join(input_list) if input_list else "0"
            self.ui.label_2.setText(surplus)
            return
        # 计算逻辑
        if not self.left_number:
            if text.isdigit() and text != "0":
                self.ui.label.setText("")
                self.left_number += text
                return self.ui.label_2.setText(self.left_number)
            else:
                return
        if not self.operator_type:
            if text.isdigit() or text == ".":
                self.left_number += text
                return self.ui.label_2.setText(self.left_number)
            if text in ("+", "-", "*", "/"):
                self.operator_type = text
                self.ui.label_2.setText("0")
                if self.left_number[-1] == ".":
                    self.left_number = self.left_number[:-1]
                return self.ui.label.setText(self.left_number + self.operator_type)
            # 本次运算得出最终结果并结束
            if text in ("=", "1/x", "sqr", "%"):
                if text == "1/x":
                    self.left_number = "1/" + self.left_number
                if text == "sqr":
                    self.left_number = self.left_number + " ** 0.5"
                if text in ("%"):
                    self.left_number = "({0} * 0) / 100".format(self.left_number)
                self.ui.label.setText(self.left_number + "=")
                result = eval(self.left_number)
                # 本次运算结束
                self.left_number = ""
                return self.ui.label_2.setText(str(result))
            if text == "+/-":
                result = "-" if self.left_number[0] != "-" else ""
                self.left_number = result + self.left_number
                self.ui.label_2.setText(self.left_number)
        if not self.right_number:
            if text.isdigit():
                self.right_number += text
                return self.ui.label_2.setText(self.right_number)
            if text in ("+", "-", "*", "/", "=", "%") and not self.right_number:
                return
        else:
            if text.isdigit() or text == ".":
                self.right_number += text
                return self.ui.label_2.setText(self.right_number)
            if text == "+/-":
                result = "-" if self.left_number[0] != "-" else ""
                self.right_number = result + self.right_number
                return self.ui.label_2.setText(self.right_number)
            if text in ("+", "-", "*", "/"):
                self.left_number = str(eval(self.left_number + self.operator_type + self.right_number))
                self.operator_type = text
                self.ui.label.setText(self.left_number + self.operator_type)
                self.right_number = ""
                return self.ui.label_2.setText("0")
            # 本次运算得出最终结果并结束
            if text in ("=", "1/x", "%"):
                if self.right_number[-1] == ".":
                    self.right_number = self.right_number[:-1]
                if text == "1/x":
                    self.right_number = "1/" + self.right_number
                if text == "sqr":
                    self.right_number = self.left_number + " ** 0.5"
                if text in ("%"):
                    self.right_number = "({0} * {1}) / 100".format(self.left_number, self.right_number)
                self.ui.label.setText(self.left_number + self.operator_type + self.right_number + "=")
                result = str(eval(self.left_number + self.operator_type + self.right_number))
                self.ui.label_2.setText(result)
                self.left_number = ""
                self.right_number = ""
                self.operator_type = ""
                return
        pass


if __name__ == "__main__":
    CalculatorMainWindow()
