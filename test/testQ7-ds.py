import os

import output_log
from qsim.widgets import QWidget, QLabel, QProgressBar, QVBoxLayout, QApplication, QFont, Qt
import sys


class ProgressIndicator(QWidget):
    """进度指示器组件"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 窗口设置
        self.setWindowTitle("Progress Indicator")
        self.setFixedHeight(150)  # 固定高度

        # 创建组件
        self.lbl_title = QLabel("Processing...")
        self.progress_bar = QProgressBar()
        self.lbl_step = QLabel("Step 2/4")

        # 样式配置
        self._setup_styles()

        # 布局管理
        layout = QVBoxLayout()
        layout.addStretch(1)  # 顶部留空
        layout.addWidget(self.lbl_title, 0, Qt.AlignCenter)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.lbl_step, 0, Qt.AlignCenter)
        layout.addStretch(1)  # 底部留空
        self.setLayout(layout)

    def _setup_styles(self):
        # 设置标题样式（蓝色文本）
        self.lbl_title.setStyleSheet("color: blue;")
        title_font = QFont()
        title_font.setPointSize(12)
        self.lbl_title.setFont(title_font)

        # 进度条设置
        self.progress_bar.setValue(50)  # 50%进度
        self.progress_bar.setFixedWidth(300)  # 固定宽度

        # 步骤文本样式
        self.lbl_step.setStyleSheet("color: #666;")
        step_font = QFont()
        step_font.setItalic(True)
        self.lbl_step.setFont(step_font)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgressIndicator()
    window.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)