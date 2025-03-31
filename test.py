# 引入模拟的 PyQt5 库
from simulated_pyqt5 import SimulatedQWidget, SimulatedQPushButton, SimulatedQVBoxLayout, SimulatedQApplication


class CircleWidget(SimulatedQWidget):
    def __init__(self):
        super().__init__()
        print("圆形区域已初始化，初始颜色为黑色")
        self.color = "黑色"

    def paintEvent(self):
        print(f"正在绘制圆形，当前颜色为 {self.color}")

    def set_blue(self):
        self.color = "蓝色"
        print("变色按钮被执行，圆形已变为蓝色")
        self.paintEvent()

    def restore_color(self):
        self.color = "黑色"
        print("复原按钮被执行，圆形已恢复为黑色")
        self.paintEvent()


class MainWindow(SimulatedQWidget):
    def __init__(self):
        super().__init__()
        print("主窗口已初始化")
        self.circle_widget = CircleWidget()
        blue_button = SimulatedQPushButton("变蓝")
        restore_button = SimulatedQPushButton("复原")

        blue_button.clicked.connect(self.circle_widget.set_blue)
        restore_button.clicked.connect(self.circle_widget.restore_color)

        layout = SimulatedQVBoxLayout()
        layout.addWidget(self.circle_widget)
        layout.addWidget(blue_button)
        layout.addWidget(restore_button)


if __name__ == "__main__":
    print("程序开始运行")
    app = SimulatedQApplication([])
    window = MainWindow()
    result = app.exec_()
    print("程序运行结束")
