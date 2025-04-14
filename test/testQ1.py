from qsimlogger import (QWidget, QLabel, QLineEdit, QPushButton,
                        QVBoxLayout, QHBoxLayout, QFont, QApplication, Qt)


class LoginForm(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主垂直布局
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # 标题标签
        title_label = QLabel("Login")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(18)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        # 输入框组件
        username_input = QLineEdit()
        username_input.setPlaceholderText("Enter username")
        password_input = QLineEdit()
        password_input.setPlaceholderText("Enter password")
        password_input.setEchoMode(QLineEdit.Password)

        # 按钮布局
        button_layout = QHBoxLayout()
        cancel_btn = QPushButton("Cancel")
        submit_btn = QPushButton("Submit")
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(submit_btn)

        # 组合所有组件
        main_layout.addWidget(title_label)
        main_layout.addSpacing(20)
        main_layout.addWidget(username_input)
        main_layout.addWidget(password_input)
        main_layout.addSpacing(15)
        main_layout.addLayout(button_layout)

        # 窗口设置
        self.setLayout(main_layout)
        self.setFixedSize(300, 250)
        self.setWindowTitle("Login Form")


# 测试代码
if __name__ == "__main__":
    app = QApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

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