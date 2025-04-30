from qsim.widgets import (QWidget, QGroupBox, QRadioButton, QVBoxLayout, QApplication)


class RadioGroupDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建分组框
        group_box = QGroupBox("Gender")

        # 创建单选按钮
        male_radio = QRadioButton("Male")
        female_radio = QRadioButton("Female")
        other_radio = QRadioButton("Other")

        # 默认选中 Male
        male_radio.setChecked(True)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(male_radio)
        layout.addWidget(female_radio)
        layout.addWidget(other_radio)
        group_box.setLayout(layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

        # 设置窗口宽度
        self.setFixedWidth(200)
        self.setWindowTitle('Radio Group Demo')


if __name__ == '__main__':
    app = QApplication([])
    demo = RadioGroupDemo()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)