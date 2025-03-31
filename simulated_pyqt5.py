# 模拟 PyQt5 库的封装
class SimulatedQWidget:
    def __init__(self):
        print("部件已初始化")


class SimulatedQPushButton(SimulatedQWidget):
    def __init__(self, text):
        super().__init__()
        print(f"{text} 按钮已创建")
        self.text = text
        self.clicked = SimulatedSignal()

    def click(self):
        print(f"{self.text} 按钮被点击")
        self.clicked.emit()


class SimulatedQVBoxLayout:
    def __init__(self):
        print("垂直布局已初始化")

    def addWidget(self, widget):
        print(f"部件 {widget.__class__.__name__} 已添加到垂直布局")


class SimulatedSignal:
    def __init__(self):
        self.slots = []

    def connect(self, slot):
        self.slots.append(slot)

    def emit(self):
        for slot in self.slots:
            slot()


class SimulatedQApplication:
    def __init__(self, args):
        print("应用程序已初始化")

    def exec_(self):
        print("应用程序开始执行")
        return 0
