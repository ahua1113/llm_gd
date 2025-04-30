from qsim.widgets import (QWidget, QVBoxLayout, QApplication)
from qsim.otherWidgets import (QCalendarWidget, QDateEdit)


class CalendarDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建日历控件
        calendar = QCalendarWidget()

        # 创建日期选择控件
        date_edit = QDateEdit()

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(calendar)
        layout.addWidget(date_edit)
        layout.setSpacing(10)

        self.setLayout(layout)
        self.setFixedSize(400, 350)
        self.setWindowTitle('Calendar Demo')


if __name__ == '__main__':
    app = QApplication([])
    demo = CalendarDemo()
    demo.show()
    app.exec_()

    import os
    from output_log import writeLog

    current_file = os.path.basename(__file__)
    writeLog(current_file)
