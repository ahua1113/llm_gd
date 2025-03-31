# 模拟 PyQt5 库的核心组件
class QObject:
    def __init__(self):
        pass


class QWidget(QObject):
    def __init__(self):
        print("部件已初始化")
        super().__init__()

    def show(self):
        print("部件已显示")

    def width(self):
        # 模拟返回一个固定的宽度值，实际应用中可根据需要调整
        return 200

    def height(self):
        # 模拟返回一个固定的高度值，实际应用中可根据需要调整
        return 200

    def update(self):
        # 模拟 update 方法，调用 paintEvent
        if hasattr(self, 'paintEvent'):
            self.paintEvent(None)

    def setLayout(self, layout):
        # 模拟 setLayout 方法，这里不做实际操作
        pass


class QPushButton(QWidget):
    def __init__(self, text):
        super().__init__()
        print(f"{text} 按钮已创建")
        self.text = text
        self.clicked = Signal()

    def click(self):
        print(f"{self.text} 按钮被点击")
        self.clicked.emit()


class QVBoxLayout:
    def __init__(self):
        print("垂直布局已初始化")

    def addWidget(self, widget):
        print(f"部件 {widget.__class__.__name__} 已添加到垂直布局")


class Signal:
    def __init__(self):
        self.slots = []

    def connect(self, slot):
        self.slots.append(slot)

    def emit(self):
        for slot in self.slots:
            slot()


class QApplication:
    def __init__(self, args):
        print("应用程序已初始化")

    def exec_(self):
        print("应用程序开始执行")
        return 0


# 模拟 QtGui 模块中的部分类
class QPainter:
    Antialiasing = 1  # 添加 Antialiasing 属性

    def __init__(self, widget):
        print("开始绘制部件")
        self.widget = widget

    def setRenderHint(self, hint):
        pass

    def setBrush(self, brush):
        pass

    def drawEllipse(self, x, y, width, height):
        print(f"在部件上绘制椭圆，位置: ({x}, {y})，大小: ({width}, {height})")


class QColor:
    def __init__(self, color):
        self.color = color

# 模拟 QtCore 模块中的 Qt 类
class Qt:
    default = "黑色"
    black = "黑色"
    blue = "蓝色"
