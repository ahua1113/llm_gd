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
        password_input.setPlaceholderText("Enter password")
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
    import os

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取根目录
    root_dir = os.path.dirname(current_dir)
    # 构建日志文本结果目录路径
    log_dir = os.path.join(root_dir, '日志文本结果')
    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    current_file = os.path.basename(__file__)
    try:
        # 构建完整的文件路径
        file_path = os.path.join(log_dir, current_file + '.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            for log in get_logs():
                file.write(log + '\n')
        print(f"日志已成功写入 {file_path} 文件。")
    except Exception as e:
        print(f"写入日志到文件时出现错误: {e}")
