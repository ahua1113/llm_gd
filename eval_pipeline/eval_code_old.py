import contextlib
import io

import evalplus
from evalplus.evaluate import evaluate

from eval_pipeline.call_api import get_problem, doubao_code, tongyi_code, deepseek_code
from eval_pipeline.rule_pattern import validate_log
import contextlib
import io
from qsim.widgets import (QSimLayout, QSimApplication, QSimListWidget, QSimSignal, QSimColor, QSimPixmap, QSimLabel,
                          QSimHBoxLayout, QSimVBoxLayout, QSimWidget, QSimFontComboBox, QSimRadioButton, QSimPushButton,
                          QSimTabWidget, QSimCheckBox, QSimGroupBox, QSimListWidgetItem, QSimComboBox, QSimTableWidget,
                          QSimTableWidgetItem, QSimSpinBox, QSimSlider, QSimFrame, QSimProgressBar, QSimStatusBar,
                          QSimHeaderView, QSimLineEdit, Qt, QSimFont, QSimGridLayout)


class LogCaptureSystem:
    def __init__(self):
        self._logs = []
        self._original_logs = None

    def _override_imports(self):
        """劫持组件类的日志记录方法"""
        # 备份原始日志列表
        self._original_logs = QSimLayout._logs
        # 劫持日志存储地址
        QSimLayout._logs = self._logs

    def _restore_imports(self):
        """恢复原始组件引用"""
        QSimLayout._logs = self._original_logs

    @contextlib.contextmanager
    def capture_logs(self, code: str):
        """执行代码并捕获日志的上下文管理器"""
        self._logs.clear()
        self._override_imports()
        try:
            with io.StringIO() as buf:
                with contextlib.redirect_stdout(buf):
                    try:
                        exec(code, globals())
                    except Exception as e:
                        print(f"执行代码时出现异常: {e}")

                if 'app' in globals() and hasattr(globals()['app'], 'exec_'):
                    globals()['app'].exec_()

            yield self._logs
        finally:
            self._restore_imports()


# Q1-deepseek模型代码
code = """
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

"""

# Q1-doubao模型代码
code_doubao = """
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
        # 顶部标题
        title_label = QSimLabel("Login")

        # 用户名输入框
        username_input = QSimLineEdit()
        username_input.setPlaceholderText("Enter username")

        # 密码输入框
        password_input = QSimLineEdit()
        password_input.setPlaceholderText("Enter password")
        password_input.setEchoMode(QSimLineEdit.Password)

        # 水平排列的按钮
        cancel_button = QSimPushButton("Cancel")
        submit_button = QSimPushButton("Submit")
        button_layout = QSimHBoxLayout()
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(submit_button)

        # 垂直布局
        main_layout = QSimVBoxLayout()
        main_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        main_layout.addWidget(username_input)
        main_layout.addWidget(password_input)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)
        self.setFixedSize(300, 250)


if __name__ == '__main__':
    app = QSimApplication([])
    login_form = LoginForm()
    login_form.show()
    app.exec_()

"""

if __name__ == '__main__':
    # 调用大模型 api 生成代码后，捕获日志

    # 取问题
    problems = get_problem()
    problem = problems[1]

    # 调用doubao api 生成代码，生成5份代码
    q1_code_res_db = doubao_code(problem, 5)

    # 调用deepseek api 生成代码
    # q1_code_res_db = deepseek_code(problem, 5)

    # 调用通义 api 生成代码
    # q1_code_res_db = tongyi_code(problem, 5)

    # 输出代码结果
    for i in range(len(q1_code_res_db)):
        print(q1_code_res_db[i])

    # 捕获日志
    log_capture = LogCaptureSystem()

    # 存储日志结果
    log_doubao = []

    # 每一份代码都要捕获日志
    for i in range(len(q1_code_res_db)):
        with log_capture.capture_logs(q1_code_res_db[i]) as logs:
            print(f"Captured logs for code {i + 1}: {logs}")
            log_doubao.append(logs)

    # 输出日志结果
    for i in range(len(log_doubao)):
        print(f"日志{i + 1}: {log_doubao[i]}")

    # 评估正确性
    res_code = []
    for i in range(len(log_doubao)):
        # 对每一份代码进行正确性评估，传入字符串
        res_code.append(validate_log(str(log_doubao[i])))

    # 输出评估结果
    for i in range(len(res_code)):
        print(f"代码{i + 1}: {res_code[i]}")

    

