import os

import output_log
from qsim.widgets import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFont, QFontComboBox,
                          QApplication, Qt, QPixmap, QColor, QGroupBox, QCheckBox,
                          QComboBox, QStatusBar, QTableWidgetItem, QTableWidget, QHeaderView)


class DataTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建表格
        self.table = QTableWidget()
        # 设置列数为 3
        self.table.setColumnCount(3)
        # 设置表头
        self.table.setHorizontalHeaderLabels(['Name', 'Age', 'Department'])

        # 设置表头字体加粗
        font = QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)

        # 预填充两行示例数据
        data = [
            ['Alice', '25', 'HR'],
            ['Bob', '30', 'IT']
        ]
        self.table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, item in enumerate(row_data):
                table_item = QTableWidgetItem(item)
                self.table.setItem(row, col, table_item)

        # 表格宽度占满窗口
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 创建布局并添加表格
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

        # 设置窗口尺寸
        self.setGeometry(100, 100, 500, 200)


if __name__ == '__main__':
    app = QApplication([])
    table_widget = DataTable()
    table_widget.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)