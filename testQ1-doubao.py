from qsimlogger import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFont, QApplication, Qt)


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 顶部标题
        title_label = QLabel("Login")
        font = QFont()
        font.setBold(True)
        font.setPointSize(18)
        title_label.setFont(font)
        title_label.setAlignment(Qt.AlignCenter)

        # 用户名输入框
        username_input = QLineEdit()
        username_input.setPlaceholderText("Enter username")

        # 密码输入框
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)

        # 取消和提交按钮
        cancel_button = QPushButton("Cancel")
        submit_button = QPushButton("Submit")
        button_layout = QHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(submit_button)

        # 垂直布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_label)
        main_layout.addWidget(username_input)
        main_layout.addWidget(password_input)
        main_layout.addLayout(button_layout)

        # 设置布局
        self.setLayout(main_layout)

        # 窗口设置
        self.setFixedSize(300, 250)
        self.setWindowTitle('Login Form')
        self.show()


if __name__ == '__main__':
    app = QApplication([])
    form = LoginForm()
    app.exec()

    # 打印捕获的日志（实际评估时输出到文件）
    from qsimlogger import get_logs

    for log in get_logs():
        print(log)
