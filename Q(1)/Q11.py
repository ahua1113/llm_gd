from qsim.widgets import (QWidget, QGroupBox, QLabel, QLineEdit, QGridLayout, QVBoxLayout, QApplication, QCheckBox)


class FilterPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建分组框
        group_box = QGroupBox("Filter Options")

        # 日期范围选择
        date_from_label = QLabel("From:")
        date_from_input = QLineEdit()
        date_to_label = QLabel("To:")
        date_to_input = QLineEdit()

        # 分类多选框
        category_label = QLabel("Category:")
        checkbox_a = QCheckBox("A")
        checkbox_b = QCheckBox("B")
        checkbox_c = QCheckBox("C")

        # 网格布局
        grid_layout = QGridLayout()
        grid_layout.addWidget(date_from_label, 0, 0)
        grid_layout.addWidget(date_from_input, 0, 1)
        grid_layout.addWidget(date_to_label, 0, 2)
        grid_layout.addWidget(date_to_input, 0, 3)
        grid_layout.addWidget(category_label, 1, 0)
        grid_layout.addWidget(checkbox_a, 1, 1)
        grid_layout.addWidget(checkbox_b, 1, 2)
        grid_layout.addWidget(checkbox_c, 1, 3)

        group_box.setLayout(grid_layout)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(group_box)
        self.setLayout(main_layout)

        # 设置最小宽度
        self.setMinimumWidth(500)
        self.setWindowTitle('Filter Panel')


if __name__ == '__main__':
    app = QApplication([])
    demo = FilterPanel()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)