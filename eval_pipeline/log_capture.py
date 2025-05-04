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
        self._original_imports = {}

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
            # 创建临时命名空间
            """
            namespace = {
                # 包含所有需要的组件类...
                'QSimApplication': QSimApplication,
                'QSimWidget': QSimWidget,
                'QSimLabel': QSimLabel,
                'QSimPushButton': QSimPushButton,
                'QSimRadioButton': QSimRadioButton,
                'QSimTabWidget': QSimTabWidget,
                'QSimCheckBox': QSimCheckBox,
                'QSimGroupBox': QSimGroupBox,
                'QSimTableWidget': QSimTableWidget,
                'QSimHeaderView': QSimHeaderView,
                'QSimTableWidgetItem': QSimTableWidgetItem,
                'QSimHBoxLayout': QSimHBoxLayout,
                'QSimVBoxLayout': QSimVBoxLayout,
                'QSimFontComboBox': QSimFontComboBox,
                'QSimSignal': QSimSignal,
                'QSimProgressBar': QSimProgressBar,
                'QSimListWidget': QSimListWidget,
                'QSimPixmap': QSimPixmap,
                'QSimColor': QSimColor,
                'QSimListWidgetItem': QSimListWidgetItem,
                'QSimComboBox': QSimComboBox,
                'QSimSpinBox': QSimSpinBox,
                'QSimSlider': QSimSlider,
                'QSimFrame': QSimFrame,
                'QSimStatusBar': QSimStatusBar,
                'QSimLineEdit': QSimLineEdit,
                'QSimFont': QSimFont,
                'QSimGridLayout': QSimGridLayout,
                'Qt': Qt
            }
            """

            # 重定向标准输出
            with io.StringIO() as buf:
                with contextlib.redirect_stdout(buf):
                    exec(code)

                # 执行应用程序事件循环
                # if 'app' in namespace:
                #    namespace['app'].exec_()

            yield self._logs
        finally:
            self._restore_imports()


# Q1-doubao.py代码
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

if __name__ == '__main__':
    log_capture = LogCaptureSystem()

    with log_capture.capture_logs(code) as captured_logs:
        # 在此上下文内执行代码
        pass

    for captured_log in captured_logs:
        print(captured_log)
