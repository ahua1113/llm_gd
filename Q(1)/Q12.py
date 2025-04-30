from qsim.widgets import (QWidget, QLabel, QSpinBox, QSlider, QHBoxLayout, QVBoxLayout, QApplication, Qt)


class NumberInputDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 标签
        label = QLabel("Value:")

        # 数字输入框
        spin_box = QSpinBox()
        spin_box.setRange(0, 100)

        # 滑动条
        slider = QSlider(Qt.Horizontal)
        slider.setRange(0, 100)

        # 连接信号和槽
        spin_box.valueChanged.connect(slider.setValue)
        slider.valueChanged.connect(spin_box.setValue)

        # 布局
        input_layout = QHBoxLayout()
        input_layout.addWidget(label)
        input_layout.addWidget(spin_box)
        input_layout.addWidget(slider)

        self.setLayout(input_layout)
        self.setFixedSize(300, 100)
        self.setWindowTitle('Number Input Demo')


if __name__ == '__main__':
    app = QApplication([])
    demo = NumberInputDemo()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)