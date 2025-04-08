from mock_pyqt5 import (QApplication, QWidget, QVBoxLayout,
                        QPushButton, QPainter, QColor, Qt)


class CircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.circle_color = Qt.black
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        blue_button = QPushButton('变蓝')
        blue_button.clicked.connect(self.set_blue)
        layout.addWidget(blue_button)

        restore_button = QPushButton('复原')
        restore_button.clicked.connect(self.restore_color)
        layout.addWidget(restore_button)

        blue_button.click()
        restore_button.click()

        self.setLayout(layout)

    def set_blue(self):
        self.circle_color = QColor(Qt.blue)
        self.update()

    def restore_color(self):
        self.circle_color = Qt.black
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(self.circle_color)
        painter.drawEllipse(50, 50, 100, 100)


if __name__ == '__main__':
    app = QApplication([])
    window = CircleWidget()
    window.show()

    app.exec_()
