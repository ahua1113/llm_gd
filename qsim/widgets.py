from functools import cmp_to_key

from qsim.utils import (QSimFont, QSimSignal, QSimColor, QSimPixmap)
from qsim.layouts import (QSimHBoxLayout, QSimVBoxLayout, QSimLayout, QSimGridLayout)
from qsim.enums import Qt


class QSimWidget:
    # _logs = []

    def __init__(self, parent=None):
        self._geometry = (0, 0, 100, 100)  # (x, y, width, height)

        self._font = QSimFont()  # 所有控件基类添加字体属性

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

    def resize(self, w, h):
        self._properties['size'] = (w, h)
        self.log_event("SET_SIZE", w, h)

    def setLayout(self, layout):
        self._layout = layout
        self.log_event("SET_LAYOUT", layout.__class__.__name__)
        layout._parent = self

    def setFont(self, font):
        """ 设置字体 (兼容Qt接口) """
        if isinstance(font, QSimFont):
            self._font = font
            self.log_event("SET_FONT",
                         f"{font.family}-{font.size}-{font.bold}-{font.italic}")

    def font(self):
        return self._font

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

    def __init__(self, text=None):
        super().__init__()
        self._alignment = None
        self._echo_mode = self.Normal

        self._is_read_only = False  # 新增属性

        self.log_event("LINEEDIT_CREATED", text)

    def setPlaceholderText(self, text):
        self.log_event("PLACEHOLDER_SET", text)

    def setEchoMode(self, mode):
        self._echo_mode = mode
        mode_names = {0: "Normal", 1: "NoEcho", 2: "Password", 3: "Pin"}
        self.log_event("ECHO_MODE_SET", mode_names.get(mode, "Unknown"))

    def setReadOnly(self, read_only):
        """ 设置只读状态 """
        self._is_read_only = bool(read_only)
        # 记录状态变更（True/False）
        self.log_event("SET_READONLY", str(self._is_read_only))

    def isReadOnly(self):
        """ 获取只读状态 """
        return self._is_read_only

    def setAlignment(self, align_flag):
        """ 设置文本对齐方式 """
        self._alignment = align_flag
        self.log_event("SET_ALIGNMENT", self._alignment)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''按钮'''


class QSimPushButton(QSimWidget):
    def __init__(self, text=""):
        super().__init__()
        self._text = text
        self.clicked = QSimSignal()  # 点击信号
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


class QSimTableWidgetItem:
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


class QSimHeaderView(QSimWidget):
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


class QSimTableWidget(QSimWidget):
    # 新增调整策略常量
    AdjustToContents = "AdjustToContents"
    AdjustToContentsOnFirstShow = "AdjustToContentsOnFirstShow"

    def __init__(self, rows=0, cols=0):
        super().__init__()
        self._size_adjust_policy = None  # 策略调整相关属性

        # 自动创建带默认字体的表头
        self.horizontal_header = QSimHeaderView("horizontal")
        self.vertical_header = QSimHeaderView("vertical")

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
        if not isinstance(item, QSimTableWidgetItem):
            raise TypeError("必须使用QTableWidgetItem类型")

        self._items[(row, col)] = item
        self.log_event("TABLE_ITEM_SET", row, col, item.text)

    def cellWidget(self, row, col):
        """获取单元格中的组件"""
        return self._items.get((row, col), None)

    def setHorizontalHeaderLabels(self, labels):
        """设置水平表头"""
        for col_idx, text in enumerate(labels):
            item = QSimTableWidgetItem(text)
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
'''进度条组件'''


class QSimProgressBar(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._min = 0
        self._max = 100
        self._value = 0
        self._orientation = Qt.Horizontal  # 使用框架中的Qt枚举
        self._text_visible = True
        self.valueChanged = QSimSignal()  # 初始化值变化信号
        self.log_event("PROGRESSBAR_CREATED")

    def setMinimum(self, min_val):
        """设置最小值并记录日志"""
        if self._min != min_val:
            self._min = min_val
            self.log_event("PROGRESSBAR_MIN_SET", min_val)
            self._clamp_value()

    def setMaximum(self, max_val):
        """设置最大值并记录日志"""
        if self._max != max_val:
            self._max = max_val
            self.log_event("PROGRESSBAR_MAX_SET", max_val)
            self._clamp_value()

    def setRange(self, min_val, max_val):
        """同时设置范围并优化日志记录"""
        changed = False
        if self._min != min_val:
            self._min = min_val
            changed = True
        if self._max != max_val:
            self._max = max_val
            changed = True
        if changed:
            self.log_event("PROGRESSBAR_RANGE_SET", min_val, max_val)
            self._clamp_value()

    def _clamp_value(self):
        """确保当前值在有效范围内"""
        new_value = max(self._min, min(self._value, self._max))
        if new_value != self._value:
            self.setValue(new_value)

    def setValue(self, value):
        """设置当前值并触发信号"""
        clamped_value = max(self._min, min(value, self._max))
        if self._value != clamped_value:
            self._value = clamped_value
            self.log_event("PROGRESSBAR_VALUE_SET", clamped_value)
            self.valueChanged.emit(clamped_value)

    def setOrientation(self, orientation):
        """设置进度条方向"""
        orientation_map = {
            Qt.Horizontal: "Horizontal",
            Qt.Vertical: "Vertical"
        }
        if self._orientation != orientation:
            self._orientation = orientation
            self.log_event("PROGRESSBAR_ORIENTATION_SET",
                           orientation_map.get(orientation, str(orientation)))

    def setTextVisible(self, visible):
        """设置文本可见性"""
        if self._text_visible != visible:
            self._text_visible = visible
            self.log_event("PROGRESSBAR_TEXT_VISIBILITY",
                           "Visible" if visible else "Hidden")

    def value(self):
        """获取当前值"""
        return self._value


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''标签页组件'''


