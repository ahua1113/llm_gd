import os

import output_log
from qsim.widgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFont, QFontComboBox,
                          QApplication, Qt, QPixmap, QColor, QGroupBox, QCheckBox, QTabWidget,
                          QComboBox, QStatusBar, QTableWidgetItem, QTableWidget)


class TabDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建选项卡控件
        tab_widget = QTabWidget()

        # 创建 General 页
        general_tab = QWidget()
        general_layout = QVBoxLayout()
        settings_group_box = QGroupBox("Settings")
        general_layout.addWidget(settings_group_box)
        general_tab.setLayout(general_layout)

        # 创建 Advanced 页
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout()
        warning_icon = QLabel()
        # 假设这里有一个红色警告图标资源，这里只是占位
        # pixmap = QPixmap("warning_icon.png")
        # warning_icon.setPixmap(pixmap)
        warning_text = QLabel("这是红色警告提示文本")
        warning_text.setStyleSheet("color: red;")
        advanced_layout.addWidget(warning_icon)
        advanced_layout.addWidget(warning_text)
        advanced_tab.setLayout(advanced_layout)

        # 将选项卡页添加到选项卡控件中
        tab_widget.addTab(general_tab, "General")
        tab_widget.addTab(advanced_tab, "Advanced")

        # 设置主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(tab_widget)
        self.setLayout(main_layout)

        # 设置窗口大小
        self.setFixedSize(400, 300)


if __name__ == '__main__':
    app = QApplication([])
    tab_demo = TabDemo()
    tab_demo.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)
