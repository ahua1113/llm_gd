from qsim.widgets import (QWidget, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QApplication)


class ListSelectorDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建列表控件
        available_list = QListWidget()
        selected_list = QListWidget()

        # 添加示例项目
        for i in range(1, 6):
            available_list.addItem(f"Item {i}")

        # 创建按钮
        add_button = QPushButton("Add>>")
        remove_button = QPushButton("<<Remove")

        # 连接信号和槽
        add_button.clicked.connect(lambda: self.move_item(available_list, selected_list))
        remove_button.clicked.connect(lambda: self.move_item(selected_list, available_list))

        # 按钮布局
        button_layout = QVBoxLayout()
        button_layout.addWidget(add_button)
        button_layout.addWidget(remove_button)

        # 主布局
        main_layout = QHBoxLayout()
        main_layout.addWidget(available_list)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(selected_list)

        self.setLayout(main_layout)
        self.setFixedSize(500, 300)
        self.setWindowTitle('List Selector Demo')

    def move_item(self, source_list, target_list):
        selected_items = source_list.selectedItems()
        for item in selected_items:
            row = source_list.row(item)
            item = source_list.takeItem(row)
            target_list.addItem(item)


if __name__ == '__main__':
    app = QApplication([])
    demo = ListSelectorDemo()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)
