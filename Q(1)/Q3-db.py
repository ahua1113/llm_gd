import os

from qsim.widgets import (QSimApplication, QSimLabel,
                          QSimVBoxLayout, QSimWidget, QSimFrame, Qt, QSimFont)
from write_new_log import writeLogNew


class ProfileCard(QSimWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 头像区域
        avatar_label = QSimLabel(self)
        avatar_label.setStyleSheet("background-color: gray;")
        avatar_label.setFixedSize(100, 100)

        # 姓名
        name = "示例姓名"
        name_label = QSimLabel(name, self)
        font = QSimFont()
        font.setPointSize(14)
        name_label.setFont(font)
        name_label.setAlignment(Qt.AlignCenter)

        # 分隔线
        separator = QSimFrame(self)
        separator.setFrameShape(QSimFrame.HLine)
        separator.setFrameShadow(QSimFrame.Sunken)
        separator.setStyleSheet("color: black;")

        # 布局
        vbox = QSimVBoxLayout()
        vbox.addWidget(avatar_label, alignment=Qt.AlignCenter)
        vbox.addWidget(name_label)
        vbox.addWidget(separator)

        self.setLayout(vbox)
        self.setFixedSize(200, 220)


if __name__ == '__main__':
    app = QSimApplication([])
    prof = ProfileCard()
    prof.show()
    app.exec()

    current_file = os.path.basename(__file__)
    writeLogNew(current_file)