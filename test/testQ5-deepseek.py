import os
import sys

import output_log
from qsimlogger import (QWidget, QLabel, QVBoxLayout, QApplication, Qt, QStatusBar)


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口固定尺寸
        self.setFixedSize(250, 300)

        # 创建顶部标签
        top_label = QLabel("Placeholder Image")
        top_label.setStyleSheet("color: gray; font-style: italic;")
        top_label.setAlignment(Qt.AlignCenter)

        # 创建中央显示区域
        center_label = QLabel()
        center_label.setFixedSize(200, 200)
        center_label.setStyleSheet("background-color: gray;")

        # 创建底部状态栏
        status_bar = QStatusBar()
        status_bar.showMessage("Ready")

        # 设置主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(top_label)
        main_layout.addStretch(1)
        main_layout.addWidget(center_label, alignment=Qt.AlignCenter)
        main_layout.addStretch(1)
        main_layout.addWidget(status_bar)

        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)