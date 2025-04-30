from qsim.widgets import (QWidget, QHBoxLayout, QApplication, Qt)
from qsim.otherWidgets import (QSplitter, QTextEdit)


class SplitViewDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建文本编辑框
        left_text_edit = QTextEdit("Left Panel")
        right_text_edit = QTextEdit("Right Panel")

        # 创建分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_text_edit)
        splitter.addWidget(right_text_edit)

        # 主布局
        main_layout = QHBoxLayout()
        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        # 设置窗口尺寸
        self.setFixedSize(600, 400)
        self.setWindowTitle('Split View Demo')


if __name__ == '__main__':
    app = QApplication([])
    demo = SplitViewDemo()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)