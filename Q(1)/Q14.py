from qsim.widgets import (QWidget, QLabel, QSlider, QFrame, QHBoxLayout, QVBoxLayout, QApplication, Qt)


class ColorPickerDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建滑动条
        red_slider = QSlider(Qt.Horizontal)
        red_slider.setRange(0, 255)
        green_slider = QSlider(Qt.Horizontal)
        green_slider.setRange(0, 255)
        blue_slider = QSlider(Qt.Horizontal)
        blue_slider.setRange(0, 255)

        # 创建标签
        red_label = QLabel("R:")
        green_label = QLabel("G:")
        blue_label = QLabel("B:")

        # 创建颜色预览方块
        color_preview = QFrame()
        color_preview.setStyleSheet("background-color: rgb(0, 0, 0);")

        # 连接信号和槽
        red_slider.valueChanged.connect(lambda: self.update_color(red_slider, green_slider, blue_slider, color_preview))
        green_slider.valueChanged.connect(
            lambda: self.update_color(red_slider, green_slider, blue_slider, color_preview))
        blue_slider.valueChanged.connect(
            lambda: self.update_color(red_slider, green_slider, blue_slider, color_preview))

        # 布局
        red_layout = QHBoxLayout()
        red_layout.addWidget(red_label)
        red_layout.addWidget(red_slider)
        green_layout = QHBoxLayout()
        green_layout.addWidget(green_label)
        green_layout.addWidget(green_slider)
        blue_layout = QHBoxLayout()
        blue_layout.addWidget(blue_label)
        blue_layout.addWidget(blue_slider)

        main_layout = QVBoxLayout()
        main_layout.addLayout(red_layout)
        main_layout.addLayout(green_layout)
        main_layout.addLayout(blue_layout)
        main_layout.addWidget(color_preview)

        self.setLayout(main_layout)
        self.setFixedSize(400, 200)
        self.setWindowTitle('Color Picker Demo')

    def update_color(self, red_slider, green_slider, blue_slider, color_preview):
        r = red_slider.value()
        g = green_slider.value()
        b = blue_slider.value()
        color_preview.setStyleSheet(f"background-color: rgb({r}, {g}, {b});")


if __name__ == '__main__':
    app = QApplication([])
    demo = ColorPickerDemo()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)