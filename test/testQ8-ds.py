import os
import sys
from qsim.widgets import (QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                          QGroupBox, QTabWidget, QApplication, Qt)

import output_log


class TabDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口固定尺寸
        self.setFixedSize(400, 300)

        # 创建主选项卡容器
        tabs = QTabWidget()

        # 创建General页
        general_tab = QWidget()
        group_box = QGroupBox("Settings")
        general_layout = QVBoxLayout(general_tab)
        general_layout.addWidget(group_box)

        # 创建Advanced页
        advanced_tab = QWidget()
        warning_icon = QLabel("⚠️")
        warning_icon.setStyleSheet("color: red; font-size: 32px;")
        warning_text = QLabel("Advanced options require careful configuration.")

        # Advanced页布局
        adv_layout = QHBoxLayout(advanced_tab)
        adv_layout.addStretch()
        adv_layout.addWidget(warning_icon)
        adv_layout.addSpacing(10)
        adv_layout.addWidget(warning_text)
        adv_layout.addStretch()

        # 添加选项卡
        tabs.addTab(general_tab, "General")
        tabs.addTab(advanced_tab, "Advanced")

        # 主布局
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(tabs)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TabDemo()
    window.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)
