from qsim.layouts import QSimLayout


class QSimFont:
    def __init__(self, family=None, size=None, style=None, bold=False, italic=False):
        self.family = family
        self.size = size
        self.bold = bold
        self.italic = italic

        if family is None:
            self._properties = {
                'family': 'Arial',
                'point_size': 12,
                'bold': False,
                'italic': False,
                'underline': False
            }
        else:
            self._properties = {
                'family': family,
                'point_size': size
            }

    def setItalic(self, enable):
        self._properties['italic'] = enable
        self.log_event("ITALIC", enable)

    def setBold(self, enable):
        self._properties['bold'] = enable
        self.log_event("BOLD", enable)

    def setPointSize(self, size):
        self._properties['point_size'] = size
        self.log_event("SIZE", size)

    def setFamily(self, family):
        self._properties['family'] = family
        self.log_event("FAMILY", family)

    def setUnderline(self, enable):
        self._properties['underline'] = enable
        self.log_event("UNDERLINE", enable)

    def log_event(self, prop_type, value):
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
    def __init__(self, sender=None, *types):  # 新增sender参数
        self._sender = sender  # 记录信号所属的组件
        self._types = types
        self._handlers = []

    def connect(self, handler):
        """连接槽函数时记录日志"""
        self._handlers.append(handler)
        # 记录日志
        self.log_event("SIGNAL_CONNECT", f"Connected to {handler.__name__}")

    def emit(self, *args):
        """触发信号时记录日志"""
        # 生成日志条目
        self.log_event("SIGNAL_EMIT", f"Emit with args: {args}")
        # 调用槽函数
        for handler in self._handlers:
            handler(*args)

    def log_event(self, event_type, details):
        """统一记录信号事件到日志"""
        entry = {
            'component': self._sender,
            'event': f"[{event_type}] {details}",
            'path': self._sender.get_path() if hasattr(self._sender, 'get_path') else []
        }
        QSimLayout._logs.append(entry)


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
