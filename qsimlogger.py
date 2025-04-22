from functools import cmp_to_key


class QSimWidget:
    _logs = []

    def __init__(self, parent=None):
        self._parent = parent
        self._properties = {}
        self._layout = None
        self._parent_layout = None  # 所属的父布局
        self._layout_index = 0  # 在父布局中的索引
        self.log_event("WIDGET_CREATED", self.__class__.__name__)

    def setFixedHeight(self, h):
        self._properties['fixed_height'] = h
        self.log_event("SET_FIXED_HEIGHT", h)

    def setLayout(self, layout):
        self._layout = layout
        self.log_event("SET_LAYOUT", layout.__class__.__name__)
        layout._parent = self

    def log_event(self, event_type, *args):
        formatted_args = [str(arg) for arg in args]
        entry = {
            'component': self,
            'event': f"[{event_type}] {', '.join(formatted_args)}",
            'path': self.get_path()
        }
        QSimWidget._logs.append(entry)

    def get_path(self):
        path = []
        current = self
        while True:
            # 获取当前组件的父布局
            if not hasattr(current, '_parent_layout') or current._parent_layout is None:
                break
            parent_layout = current._parent_layout
            layout_type = 'HBox' if isinstance(parent_layout, QSimHBoxLayout) else 'VBox'
            path.insert(0, (layout_type, current._layout_index))

            # 向上遍历到父布局的父组件
            current = parent_layout._parent
            # 继续查找父组件是否属于其他布局
            while current is not None and not hasattr(current, '_parent_layout'):
                current = getattr(current, '_parent', None)
        return path

    def setFixedSize(self, w, h):
        self._properties['size'] = (w, h)
        self.log_event("SET_SIZE", w, h)

    def setWindowTitle(self, title):
        self._properties['title'] = title
        self.log_event("SET_TITLE", title)

    def show(self):
        self.log_event("WINDOW_SHOW")

    def setStyleSheet(self, style):
        self._properties['style'] = style
        self.log_event("STYLESHEET_SET", style)


class QSimLabel(QSimWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)  # 传递给父类
        self._text = text
        self._font = QSimFont()  # 初始化默认字体对象
        self.log_event("LABEL_CREATED", text)

    def setText(self, text):
        self._text = text
        self.log_event("LABEL_TEXT_CHANGED", text)

    def setFont(self, font):
        self.log_event("FONT_SET", font.get_properties())

    def setPixmap(self, pixmap):
        color_info = f"{pixmap.color.r},{pixmap.color.g},{pixmap.color.b}" if pixmap.color else "None"
        self.log_event("PIXMAP_SET", f"Size({pixmap.width}x{pixmap.height})", f"Color({color_info})")

    def setAlignment(self, alignment):
        # 添加对齐值的转换
        alignment_map = {
            Qt.AlignLeft: "Left",
            Qt.AlignRight: "Right",
            Qt.AlignCenter: "Center",
            Qt.AlignHCenter: "HCenter",
            Qt.AlignVCenter: "VCenter"
        }
        self.log_event("ALIGNMENT_SET", alignment_map.get(alignment, str(alignment)))

    # 返回当前字体对象
    def font(self):
        """ 返回当前字体对象 """
        return self._font  # 返回已关联的字体对象


class QSimLineEdit(QSimWidget):
    Normal = 0
    NoEcho = 1
    Password = 2
    Pin = 3

    def __init__(self):
        super().__init__()
        self._echo_mode = self.Normal
        self.log_event("LINEEDIT_CREATED")

    def setPlaceholderText(self, text):
        self.log_event("PLACEHOLDER_SET", text)

    def setEchoMode(self, mode):
        self._echo_mode = mode
        mode_names = {0: "Normal", 1: "NoEcho", 2: "Password", 3: "Pin"}
        self.log_event("ECHO_MODE_SET", mode_names.get(mode, "Unknown"))


class QSimPushButton(QSimWidget):
    def __init__(self, text=""):
        super().__init__()
        self._text = text
        self.log_event("BUTTON_CREATED", text)


