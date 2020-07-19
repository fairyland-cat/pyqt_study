import sys
from PyQt5.QtGui import QPalette
from PyQt5.QtWidgets import QColorDialog, QFontDialog
from Ui_pull_down import Ui_MainWindow  # 调用ui模块中的Ui_MainWindow()类
from PyQt5 import QtWidgets
import re


class Menu():
    def __init__(self):
        super(Menu, self).__init__()
        app = QtWidgets.QApplication(sys.argv)
        self.mian_window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.mian_window)
        self.mian_window.show()

        # 字体事件
        self.ui.action_name.triggered.connect(self.set_font)
        # 颜色事件
        self.ui.actioncolor.triggered.connect(self.set_color)
        # 推出
        self.ui.actionexit.triggered.connect(quit)
        # 粗体
        self.ui.action_1.triggered.connect(self.bold)
        # 斜体
        self.ui.action_2.triggered.connect(self.italic)
        # 下划线
        self.ui.action_3.triggered.connect(self.underline)
        sys.exit(app.exec_())

    def underline(self):
        is_bold = re.search("<u>", self.ui.label.text())
        if not is_bold:
            self.ui.label.setText("<u>{0}</u>".format(self.ui.label.text()))
        else:
            self.ui.label.setText(self.ui.label.text().replace("u", "p"))
        self.ui.label.adjustSize()

    def italic(self):
        is_bold = re.search("<i>", self.ui.label.text())
        if not is_bold:
            self.ui.label.setText("<i>{0}</i>".format(self.ui.label.text()))
        else:
            self.ui.label.setText(self.ui.label.text().replace("i", "p"))
        self.ui.label.adjustSize()

    def bold(self):
        is_bold = re.search("<b>", self.ui.label.text())
        if not is_bold:
            self.ui.label.setText("<b>{0}</b>".format(self.ui.label.text()))
        else:
            self.ui.label.setText(self.ui.label.text().replace("b", "p"))
        self.ui.label.adjustSize()

    def set_font(self):
        self.font, ok = QFontDialog.getFont()
        if ok:
            self.ui.label.setFont(self.font)
            self.ui.label.adjustSize()
        pass

    def set_color(self):
        color = QColorDialog.getColor()
        p = QPalette()
        p.setColor(QPalette.WindowText, color)
        self.ui.label.setPalette(p)
        pass


if __name__ == "__main__":
    Menu()
