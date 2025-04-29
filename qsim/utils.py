class QSimFont:
    def __init__(self, font_family='', font_size=12):
        """模拟Qt的字体对象构造函数
        :param font_family: 字体名称（如'Arial'）
        :param font_size: 字号（整数）
        """
        self._props = {
            'family': font_family,
            'size': font_size,
            'bold': False,
            'italic': False
        }

    def setFamily(self, name):
        self._props['family'] = name

    def pointSize(self):
        return self._props['size']

    def setBold(self, bold):
        self._props['bold'] = bold

    def setPointSize(self, size):
        self._props['size'] = size

    def get_properties(self):
        return f"Font(bold={self._props.get('bold', False)}, size={self._props.get('size', 12)})"


# 添加信号基类
class QSimSignal:
    def __init__(self):
        self._handlers = []

    def connect(self, handler):
        self._handlers.append(handler)

    def emit(self, *args):
        for handler in self._handlers:
            handler(*args)


# QSimColor 颜色模拟类
class QSimColor:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __repr__(self):
        return f"Color({self.r},{self.g},{self.b})"


# QSimPixmap 图像模拟类
class QSimPixmap:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.color = None

    def fill(self, color):
        self.color = color
