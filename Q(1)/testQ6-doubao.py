import os
import sys

import output_log
from qsim.widgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFont, QFontComboBox,
                          QApplication, Qt, QPixmap, QColor, QGroupBox, QCheckBox,
                          QComboBox, QStatusBar, QTableWidgetItem, QTableWidget)


class DataTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建表格
        table = QTableWidget()
        # 设置表格列数
        table.setColumnCount(3)
        # 设置表头
        table.setHorizontalHeaderLabels(['Name', 'Age', 'Department'])
        # 预填充两行示例数据
        data = [
            ['Alice', '25', 'HR'],
            ['Bob', '30', 'IT']
        ]
        table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(value)
                table.setItem(row, col, item)

        # 表头字体加粗
        font = table.horizontalHeader().font()
        font.setBold(True)
        table.horizontalHeader().setFont(font)

        # 表格宽度占满窗口
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setSectionResizeMode(Qt.HeaderResize.Stretch)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)

        # 窗口尺寸设置为500x200
        self.setGeometry(100, 100, 500, 200)
        self.setWindowTitle('Data Table')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dt = DataTable()
    dt.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)
