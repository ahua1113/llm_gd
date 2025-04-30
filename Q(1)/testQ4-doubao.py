import os
import sys

import output_log
from qsim.widgets import (QWidget, QVBoxLayout, QApplication, QGroupBox, QCheckBox, QComboBox)


class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建主垂直布局
        main_layout = QVBoxLayout()

        # 创建 Preferences 分组框
        preferences_group = QGroupBox("Preferences")
        preferences_layout = QVBoxLayout()

        # 创建 Dark Mode 复选框
        dark_mode_checkbox = QCheckBox("Dark Mode")
        preferences_layout.addWidget(dark_mode_checkbox)

        # 创建 Auto Update 复选框
        auto_update_checkbox = QCheckBox("Auto Update")
        preferences_layout.addWidget(auto_update_checkbox)

        preferences_group.setLayout(preferences_layout)
        main_layout.addWidget(preferences_group)

        # 创建 Language 下拉框
        language_combo = QComboBox()
        language_combo.addItems(["English", "中文"])
        main_layout.addWidget(language_combo)

        # 设置主布局
        self.setLayout(main_layout)

        # 设置窗口宽度固定为 400
        self.setFixedWidth(400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = SettingsPanel()
    panel.show()
    app.exec_()
    
    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)
