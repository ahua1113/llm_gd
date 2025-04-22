import os

import output_log
from qsimlogger import (QWidget, QLabel, QVBoxLayout, Qt, QPixmap, QColor, QFont, QApplication)


class ProfileCard(QWidget):
    """创建用户信息卡片"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口固定尺寸
        self.setFixedSize(200, 220)

        # 创建垂直布局
        layout = QVBoxLayout()

        # 头像区域
        avatar = QLabel(self)
        avatar.setFixedSize(100, 100)

        # 创建灰色矩形
        pixmap = QPixmap(100, 100)
        pixmap.fill(QColor(200, 200, 200))
        avatar.setPixmap(pixmap)
        avatar.setAlignment(Qt.AlignCenter)
        layout.addWidget(avatar, alignment=Qt.AlignCenter)

        # 姓名区域
        name_label = QLabel("姓名", self)
        name_label.setAlignment(Qt.AlignCenter)

        # 设置字体
        font = name_label.font()
        font.setPointSize(14)
        name_label.setFont(font)
        layout.addWidget(name_label)

        # 分隔线
        separator = QLabel(self)
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: black;")
        layout.addWidget(separator)

        self.setLayout(layout)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    card = ProfileCard()
    card.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    print(current_file)
    output_log.writeLog(current_file)
