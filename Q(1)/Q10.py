import os

import output_log
from qsim.widgets import (QWidget, QLabel, QHBoxLayout, QVBoxLayout, QApplication, Qt)

class NotificationBox(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置浅黄色背景和圆角
        self.setStyleSheet("background-color: #FFFFCC; border-radius: 10px;")

        # 警告图标
        icon_label = QLabel("[!]")
        icon_label.setStyleSheet("font-size: 24px;")

        # 消息文本
        message_label = QLabel("System maintenance\nScheduled at 3:00 AM")

        # 布局
        layout = QHBoxLayout()
        layout.addWidget(icon_label, alignment=Qt.AlignTop)
        layout.addWidget(message_label, alignment=Qt.AlignTop)

        self.setLayout(layout)
        self.setFixedSize(350, 100)
        self.setWindowTitle('Notification Box')


if __name__ == '__main__':
    app = QApplication([])
    demo = NotificationBox()
    demo.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)