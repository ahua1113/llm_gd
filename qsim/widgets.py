from functools import cmp_to_key

from qsim.utils import (QSimFont, QSimSignal, QSimColor, QSimPixmap)
from qsim.layouts import (QSimHBoxLayout, QSimVBoxLayout, QSimLayout)
from qsim.enums import Qt


class QSimWidget:
    # _logs = []

    def __init__(self, parent=None):
        self._geometry = (0, 0, 100, 100)  # (x, y, width, height)

        self._parent = parent
        self._properties = {}
        self._layout = None
        self._parent_layout = None  # 所属的父布局
        self._layout_index = 0  # 在父布局中的索引
        self.log_event("WIDGET_CREATED", self.__class__.__name__)

    def setGeometry(self, x: int, y: int, w: int, h: int):
        """模拟Qt的setGeometry方法"""
        self._geometry = (x, y, w, h)
        self.log_event("SET_GEOMETRY", x, y, w, h)

    def geometry(self):
        """获取当前几何参数"""
        return self._geometry

    def setFixedHeight(self, h):
        self._properties['fixed_height'] = h
        self.log_event("SET_FIXED_HEIGHT", h)

    def setFixedWidth(self, w):
        self._properties['fixed_width'] = w
        self.log_event("SET_FIXED_WIDTH", w)

    def setMinimumWidth(self, w):
        self._properties['min_width'] = w
        self.log_event("SET_MIN_WIDTH", w)

    def setMaximumWidth(self, w):
        self._properties['max_width'] = w
        self.log_event("SET_MAX_WIDTH", w)

    def setFixedSize(self, w, h):
        self._properties['size'] = (w, h)
        self.log_event("SET_SIZE", w, h)

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
        QSimLayout._logs.append(entry)

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

    def setWindowTitle(self, title):
        self._properties['title'] = title
        self.log_event("SET_TITLE", title)

    def show(self):
        self.log_event("WINDOW_SHOW")

    def setStyleSheet(self, style):
        self._properties['style'] = style
        self.log_event("STYLESHEET_SET", style)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''标签'''


class QSimLabel(QSimWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)  # 传递给父类
        self._text = text
        self._font = QSimFont()  # 初始化默认字体对象，在 setFont 没有被显式调用时保证 _font不会为空
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


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''单行文本框'''


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


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''按钮'''


class QSimPushButton(QSimWidget):
    def __init__(self, text=""):
        super().__init__()
        self._text = text
        self.log_event("BUTTON_CREATED", text)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''字体组合框'''


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


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''分组框'''


class QSimGroupBox(QSimWidget):
    def __init__(self, title="", parent=None):
        super().__init__(parent=parent)
        self._title = title
        self._layout = None
        self.log_event("GROUPBOX_CREATED", title)

    def setTitle(self, title):
        self._title = title
        self.log_event("GROUPBOX_TITLE_SET", title)

    def setLayout(self, layout):
        """继承自QSimWidget的方法，无需重写"""
        super().setLayout(layout)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''复选框'''


