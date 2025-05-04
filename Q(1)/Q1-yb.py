import os

from output_log import writeLog
from qsim.widgets import (QSimWidget, QSimLabel, QSimLineEdit,
                          QSimPushButton, QSimHBoxLayout, QSimVBoxLayout,
                          QSimApplication, Qt)


class LoginForm(QSimWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口固定尺寸
        self.setFixedSize(300, 250)

        # 创建界面元素
        title = QSimLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        username = QSimLineEdit()
        username.setPlaceholderText("Enter username")

        password = QSimLineEdit()
        password.setPlaceholderText("Enter password")
        password.setEchoMode(QSimLineEdit.Password)

        # 创建按钮并设置水平布局
        cancel_btn = QSimPushButton("Cancel")
        submit_btn = QSimPushButton("Submit")

        btn_layout = QSimHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(submit_btn)
        btn_layout.addStretch(1)

        # 创建主垂直布局
        main_layout = QSimVBoxLayout()
        main_layout.addStretch(1)
        main_layout.addWidget(title)
        main_layout.addSpacing(20)
        main_layout.addWidget(username)
        main_layout.addWidget(password)
        main_layout.addSpacing(20)
        main_layout.addLayout(btn_layout)
        main_layout.addStretch(1)

        # 设置布局边距
        main_layout.setContentsMargins(30, 0, 30, 0)
        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QSimApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    writeLog(current_file)