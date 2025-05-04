import contextlib
import io

from evalplus import evaluate
from evalplus.eval.utils import time_limit

from eval_pipeline.call_api import deepseek_code
from eval_pipeline.logValidator import LogValidator
from eval_pipeline.rule_pattern import Q1_PATTERN
from log_capture import LogCaptureSystem


def evaluate_code(code: str) -> dict:
    # 初始化验证系统
    log_capture = LogCaptureSystem()

    # 根据问题ID加载规则
    # rules = {
    #    "Q1": Q1_PATTERN,
    #    # 其他问题的规则...
    # }[problem_id]

    try:
        with log_capture.capture_logs(code) as captured_logs:
            pass  # 代码已通过exec执行

        for captured_log in captured_logs:
            print("日志:", captured_log)

        # 执行验证
        # validator = LogValidator(
        #    actual_logs=logs,
        #    expected_pattern=rules
        # )
        # score = validator.validate()

        # return {
        #    "pass": score == 1.0,
        #    "score": score,
        #    "logs": logs
        # }

        return {
            "logs": captured_logs
        }

    except TimeoutError:
        return {"error": "Timeout"}
    except Exception as e:
        return {"error": str(e)}


def get_problem():
    file_path = r'f:\桌面\llm_gd\data\QUI-old.txt'
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 分割问题
            problems = []
            lines = content.split('\n')
            problem_start = False
            current_problem = ""
            for line in lines:
                if line.startswith('Q') and '/' in line:
                    if current_problem:
                        problems.append(current_problem.strip())
                    current_problem = line + '\n'
                    problem_start = True
                elif problem_start:
                    current_problem += line + '\n'
            if current_problem:
                problems.append(current_problem.strip())
            return problems
    except FileNotFoundError:
        print(f"未找到文件: {file_path}")
        return []


codeQ1 = """
from qsim.widgets import (QSimLayout, QSimApplication, QSimListWidget, QSimSignal, QSimColor, QSimPixmap, QSimLabel,
                          QSimHBoxLayout, QSimVBoxLayout, QSimWidget, QSimFontComboBox, QSimRadioButton, QSimPushButton,
                          QSimTabWidget, QSimCheckBox, QSimGroupBox, QSimListWidgetItem, QSimComboBox, QSimTableWidget,
                          QSimTableWidgetItem, QSimSpinBox, QSimSlider, QSimFrame, QSimProgressBar, QSimStatusBar,
                          QSimHeaderView, QSimLineEdit, Qt, QSimFont, QSimGridLayout)


class LoginForm(QSimWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(300, 250)
        
        main_layout = QSimVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        
        title = QSimLabel("Login")
        title.setAlignment(Qt.AlignCenter)
        
        self.username_input = QSimLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        
        self.password_input = QSimLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QSimLineEdit.Password)
        
        button_layout = QSimHBoxLayout()
        cancel_button = QSimPushButton("Cancel")
        submit_button = QSimPushButton("Submit")
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(submit_button)
        
        main_layout.addWidget(title)
        main_layout.addWidget(self.username_input)
        main_layout.addWidget(self.password_input)
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QSimApplication([])
    window = LoginForm()
    window.show()
    app.exec_()
"""

if __name__ == '__main__':
    # evaluation_results = evaluate.evaluate()

    # Q1模拟
    problems = get_problem()
    problem = problems[1]

    # 调用deepseek api 生成代码
    q1_code_res_ds = deepseek_code(problem)

    log_capture = LogCaptureSystem()

    with log_capture.capture_logs(str(q1_code_res_ds)) as captured_logs:
        # 在此上下文内执行代码
        pass

    for captured_log in captured_logs:
        print(captured_log)
