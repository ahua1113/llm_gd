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


class QSimLabel(QSimWidget):
    def __init__(self, text=""):
        super().__init__()
        self._text = text
        self.log_event("LABEL_CREATED", text)

    def setText(self, text):
        self._text = text
        self.log_event("LABEL_TEXT_CHANGED", text)

    def setFont(self, font):
        self.log_event("FONT_SET", font.get_properties())

    def setAlignment(self, alignment):
        self.log_event("ALIGNMENT_SET", str(alignment))


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
        self._layout_index = 0      # 新增：在父布局中的索引
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

    def addWidget(self, widget):
        widget._parent_layout = self  # 设置子组件的父布局
        widget._layout_index = len(self._children)
        self._children.append(widget)
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
    def __init__(self):
        self._props = {}

    def setBold(self, bold):
        self._props['bold'] = bold

    def setPointSize(self, size):
        self._props['size'] = size

    def get_properties(self):
        return f"Font(bold={self._props.get('bold', False)}, size={self._props.get('size', 12)})"


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


Qt = type('Qt', (), {'AlignCenter': 'AlignCenter'})
QWidget = QSimWidget
QLabel = QSimLabel
QLineEdit = QSimLineEdit
QPushButton = QSimPushButton
QVBoxLayout = QSimVBoxLayout
QHBoxLayout = QSimHBoxLayout
QFont = QSimFont
QApplication = QSimApplication


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