class QSimWidget:
    _logs = []

    def __init__(self, parent=None):
        self._parent = parent
        self._properties = {}
        self._layout = None
        self.log_event("WIDGET_CREATED", self.__class__.__name__)

    def setLayout(self, layout):
        self._layout = layout
        self.log_event("SET_LAYOUT", layout.__class__.__name__)
        # 模拟Qt的父子关系
        layout._parent = self

    def log_event(self, event_type, *args):
        formatted_args = [str(arg) for arg in args]
        QSimWidget._logs.append(f"[{event_type}] {', '.join(formatted_args)}")

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
    # 添加回显模式常量
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
        # 将数字代码转换为可读名称
        mode_names = {
            0: "Normal",
            1: "NoEcho",
            2: "Password",
            3: "Pin"
        }
        self.log_event("ECHO_MODE_SET", mode_names.get(mode, "Unknown"))


class QSimPushButton(QSimWidget):
    def __init__(self, text=""):
        super().__init__()
        self._text = text
        self.log_event("BUTTON_CREATED", text)


class QSimLayout:
    def __init__(self):
        self._parent = None
        self.log_event("LAYOUT_CREATED", self.__class__.__name__)

    def log_event(self, event_type, *args):
        QSimWidget.log_event(None, event_type, *args)

    def addWidget(self, widget):
        self.log_event("ADD_WIDGET", widget.__class__.__name__)

    def addLayout(self, layout):
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
        QSimWidget.log_event(None, event_type, *args)

    # 两种可能的执行方式
    def exec(self):
        self.log_event("APP_EXEC")
        return 0

    def exec_(self):
        self.log_event("APP_EXEC")
        return 0


# PyQt5 兼容接口
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
    return QSimWidget._logs
