import os

import output_log
from qsim.widgets import (QWidget, QPushButton, QHBoxLayout, QLabel, QApplication, Qt, QVBoxLayout)

class ToolbarDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建按钮
        buttons = []
        for _ in range(5):
            button = QPushButton("[Icon]")
            buttons.append(button)

        # 布局按钮
        button_layout = QHBoxLayout()
        for button in buttons:
            button_layout.addWidget(button)

        # 底部分隔线
        separator = QLabel()
        separator.setStyleSheet("border-bottom: 1px solid gray;")
        separator.setFixedHeight(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addWidget(separator)
        self.setLayout(main_layout)

        # 设置窗口尺寸
        self.setFixedSize(600, 80)
        self.setWindowTitle('Toolbar Demo')

if __name__ == '__main__':
    app = QApplication([])
    demo = ToolbarDemo()
    demo.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)