class QSimTabWidget(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._tabs = []  # 保存元组（组件, 标题, 图标）
        self._current_index = -1
        self.currentChanged = QSimSignal()  # 当前页变化信号
        self.log_event("TABWIDGET_CREATED")

    def addTab(self, widget, label):
        """添加新标签页"""
        self._tabs.append((widget, label, None))
        widget._parent = self  # 设置子组件的父级
        index = len(self._tabs) - 1
        self.log_event("TAB_ADDED", label, widget.__class__.__name__, index)

        # 自动选择第一个标签页
        if self._current_index == -1:
            self.setCurrentIndex(0)

    def insertTab(self, index, widget, label):
        """插入标签页到指定位置"""
        self._tabs.insert(index, (widget, label, None))
        widget._parent = self
        # 更新后续标签页的布局索引
        for i in range(index + 1, len(self._tabs)):
            tab_widget = self._tabs[i][0]
            tab_widget._layout_index = i
        self.log_event("TAB_INSERTED", index, label, widget.__class__.__name__)

        if self._current_index >= index:
            self._current_index += 1

    def setCurrentIndex(self, index):
        """设置当前选中的标签页"""
        if index < 0 or index >= len(self._tabs):
            return
        if self._current_index != index:
            prev_index = self._current_index
            self._current_index = index
            self.log_event("TAB_SWITCHED", prev_index, index)
            self.currentChanged.emit(index)

    def setTabText(self, index, text):
        """修改标签页文本"""
        if 0 <= index < len(self._tabs):
            widget, old_text, icon = self._tabs[index]
            self._tabs[index] = (widget, text, icon)
            self.log_event("TAB_TEXT_CHANGED", index, old_text, text)

    def setTabIcon(self, index, icon):
        """设置标签页图标"""
        if 0 <= index < len(self._tabs):
            widget, text, old_icon = self._tabs[index]
            self._tabs[index] = (widget, text, icon)
            icon_info = f"{icon.width}x{icon.height}" if icon else "None"
            self.log_event("TAB_ICON_SET", index, icon_info)

    def currentWidget(self):
        """获取当前显示的组件"""
        if self._current_index != -1:
            return self._tabs[self._current_index][0]
        return None

    def count(self):
        """获取标签页数量"""
        return len(self._tabs)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''数字输入框组件'''


class QSimSpinBox(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._min = 0
        self._max = 100
        self._value = 0
        self._step = 1
        self.valueChanged = QSimSignal()  # 数值变化信号
        self.log_event("SPINBOX_CREATED")

    def setMinimum(self, min_val):
        if self._min != min_val:
            self._min = min_val
            self.log_event("SPINBOX_MIN_SET", min_val)
            self._clamp_value()

    def setMaximum(self, max_val):
        if self._max != max_val:
            self._max = max_val
            self.log_event("SPINBOX_MAX_SET", max_val)
            self._clamp_value()

    def setRange(self, min_val, max_val):
        changed = False
        if self._min != min_val:
            self._min = min_val
            changed = True
        if self._max != max_val:
            self._max = max_val
            changed = True
        if changed:
            self.log_event("SPINBOX_RANGE_SET", min_val, max_val)
            self._clamp_value()

    def setValue(self, value):
        clamped_value = max(self._min, min(value, self._max))
        if self._value != clamped_value:
            self._value = clamped_value
            self.log_event("SPINBOX_VALUE_SET", clamped_value)
            self.valueChanged.emit(clamped_value)

    def setSingleStep(self, step):
        if self._step != step:
            self._step = step
            self.log_event("SPINBOX_STEP_SET", step)

    def value(self):
        return self._value

    def _clamp_value(self):
        """确保当前值在有效范围内"""
        self.setValue(self._value)  # 强制重新校验当前值


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''滑块组件'''


class QSimSlider(QSimWidget):
    def __init__(self, orientation=Qt.Horizontal, parent=None):
        super().__init__(parent=parent)
        self._min = 0
        self._max = 100
        self._value = 0
        self._orientation = orientation
        self.valueChanged = QSimSignal()  # 数值变化信号
        self.sliderMoved = QSimSignal()  # 滑块拖动信号
        self.log_event("SLIDER_CREATED", "Horizontal" if orientation == Qt.Horizontal else "Vertical")

    def setMinimum(self, min_val):
        if self._min != min_val:
            self._min = min_val
            self.log_event("SLIDER_MIN_SET", min_val)
            self._clamp_value()

    def setMaximum(self, max_val):
        if self._max != max_val:
            self._max = max_val
            self.log_event("SLIDER_MAX_SET", max_val)
            self._clamp_value()

    def setRange(self, min_val, max_val):
        changed = False
        if self._min != min_val:
            self._min = min_val
            changed = True
        if self._max != max_val:
            self._max = max_val
            changed = True
        if changed:
            self.log_event("SLIDER_RANGE_SET", min_val, max_val)
            self._clamp_value()

    def setValue(self, value):
        clamped_value = max(self._min, min(value, self._max))
        if self._value != clamped_value:
            self._value = clamped_value
            self.log_event("SLIDER_VALUE_SET", clamped_value)
            self.valueChanged.emit(clamped_value)

    def value(self):
        return self._value

    def setOrientation(self, orientation):
        if self._orientation != orientation:
            self._orientation = orientation
            orient_str = "Horizontal" if orientation == Qt.Horizontal else "Vertical"
            self.log_event("SLIDER_ORIENTATION_SET", orient_str)

    def sliderPosition(self):
        """获取滑块当前位置（模拟值为当前值）"""
        return self._value

    def _clamp_value(self):
        """确保当前值在有效范围内"""
        self.setValue(self._value)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''单选按钮组件'''


class QSimRadioButton(QSimWidget):
    def __init__(self, text="", parent=None):
        super().__init__(parent=parent)
        self._text = text
        self._checked = False
        self.toggled = QSimSignal(bool)  # 状态变化信号（携带布尔值）
        self.log_event("RADIOBUTTON_CREATED", text)

    def setText(self, text):
        self._text = text
        self.log_event("RADIOBUTTON_TEXT_CHANGED", text)

    def isChecked(self):
        return self._checked

    def setChecked(self, checked):
        if self._checked != checked:
            self._checked = checked
            self.log_event("RADIOBUTTON_CHECKED" if checked else "RADIOBUTTON_UNCHECKED")
            self.toggled.emit(checked)  # 触发信号

    def text(self):
        return self._text


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''框架组件'''


class QSimFrame(QSimWidget):
    # 边框样式枚举（模拟Qt的QFrame.Shape）
    NoFrame = 0
    Box = 1
    Panel = 2
    WinPanel = 3
    HLine = 4
    VLine = 5
    StyledPanel = 6

    # 阴影样式枚举（模拟Qt的QFrame.Shadow）
    Plain = 0
    Raised = 1
    Sunken = 2

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._frame_shape = self.NoFrame
        self._frame_shadow = self.Plain
        self._line_width = 1
        self.log_event("FRAME_CREATED")

    def setFrameShape(self, shape):
        shape_names = {
            self.NoFrame: "NoFrame",
            self.Box: "Box",
            self.Panel: "Panel",
            self.HLine: "HLine",
            self.VLine: "VLine"
        }
        if self._frame_shape != shape:
            self._frame_shape = shape
            self.log_event("FRAME_SHAPE_SET", shape_names.get(shape, "Unknown"))

    def setFrameShadow(self, shadow):
        shadow_names = {
            self.Plain: "Plain",
            self.Raised: "Raised",
            self.Sunken: "Sunken"
        }
        if self._frame_shadow != shadow:
            self._frame_shadow = shadow
            self.log_event("FRAME_SHADOW_SET", shadow_names.get(shadow, "Unknown"))

    def setLineWidth(self, width):
        if self._line_width != width:
            self._line_width = width
            self.log_event("FRAME_LINE_WIDTH_SET", width)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''列表组件'''


class QSimListWidgetItem:
    def __init__(self, text=""):
        self.text = text
        self._flags = Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable  # 默认标志

    def setText(self, text):
        self.text = text

    def setFlags(self, flags):
        self._flags = flags


class QSimListWidget(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._items = []
        self._current_row = -1
        self.itemClicked = QSimSignal(QSimListWidgetItem)  # 点击项信号
        self.currentRowChanged = QSimSignal(int)  # 当前行变化信号
        self.log_event("LISTWIDGET_CREATED")

    def addItem(self, text):
        item = QSimListWidgetItem(text)
        self._items.append(item)
        self.log_event("LISTWIDGET_ITEM_ADDED", text, f"row={len(self._items) - 1}")

    def addItems(self, texts):
        for text in texts:
            self.addItem(text)
        self.log_event("LISTWIDGET_ITEMS_ADDED", len(texts))

    def setCurrentRow(self, row):
        if row < -1 or row >= len(self._items):
            return
        if self._current_row != row:
            prev_row = self._current_row
            self._current_row = row
            self.log_event("LISTWIDGET_ROW_CHANGED", prev_row, row)
            self.currentRowChanged.emit(row)  # 触发信号
            if row != -1:
                self.itemClicked.emit(self._items[row])  # 模拟点击事件

    def currentItem(self):
        return self._items[self._current_row] if self._current_row != -1 else None

    def clear(self):
        self._items.clear()
        self._current_row = -1
        self.log_event("LISTWIDGET_CLEARED")


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
    # print("before:", QSimLayout._logs)

    sorted_entries = sorted(QSimLayout._logs, key=cmp_to_key(compare_entries))

    # print("after:", sorted_entries)

    return [entry['event'] for entry in sorted_entries]