class QSimLayout:
    def __init__(self):
        self._parent = None
        self._parent_layout = None  # 新增：记录父布局
        self._layout_index = 0  # 新增：在父布局中的索引
        self._children = []
        self.log_event("LAYOUT_CREATED", self.__class__.__name__)  # 调用自身方法

    def log_event(self, event_type, *args):
        # 布局自己的日志记录方法
        formatted_args = [str(arg) for arg in args]
        entry = {
            'component': self,
            'event': f"[{event_type}] {', '.join(formatted_args)}",
            'path': self.get_layout_path()  # 调用布局专用的路径生成方法
        }
        QSimWidget._logs.append(entry)

    def get_layout_path(self):
        """生成布局的层级路径，格式同组件路径"""
        path = []
        current = self
        while current._parent_layout is not None:
            parent_layout = current._parent_layout
            layout_type = 'HBox' if isinstance(parent_layout, QSimHBoxLayout) else 'VBox'
            path.insert(0, (layout_type, current._layout_index))
            # 向上查找父布局的父组件
            current = parent_layout._parent
            while current is not None and not hasattr(current, '_parent_layout'):
                current = getattr(current, '_parent', None)
        return path

    def addWidget(self, widget, alignment=None):
        widget._parent_layout = self  # 设置子组件的父布局
        widget._layout_index = len(self._children)
        self._children.append(widget)
        self.log_event("ADD_WIDGET", widget.__class__.__name__)

        # 对齐参数处理
        if alignment is not None:
            alignment_map = {
                Qt.AlignLeft: "Left",
                Qt.AlignRight: "Right",
                Qt.AlignCenter: "Center",
                Qt.AlignHCenter: "HCenter",
                Qt.AlignVCenter: "VCenter"
            }
            aligned_str = alignment_map.get(alignment, str(alignment))
            self.log_event("ADD_WIDGET_ALIGNMENT", widget.__class__.__name__, aligned_str)
        else:
            self.log_event("ADD_WIDGET", widget.__class__.__name__)

    def addLayout(self, layout):
        layout._parent_layout = self  # 设置子布局的父布局
        layout._layout_index = len(self._children)
        self._children.append(layout)
        self.log_event("ADD_LAYOUT", layout.__class__.__name__)

    def setAlignment(self, alignment):
        self.log_event("LAYOUT_ALIGNMENT_SET", str(alignment))

    def addSpacing(self, space):
        self.log_event("ADD_SPACING", space)

    def setContentsMargins(self, left, top, right, bottom):
        self.log_event("SET_MARGINS", f"{left},{top},{right},{bottom}")

    def setSpacing(self, space):
        self.log_event("SET_SPACING", space)


class QSimVBoxLayout(QSimLayout): pass


class QSimHBoxLayout(QSimLayout): pass


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


# 字体框类
class QSimFontComboBox(QSimWidget):
    def __init__(self):
        super().__init__()
        self._current_font = QSimFont()
        self.currentFontChanged = QSimSignal()  # 初始化信号对象
        self.log_event("FONTCOMBOBOX_CREATED")

    def setCurrentFont(self, font):
        prev_props = self._current_font.get_properties()
        new_props = font.get_properties()

        if prev_props != new_props:
            self._current_font = font
            self.log_event("FONTCOMBOBOX_SET_FONT", new_props)
            self.currentFontChanged.emit(font)  # 触发信号

    def currentFont(self):
        return self._current_font


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


class QSimApplication:
    def __init__(self, args):
        QSimWidget._logs.clear()

    def log_event(self, event_type, *args):
        entry = {
            'component': None,
            'event': f"[{event_type}] {', '.join(map(str, args))}",
            'path': []
        }
        QSimWidget._logs.append(entry)

    def exec(self):
        self.log_event("APP_EXEC")
        return 0

    def exec_(self):
        self.log_event("APP_EXEC")
        return 0


class Qt:
    AlignLeft = 'AlignLeft'
    AlignRight = 'AlignRight'
    AlignHCenter = 'AlignHCenter'
    AlignTop = 'AlignTop'
    AlignBottom = 'AlignBottom'
    AlignVCenter = 'AlignVCenter'
    AlignCenter = 'AlignCenter'


QWidget = QSimWidget
QLabel = QSimLabel
QLineEdit = QSimLineEdit
QPushButton = QSimPushButton
QVBoxLayout = QSimVBoxLayout
QHBoxLayout = QSimHBoxLayout
QFont = QSimFont
QApplication = QSimApplication
QFontComboBox = QSimFontComboBox
QColor = QSimColor
QPixmap = QSimPixmap


def get_logs():
    def compare_entries(a, b):
        path_a = a.get('path', [])
        path_b = b.get('path', [])

        # 处理无组件事件
        if not path_a and not path_b:
            return 0
        if not path_a:
            return 1
        if not path_b:
            return -1

        # 逐层比较
        min_len = min(len(path_a), len(path_b))
        for i in range(min_len):
            (type_a, idx_a), (type_b, idx_b) = path_a[i], path_b[i]

            # 层级类型不同：HBox优先于VBox
            if type_a != type_b:
                if type_a == 'HBox' and type_b == 'VBox':
                    return -1  # a优先
                elif type_a == 'VBox' and type_b == 'HBox':
                    return 1  # b优先

            # 类型相同，按索引排序
            if type_a == type_b:
                if idx_a != idx_b:
                    if type_a == 'HBox':
                        return -1 if idx_a < idx_b else 1
                    else:  # VBox
                        return -1 if idx_a < idx_b else 1

        # 路径长度不同时，短路径优先
        return len(path_a) - len(path_b)

    # 获取排序后的日志并提取事件
    sorted_entries = sorted(QSimWidget._logs, key=cmp_to_key(compare_entries))
    return [entry['event'] for entry in sorted_entries]
