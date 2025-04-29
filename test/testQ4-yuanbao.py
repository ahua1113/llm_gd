import os

import output_log
from qsim.widgets import (QWidget, QVBoxLayout, QApplication, QGroupBox, QCheckBox, QComboBox)


class SettingsPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 主垂直布局
        main_layout = QVBoxLayout(self)

        # Preferences分组框
        prefs_group = QGroupBox("Preferences")
        prefs_layout = QVBoxLayout()

        # 添加复选框
        self.dark_mode_check = QCheckBox("Dark Mode")
        self.auto_update_check = QCheckBox("Auto Update")
        prefs_layout.addWidget(self.dark_mode_check)
        prefs_layout.addWidget(self.auto_update_check)
        prefs_group.setLayout(prefs_layout)

        # Language下拉框
        self.language_combo = QComboBox()
        self.language_combo.addItems(["English", "中文"])

        # 将所有控件添加到主布局
        main_layout.addWidget(prefs_group)
        main_layout.addWidget(self.language_combo)

        # 设置窗口固定宽度
        self.setFixedWidth(400)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    settings_panel = SettingsPanel()
    settings_panel.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)