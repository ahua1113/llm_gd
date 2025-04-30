import os

import output_log
from qsim.widgets import QWidget, QLabel, QProgressBar, QVBoxLayout, QApplication, QFont, Qt
import sys


class ProgressIndicator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建顶部标签
        processing_label = QLabel("Processing...")
        processing_label.setStyleSheet("color: blue;")
        font = QFont()
        font.setBold(True)
        processing_label.setFont(font)

        # 创建进度条
        progress_bar = QProgressBar(self)
        progress_bar.setValue(50)

        # 创建进度条下方的说明文本
        step_label = QLabel("Step 2/4")

        # 创建垂直布局
        layout = QVBoxLayout()
        layout.addWidget(processing_label, alignment=Qt.AlignCenter)
        layout.addWidget(progress_bar, alignment=Qt.AlignCenter)
        layout.addWidget(step_label, alignment=Qt.AlignCenter)

        # 设置布局
        self.setLayout(layout)

        # 设置窗口高度
        self.setFixedHeight(150)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    indicator = ProgressIndicator()
    indicator.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)