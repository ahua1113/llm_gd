from qsim.utils import QSimSignal
from qsim.widgets import (QSimWidget, QSimLayout)

'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''日期编辑框组件'''


class QSimDateEdit(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._date = (2000, 1, 1)  # (年, 月, 日)
        self._min_date = (1900, 1, 1)
        self._max_date = (3000, 12, 31)
        self._display_format = "yyyy-MM-dd"
        self.dateChanged = QSimSignal(tuple)  # 日期变化信号
        self.log_event("DATEEDIT_CREATED")

    def setDate(self, year, month, day):
        """设置当前日期并进行有效性校验"""
        new_date = (year, month, day)
        if self._is_valid_date(new_date) and new_date != self._date:
            self._date = new_date
            self.log_event("DATEEDIT_DATE_SET", f"{year}-{month}-{day}")
            self.dateChanged.emit(new_date)

    def setMinimumDate(self, year, month, day):
        """设置最小允许日期"""
        new_min = (year, month, day)
        if self._is_valid_date(new_min):
            self._min_date = new_min
            self.log_event("DATEEDIT_MIN_DATE_SET", f"{year}-{month}-{day}")
            self._clamp_date()

    def setMaximumDate(self, year, month, day):
        """设置最大允许日期"""
        new_max = (year, month, day)
        if self._is_valid_date(new_max):
            self._max_date = new_max
            self.log_event("DATEEDIT_MAX_DATE_SET", f"{year}-{month}-{day}")
            self._clamp_date()

    def setDisplayFormat(self, format_str):
        """设置日期显示格式"""
        if self._display_format != format_str:
            self._display_format = format_str
            self.log_event("DATEEDIT_FORMAT_SET", format_str)

    def _is_valid_date(self, date_tuple):
        """简易日期有效性检查"""
        year, month, day = date_tuple
        return (self._min_date <= date_tuple <= self._max_date and
                1 <= month <= 12 and
                1 <= day <= 31)

    def _clamp_date(self):
        """确保当前日期在有效范围内"""
        if not self._is_valid_date(self._date):
            self.setDate(*self._date)  # 强制重新校验设置

    def date(self):
        """获取当前日期"""
        return self._date


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''日历组件'''


class QSimCalendarWidget(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._selected_date = (2000, 1, 1)
        self._min_date = (1900, 1, 1)
        self._max_date = (3000, 12, 31)
        self.selectionChanged = QSimSignal(tuple)  # 日期选择变化信号
        self.log_event("CALENDAR_CREATED")

    def setSelectedDate(self, year, month, day):
        """设置当前选中日期"""
        new_date = (year, month, day)
        if self._is_valid_date(new_date) and new_date != self._selected_date:
            self._selected_date = new_date
            self.log_event("CALENDAR_DATE_SET", f"{year}-{month}-{day}")
            self.selectionChanged.emit(new_date)

    def setMinimumDate(self, year, month, day):
        """设置最小可选日期"""
        new_min = (year, month, day)
        if self._is_valid_date(new_min):
            self._min_date = new_min
            self.log_event("CALENDAR_MIN_DATE_SET", f"{year}-{month}-{day}")
            self._clamp_selection()

    def setMaximumDate(self, year, month, day):
        """设置最大可选日期"""
        new_max = (year, month, day)
        if self._is_valid_date(new_max):
            self._max_date = new_max
            self.log_event("CALENDAR_MAX_DATE_SET", f"{year}-{month}-{day}")
            self._clamp_selection()

    def selectedDate(self):
        """获取当前选中日期"""
        return self._selected_date

    def _is_valid_date(self, date_tuple):
        """日期范围有效性检查"""
        return self._min_date <= date_tuple <= self._max_date

    def _clamp_selection(self):
        """确保选中日期在有效范围内"""
        if not self._is_valid_date(self._selected_date):
            self.setSelectedDate(*self._selected_date)  # 强制重新校验设置


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''滚动区域组件'''


class QSimScrollArea(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._widget = None  # 子部件
        self._horizontal_policy = "AsNeeded"  # 水平滚动条策略
        self._vertical_policy = "AsNeeded"  # 垂直滚动条策略

        self._widget_resizable = False  # 新增属性：是否自动调整子部件大小

        self.widgetChanged = QSimSignal(QSimWidget)  # 子部件变化信号
        self.log_event("SCROLLAREA_CREATED")

    def setWidget(self, widget):
        """设置滚动区域内的子部件"""
        if isinstance(widget, QSimWidget) and widget != self._widget:
            self._widget = widget
            self.log_event("SCROLLAREA_WIDGET_SET", widget.__class__.__name__)
            self.widgetChanged.emit(widget)

    def widget(self):
        """获取当前子部件"""
        return self._widget

    def setHorizontalScrollBarPolicy(self, policy):
        """设置水平滚动条策略
        可选值: "AlwaysOff", "AlwaysOn", "AsNeeded"
        """
        valid_policies = ["AlwaysOff", "AlwaysOn", "AsNeeded"]
        if policy in valid_policies and policy != self._horizontal_policy:
            self._horizontal_policy = policy
            self.log_event("SCROLLAREA_HORIZONTAL_POLICY_SET", policy)

    def setVerticalScrollBarPolicy(self, policy):
        """设置垂直滚动条策略
        可选值: "AlwaysOff", "AlwaysOn", "AsNeeded"
        """
        valid_policies = ["AlwaysOff", "AlwaysOn", "AsNeeded"]
        if policy in valid_policies and policy != self._vertical_policy:
            self._vertical_policy = policy
            self.log_event("SCROLLAREA_VERTICAL_POLICY_SET", policy)

    def horizontalScrollBarPolicy(self):
        """获取当前水平滚动条策略"""
        return self._horizontal_policy

    def verticalScrollBarPolicy(self):
        """获取当前垂直滚动条策略"""
        return self._vertical_policy

    # 新增方法：设置是否自动调整子部件大小
    def setWidgetResizable(self, resizable):
        """设置是否自动调整子部件大小"""
        if isinstance(resizable, bool) and resizable != self._widget_resizable:
            self._widget_resizable = resizable
            self.log_event("SCROLLAREA_WIDGET_RESIZABLE_SET", str(resizable))


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''分割器组件'''


class QSimSplitter(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._children = []  # 子部件列表
        self._orientation = "Horizontal"  # 方向: Horizontal/Vertical
        self._sizes = []  # 分割比例
        self.splitterMoved = QSimSignal(int, int)  # 参数: 索引, 新位置
        self.log_event("SPLITTER_CREATED")

    def addWidget(self, widget):
        """添加子部件到末尾"""
        if isinstance(widget, QSimWidget):
            self._children.append(widget)
            self._update_sizes()
            self.log_event("SPLITTER_ADD_WIDGET", widget.__class__.__name__)

    def insertWidget(self, index, widget):
        """在指定位置插入子部件"""
        if isinstance(widget, QSimWidget) and 0 <= index <= len(self._children):
            self._children.insert(index, widget)
            self._update_sizes()
            self.log_event("SPLITTER_INSERT_WIDGET", (index, widget.__class__.__name__))

    def setOrientation(self, orientation):
        """设置分割方向
        有效值: "Horizontal", "Vertical"
        """
        if orientation in ("Horizontal", "Vertical") and orientation != self._orientation:
            self._orientation = orientation
            self.log_event("SPLITTER_ORIENTATION_CHANGED", orientation)

    def setSizes(self, sizes):
        """设置分割比例
        示例: [2, 1] 表示2:1比例
        """
        if len(sizes) == len(self._children) and all(isinstance(x, int) for x in sizes):
            self._sizes = sizes
            self.log_event("SPLITTER_SIZES_SET", str(sizes))
            self.splitterMoved.emit(-1, 0)  # 模拟整体变化信号

    def _update_sizes(self):
        """子部件数量变化时自动调整比例为均分"""
        if self._children:
            self._sizes = [100] * len(self._children)

    def orientation(self):
        return self._orientation

    def sizes(self):
        return self._sizes.copy()

    def count(self):
        return len(self._children)

    def widget(self, index):
        """获取指定索引的子部件"""
        if 0 <= index < len(self._children):
            return self._children[index]
        return None


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''富文本编辑框组件'''


class QSimTextEdit(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._text = ""
        self._is_readonly = False
        self.textChanged = QSimSignal(str)  # 文本变化信号
        self.log_event("TEXTEDIT_CREATED")

    def setText(self, text):
        """设置编辑框内容"""
        if isinstance(text, str) and text != self._text:
            self._text = text
            self.log_event("TEXTEDIT_TEXT_SET", f"Length:{len(text)}")
            self.textChanged.emit(text)

    def toPlainText(self):
        """获取纯文本内容"""
        return self._text

    def setReadOnly(self, readonly):
        """设置只读状态"""
        if isinstance(readonly, bool) and readonly != self._is_readonly:
            self._is_readonly = readonly
            self.log_event("TEXTEDIT_READONLY_SET", str(readonly))

    def isReadOnly(self):
        return self._is_readonly

    def append(self, text):
        """追加文本内容"""
        if isinstance(text, str):
            self._text += text
            self.log_event("TEXTEDIT_APPEND", f"Length:{len(text)}")
            self.textChanged.emit(self._text)


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''数码管显示组件'''


class QSimLCDNumber(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._value = 0                # 当前显示值
        self._digit_count = 4          # 显示位数
        self._mode = "Dec"             # 显示模式：Dec/Hex/Bin
        self._segment_style = "Filled" # 段样式：Filled/Outline
        self.valueChanged = QSimSignal(int)  # 值变化信号
        self.log_event("LCDNUMBER_CREATED")

    def setValue(self, value):
        """设置显示数值"""
        if isinstance(value, int) and value != self._value:
            self._value = value
            self.log_event("LCDNUMBER_VALUE_SET", str(value))
            self.valueChanged.emit(value)

    def setDigitCount(self, num):
        """设置显示位数"""
        if isinstance(num, int) and num > 0 and num != self._digit_count:
            self._digit_count = num
            self.log_event("LCDNUMBER_DIGIT_CHANGED", str(num))

    def setMode(self, mode):
        """设置显示模式
        有效值: "Dec"(十进制), "Hex"(十六进制), "Bin"(二进制)
        """
        valid_modes = ["Dec", "Hex", "Bin"]
        if mode in valid_modes and mode != self._mode:
            self._mode = mode
            self.log_event("LCDNUMBER_MODE_CHANGED", mode)

    def setSegmentStyle(self, style):
        """设置段显示样式
        有效值: "Filled"(实心), "Outline"(空心)
        """
        valid_styles = ["Filled", "Outline"]
        if style in valid_styles and style != self._segment_style:
            self._segment_style = style
            self.log_event("LCDNUMBER_STYLE_CHANGED", style)

    def value(self):
        return self._value

    def digitCount(self):
        return self._digit_count

    def mode(self):
        return self._mode

    def segmentStyle(self):
        return self._segment_style

    def display(self, value):
        """设置显示数值并记录日志"""
        self._value = value
        # 生成标准日志条目
        log_entry = {
            'component': self,
            'event': f"[DISPLAY_SET] {value}",
            'path': []
        }
        QSimLayout._logs.append(log_entry)

    def get_value(self):  # 可选：提供获取当前显示值的接口
        return self._value


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''
'''刻度旋钮组件'''


class QSimDial(QSimWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._min = 0                  # 最小值
        self._max = 99                 # 最大值
        self._value = 0                # 当前值
        self._step = 1                 # 单步长
        self._notch_visible = False    # 是否显示刻度
        self.valueChanged = QSimSignal(int)  # 值变化信号
        self.log_event("DIAL_CREATED")

    def setRange(self, min_val, max_val):
        """设置取值范围"""
        if isinstance(min_val, int) and isinstance(max_val, int) and min_val < max_val:
            self._min = min_val
            self._max = max_val
            self._clamp_value()
            self.log_event("DIAL_RANGE_SET", f"{min_val}-{max_val}")

    def setValue(self, value):
        """设置当前值并触发范围钳制"""
        if isinstance(value, int):
            clamped = max(self._min, min(value, self._max))
            if clamped != self._value:
                self._value = clamped
                self.log_event("DIAL_VALUE_SET", str(clamped))
                self.valueChanged.emit(clamped)

    def setSingleStep(self, step):
        """设置步进值"""
        if isinstance(step, int) and step > 0 and step != self._step:
            self._step = step
            self.log_event("DIAL_STEP_CHANGED", str(step))

    def setNotchVisible(self, visible):
        """设置刻度可见性"""
        if isinstance(visible, bool) and visible != self._notch_visible:
            self._notch_visible = visible
            self.log_event("DIAL_NOTCH_TOGGLED", str(visible))

    def _clamp_value(self):
        """确保当前值在有效范围内"""
        self.setValue(self._value)  # 通过setValue自动钳制

    def value(self):
        return self._value

    def minimum(self):
        return self._min

    def maximum(self):
        return self._max

    def singleStep(self):
        return self._step

    def isNotchVisible(self):
        return self._notch_visible


'''—————————————————————————————————————————————分割线———————————————————————————————————————————————————————————————'''


QLCDNumber = QSimLCDNumber
QDial = QSimDial
QSplitter = QSimSplitter
QTextEdit = QSimTextEdit
QScrollArea = QSimScrollArea
QCalendarWidget = QSimCalendarWidget
QDateEdit = QSimDateEdit
