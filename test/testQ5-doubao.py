import os
import sys

import output_log
from qsim.widgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFont, QFontComboBox,
                          QApplication, Qt, QPixmap, QColor, QGroupBox, QCheckBox, QComboBox, QStatusBar)


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建垂直布局
        layout = QVBoxLayout()

        # 创建顶部标签
        top_label = QLabel("Placeholder Image")
        top_label.setStyleSheet("font-style: italic; color: gray;")
        layout.addWidget(top_label)

        # 创建中央显示区域
        self.image_area = QLabel()
        self.image_area.setFixedSize(200, 200)
        self.image_area.setStyleSheet("background-color: gray;")
        layout.addWidget(self.image_area, alignment=Qt.AlignmentFlag.AlignCenter)

        # 创建底部状态栏
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Ready")
        layout.addWidget(self.status_bar)

        # 设置布局
        self.setLayout(layout)

        # 锁定窗口尺寸
        self.setFixedSize(250, 300)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)
