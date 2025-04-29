import os

import output_log
from qsim.widgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QApplication, QFont
)
import sys


class DataTable(QWidget):
    """固定数据表格组件"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 窗口设置
        self.setWindowTitle("Data Table Demo")
        self.setFixedSize(500, 200)

        # 创建表格
        self.table = QTableWidget()
        self.table.setColumnCount(3)  # 3列
        self.table.setRowCount(2)  # 2行

        # 设置表头
        headers = ["Name", "Age", "Department"]
        self.table.setHorizontalHeaderLabels(headers)

        # 表头字体加粗
        font = QFont()
        font.setBold(True)
        self.table.horizontalHeader().setFont(font)

        # 填充示例数据
        data = [['Alice', '25', 'HR'], ['Bob', '30', 'IT']]

        for row, items in enumerate(data):
            for col, text in enumerate(items):
                item = QTableWidgetItem(text)
                self.table.setItem(row, col, item)

        # 设置表格扩展策略
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

        # 布局管理
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.table)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataTable()
    window.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    output_log.writeLog(current_file)