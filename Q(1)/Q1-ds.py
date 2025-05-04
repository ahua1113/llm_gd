import os

from output_log import writeLog
from qsim.widgets import (QSimLayout, QSimApplication, QSimListWidget, QSimSignal, QSimColor, QSimPixmap, QSimLabel,
                          QSimHBoxLayout, QSimVBoxLayout, QSimWidget, QSimFontComboBox, QSimRadioButton, QSimPushButton,
                          QSimTabWidget, QSimCheckBox, QSimGroupBox, QSimListWidgetItem, QSimComboBox, QSimTableWidget,
                          QSimTableWidgetItem, QSimSpinBox, QSimSlider, QSimFrame, QSimProgressBar, QSimStatusBar,
                          QSimHeaderView, QSimLineEdit, Qt, QSimFont, QSimGridLayout)


class LoginForm(QSimWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(300, 250)

        # 创建组件
        title = QSimLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        font = QSimFont()
        font.setBold(True)
        font.setPointSize(16)
        title.setFont(font)

        username = QSimLineEdit()
        username.setPlaceholderText("Enter username")

        password = QSimLineEdit()
        password.setPlaceholderText("Enter password")
        password.setEchoMode(QSimLineEdit.Password)

        cancel_btn = QSimPushButton("Cancel")
        submit_btn = QSimPushButton("Submit")

        # 按钮水平布局
        btn_layout = QSimHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(submit_btn)

        # 主垂直布局
        main_layout = QSimVBoxLayout()
        main_layout.addStretch()
        main_layout.addWidget(title)
        main_layout.addWidget(username)
        main_layout.addWidget(password)
        main_layout.addLayout(btn_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QSimApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    writeLog(current_file)
