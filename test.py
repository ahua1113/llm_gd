import sys
# 替换为模拟的 PyQt5 库导入
from mock_pyqt5 import (QApplication, QWidget, QVBoxLayout,
                        QPushButton, QPainter, QColor, Qt)


class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.color = QColor(Qt.default)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.color)
        size = min(self.width(), self.height())
        painter.drawEllipse(self.width() // 2 - size // 4,
                            self.height() // 2 - size // 4,
                            size // 2, size // 2)

    def set_blue(self):
        self.color = QColor(Qt.blue)
        self.update()

    def restore_color(self):
        self.color = QColor(Qt.default)
        self.update()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.circle_widget = CircleWidget()
        self.blue_button = QPushButton('Make Blue')
        self.blue_button.clicked.connect(self.circle_widget.set_blue)
        self.restore_button = QPushButton('Restore Color')
        self.restore_button.clicked.connect(self.circle_widget.restore_color)
        self.blue_button.click()
        self.restore_button.click()
        layout = QVBoxLayout()
        layout.addWidget(self.circle_widget)
        layout.addWidget(self.blue_button)
        layout.addWidget(self.restore_button)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    result = app.exec_()
