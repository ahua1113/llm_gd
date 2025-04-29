from qsim.layouts import QSimLayout


class QSimFont:
    def __init__(self):
        self._properties = {
            'family': 'Arial',
            'point_size': 12,
            'bold': False,
            'italic': False,
            'underline': False
        }

    def setItalic(self, enable):
        self._properties['italic'] = enable
        self._log_change("ITALIC", enable)

    def setBold(self, enable):
        self._properties['bold'] = enable
        self._log_change("BOLD", enable)

    def setPointSize(self, size):
        self._properties['point_size'] = size
        self._log_change("SIZE", size)

    def setFamily(self, family):
        self._properties['family'] = family
        self._log_change("FAMILY", family)

    def setUnderline(self, enable):
        self._properties['underline'] = enable
        self._log_change("UNDERLINE", enable)

    def _log_change(self, prop_type, value):
        """统一记录字体属性变化"""
        entry = {
            'component': self,
            'event': f"[FONT_{prop_type}_SET] {value}",
            'path': []
        }
        QSimLayout._logs.append(entry)

    def get_properties(self):
        """获取字体特征字典（用于日志记录）"""
        return self._properties.copy()


# 添加信号基类
class QSimSignal:
    def __init__(self, *types):
        """构造信号时定义参数类型（如 QSimSignal(int) 表示传递整数）"""
        self._types = types  # 存储期望的参数类型
        self._handlers = []  # 信号连接的槽函数列表

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