class QSimCheckBox(QSimWidget):
    # 状态常量
    Unchecked = 0
    PartiallyChecked = 1
    Checked = 2

    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self._text = text
        self._state = self.Unchecked
        self.stateChanged = QSimSignal()  # 状态变化信号
        self.log_event("CHECKBOX_CREATED", text)

    def setText(self, text):
        self._text = text
        self.log_event("CHECKBOX_TEXT_CHANGED", text)

    def isChecked(self):
        return self._state == self.Checked

    def setCheckState(self, state):
        state_map = {
            self.Unchecked: "Unchecked",
            self.PartiallyChecked: "PartiallyChecked",
            self.Checked: "Checked"
        }
        if self._state != state:
            self._state = state
            self.log_event("CHECKBOX_STATE_CHANGED", state_map[state])
            self.stateChanged.emit(state)

    def setChecked(self, checked):
        state = self.Checked if checked else self.Unchecked
        self.setCheckState(state)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''组合框'''


class QSimComboBox(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._items = []
        self._current_index = -1
        self.currentIndexChanged = QSimSignal()  # 索引变化信号
        self.log_event("COMBOBOX_CREATED")

    def addItem(self, text):
        self._items.append(text)
        self.log_event("COMBOBOX_ITEM_ADDED", text)
        if self._current_index == -1:
            self.setCurrentIndex(0)

    def addItems(self, items):
        """ 批量添加多个选项 """
        for text in items:
            self.addItem(text)  # 复用单个添加的逻辑
        self.log_event("COMBOBOX_ITEMS_ADDED", len(items))

    def currentIndex(self):
        return self._current_index

    def currentText(self):
        return self._items[self._current_index] if self._current_index >= 0 else ""

    def setCurrentIndex(self, index):
        if index != self._current_index and 0 <= index < len(self._items):
            self._current_index = index
            self.log_event("COMBOBOX_INDEX_CHANGED", index, self._items[index])
            self.currentIndexChanged.emit(index)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''状态栏'''


