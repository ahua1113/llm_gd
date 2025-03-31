from mock_pyqt5 import (QApplication, QWidget, QVBoxLayout,
                        QPushButton, QPainter, QColor, Qt)


class CanvasWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.default_color = QColor(Qt.black)
        self.current_color = self.default_color

    def set_blue(self):
        self.current_color = QColor(Qt.blue)
        self.update()

    def reset_color(self):
        self.current_color = self.default_color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(self.current_color)
        widget_size = min(self.width(), self.height()) * 0.8
        x = (self.width() - widget_size) / 2
        y = (self.height() - widget_size) / 2
        painter.drawEllipse(x, y, widget_size, widget_size)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.canvas = CanvasWidget()

        btn_blue = QPushButton('Blue')
        btn_blue.clicked.connect(self.canvas.set_blue)
        btn_blue.click()

        btn_reset = QPushButton('Reset')
        btn_reset.clicked.connect(self.canvas.reset_color)
        btn_blue.click()

        layout.addWidget(btn_blue)
        layout.addWidget(btn_reset)
        layout.addWidget(self.canvas)

        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()

    app.exec_()
