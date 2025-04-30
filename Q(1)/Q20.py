from qsim.widgets import (QWidget, QLabel, QLineEdit, QComboBox, QGridLayout, QApplication)
from qsim.otherWidgets import QTextEdit


class ComplexFormDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建标签
        name_label = QLabel("Name:")
        country_label = QLabel("Country:")
        notes_label = QLabel("Notes:")

        # 创建输入控件
        name_input = QLineEdit()
        country_combo = QComboBox()
        country_combo.addItems(["USA", "China", "UK"])
        notes_input = QTextEdit()

        # 网格布局
        layout = QGridLayout()
        layout.addWidget(name_label, 0, 0)
        layout.addWidget(name_input, 0, 1)
        layout.addWidget(country_label, 1, 0)
        layout.addWidget(country_combo, 1, 1)
        layout.addWidget(notes_label, 2, 0)
        layout.addWidget(notes_input, 2, 1)

        self.setLayout(layout)
        self.setFixedSize(450, 300)
        self.setWindowTitle('Complex Form Demo')


if __name__ == '__main__':
    app = QApplication([])
    demo = ComplexFormDemo()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)
