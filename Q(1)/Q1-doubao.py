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
        self.initUI()

    def initUI(self):
        # 创建垂直布局
        main_layout = QSimVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # 顶部标题
        title_label = QSimLabel("Login")
        main_layout.addWidget(title_label)

        # 用户名输入框
        username_input = QSimLineEdit()
        username_input.setPlaceholderText("Enter username")
        main_layout.addWidget(username_input)

        # 密码输入框
        password_input = QSimLineEdit()
        password_input.setPlaceholderText("Enter password")
        password_input.setEchoMode(QSimLineEdit.Password)
        main_layout.addWidget(password_input)

        # 水平排列的按钮
        button_layout = QSimHBoxLayout()
        cancel_button = QSimPushButton("Cancel")
        submit_button = QSimPushButton("Submit")
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(submit_button)
        main_layout.addLayout(button_layout)

        # 设置布局
        self.setLayout(main_layout)

        # 设置窗口大小
        self.setFixedSize(300, 250)


if __name__ == '__main__':
    app = QSimApplication([])
    login_form = LoginForm()
    login_form.show()
    app.exec()

    current_file = os.path.basename(__file__)
    writeLog(current_file)

