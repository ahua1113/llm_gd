import os

import output_log
from qsimlogger import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFont, QFontComboBox,
                        QApplication, Qt, QPixmap, QColor)


class ProfileCard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 头像区域
        avatar_label = QLabel(self)
        avatar_label.setFixedSize(100, 100)
        avatar_label.setStyleSheet("background-color: gray;")
        avatar_label.setAlignment(Qt.AlignCenter)

        # 姓名区域
        name_label = QLabel("姓名", self)
        font = QFont()
        font.setPointSize(14)
        name_label.setFont(font)
        name_label.setAlignment(Qt.AlignCenter)

        # 分隔线
        separator = QLabel(self)
        separator.setFixedHeight(1)
        separator.setStyleSheet("background-color: black;")

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(avatar_label, alignment=Qt.AlignCenter)
        layout.addWidget(name_label)
        layout.addWidget(separator)

        self.setLayout(layout)
        self.setFixedSize(200, 220)


if __name__ == '__main__':
    app = QApplication([])
    card = ProfileCard()
    card.show()
    app.exec()

    current_file = os.path.basename(__file__)
    print(current_file)
    output_log.writeLog(current_file)
