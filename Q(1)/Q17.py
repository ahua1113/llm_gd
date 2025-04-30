from qsim.widgets import (QWidget, QLabel, QVBoxLayout, QApplication, Qt)
from qsim.otherWidgets import QScrollArea


class ScrollAreaDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # 创建内容部件
        content_widget = QWidget()
        content_layout = QVBoxLayout()

        # 添加带序号的标签
        for i in range(1, 21):
            label = QLabel(f"Label {i}")
            label.setFixedHeight(40)
            content_layout.addWidget(label)

        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

        # 设置窗口尺寸
        self.setFixedSize(300, 250)
        self.setWindowTitle('Scroll Area Demo')


if __name__ == '__main__':
    app = QApplication([])
    demo = ScrollAreaDemo()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)