class QSimStatusBar(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._temporary_message = ""
        self._permanent_widgets = []
        self._normal_widgets = []
        self.log_event("STATUSBAR_CREATED")
        self.messageChanged = QSimSignal()  # 消息变化信号

    def showMessage(self, message, timeout=0):
        self._temporary_message = message
        self.log_event("STATUSBAR_SHOW_MESSAGE", message, f"{timeout}ms")
        self.messageChanged.emit(message)

    def clearMessage(self):
        self._temporary_message = ""
        self.log_event("STATUSBAR_CLEAR_MESSAGE")
        self.messageChanged.emit("")

    def addPermanentWidget(self, widget, stretch=0):
        self._permanent_widgets.append(widget)
        self.log_event("STATUSBAR_ADD_PERMANENT", widget.__class__.__name__, f"stretch={stretch}")
        widget._parent = self

    def addWidget(self, widget, stretch=0):
        self._normal_widgets.append(widget)
        self.log_event("STATUSBAR_ADD_WIDGET", widget.__class__.__name__, f"stretch={stretch}")
        widget._parent = self

    def removeWidget(self, widget):
        if widget in self._normal_widgets:
            self._normal_widgets.remove(widget)
            self.log_event("STATUSBAR_REMOVE_WIDGET", widget.__class__.__name__)
        elif widget in self._permanent_widgets:
            self._permanent_widgets.remove(widget)
            self.log_event("STATUSBAR_REMOVE_PERMANENT", widget.__class__.__name__)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''表格组件类'''


class QTableWidgetItem:
    """表格单元格项"""

    def __init__(self, text=""):
        self.text = text
        self._alignment = None

    def setText(self, text):
        self.text = text

    def setAlignment(self, alignment):
        align_map = {
            Qt.AlignLeft: "左对齐",
            Qt.AlignRight: "右对齐",
            Qt.AlignCenter: "居中"
        }
        self._alignment = align_map.get(alignment, "未知对齐")


class QHeaderView(QSimWidget):
    """模拟表头组件"""
    Interactive = 0
    Fixed = 1
    Stretch = 2
    ResizeToContents = 3
    Custom = 4

    class ResizeMode:
        Interactive = 0
        Fixed = 1
        Stretch = 2
        ResizeToContents = 3
        Custom = 4

    def __init__(self, orientation="horizontal"):
        super().__init__()
        self.orientation = orientation
        self._font = QSimFont()  # 字体初始化，默认字体

        self.ResizeMode = self.ResizeMode()  # 使枚举可通过实例访问
        self._stretch_last = False  # 新增属性
        self._resize_mode = "Interactive"  # 新增属性

        self.log_event("HEADER_CREATED", orientation)

    def setFont(self, font):
        self._font = font
        self.log_event("HEADER_FONT_SET", self.orientation)

    def font(self):
        return self._font  # 永远返回有效字体对象

    def setStretchLastSection(self, enable):
        self._stretch_last = enable
        self.log_event("HEADER_STRETCH_LAST", str(enable))

    def setSectionResizeMode(self, mode):
        mode_map = {
            self.ResizeMode.Interactive: "Interactive",
            self.ResizeMode.Fixed: "Fixed",
            self.ResizeMode.Stretch: "Stretch",  # 新增枚举映射
            self.ResizeMode.ResizeToContents: "ResizeToContents",
            self.ResizeMode.Custom: "Custom"
        }
        self._resize_mode = mode_map.get(mode, "Unknown")
        self.log_event("HEADER_RESIZE_MODE", self._resize_mode)


class QTableWidget(QSimWidget):
    # 新增调整策略常量
    AdjustToContents = "AdjustToContents"
    AdjustToContentsOnFirstShow = "AdjustToContentsOnFirstShow"

    def __init__(self, rows=0, cols=0):
        super().__init__()
        self._size_adjust_policy = None  # 策略调整相关属性

        # 自动创建带默认字体的表头
        self.horizontal_header = QHeaderView("horizontal")
        self.vertical_header = QHeaderView("vertical")

        self._rows = rows
        self._cols = cols
        self._items = {}
        self.log_event("TABLE_CREATED", f"{rows}x{cols}")

    def setRowCount(self, rows):
        self._rows = rows
        self.log_event("TABLE_ROW_RESIZED", rows)

    def setColumnCount(self, cols):
        self._cols = cols
        self.log_event("TABLE_COL_RESIZED", cols)

    def setItem(self, row, col, item):
        """核心方法：设置单元格内容"""
        if not isinstance(item, QTableWidgetItem):
            raise TypeError("必须使用QTableWidgetItem类型")

        self._items[(row, col)] = item
        self.log_event("TABLE_ITEM_SET", row, col, item.text)

    def cellWidget(self, row, col):
        """获取单元格中的组件"""
        return self._items.get((row, col), None)

    def setHorizontalHeaderLabels(self, labels):
        """设置水平表头"""
        for col_idx, text in enumerate(labels):
            item = QTableWidgetItem(text)
            self.setItem(-1, col_idx, item)  # 用-1表示表头行
        self.log_event("TABLE_HEADER_SET", "horizontal", labels)

    # 继承自QSimWidget的日志方法
    def log_event(self, event_type, *args):
        entry = {
            'component': self,
            'event': f"[{event_type}] {', '.join(map(str, args))}",
            'path': self.get_path()
        }
        QSimLayout._logs.append(entry)  # 直接操作布局类的日志存储

    def horizontalHeader(self):
        return self.horizontal_header

    def verticalHeader(self):
        return self.vertical_header

    def setSizeAdjustPolicy(self, policy):
        """ 核心：将策略常量映射到表头调整模式 """
        policy_map = {
            self.AdjustToContents: Qt.HeaderResize.ResizeToContents,
            self.AdjustToContentsOnFirstShow: Qt.HeaderResize.Interactive
        }
        if policy in policy_map:
            mode = policy_map[policy]
            self.horizontalHeader().setSectionResizeMode(mode)
            self.verticalHeader().setSectionResizeMode(mode)
            self.log_event("TABLE_SIZE_ADJUST_POLICY", policy)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''


class QSimApplication:
    def __init__(self, args):
        QSimLayout._logs.clear()

    def log_event(self, event_type, *args):
        entry = {
            'component': None,
            'event': f"[{event_type}] {', '.join(map(str, args))}",
            'path': []
        }
        QSimLayout._logs.append(entry)

    def exec(self):
        self.log_event("APP_EXEC")
        return 0

    def exec_(self):
        self.log_event("APP_EXEC")
        return 0


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
QGroupBox = QSimGroupBox
QCheckBox = QSimCheckBox
QComboBox = QSimComboBox
QStatusBar = QSimStatusBar


# 为了方便导入，在组件类中取日志
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
    sorted_entries = sorted(QSimLayout._logs, key=cmp_to_key(compare_entries))
    return [entry['event'] for entry in sorted_entries]
