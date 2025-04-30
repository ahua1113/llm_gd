from qsim.widgets import (QWidget, QVBoxLayout, QApplication, Qt)
from qsim.otherWidgets import (QLCDNumber, QDial)


class DigitalDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建 LCD 数字显示
        lcd = QLCDNumber()
        lcd.display(12345)

        # 创建旋钮控件
        dial = QDial()
        dial.setRange(0, 100)

        # 连接信号和槽
        dial.valueChanged.connect(lcd.display)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(lcd, alignment=Qt.AlignCenter)
        layout.addWidget(dial, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # 设置窗口尺寸
        self.setFixedSize(200, 250)
        self.setWindowTitle('Digital Dashboard')


if __name__ == '__main__':
    app = QApplication([])
    demo = DigitalDashboard()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)
