from qsim.enums import Qt


class QSimLayout:
    # 由于排序逻辑是根据 HBOX 和 VBOX 来判断的，因此为便于操作，在布局类中记录所有日志
    _logs = []

    def __init__(self, parent=None):
        self._parent = parent  # 保存父组件引用
        self._parent_layout = None  # 记录父布局
        self._layout_index = 0  # 在父布局中的索引
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
        QSimLayout._logs.append(entry)

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

    def addStretch(self, stretch_factor=0):
        """ 实现拉伸因子添加 """
        self.log_event("ADD_STRETCH", stretch_factor)

    def insertStretch(self, index, stretch=0):
        self.log_event("INSERT_STRETCH", index, stretch)

    def setStretchFactor(self, widget, stretch):
        self.log_event("SET_STRETCH_FACTOR", widget.__class__.__name__, stretch)


class QSimVBoxLayout(QSimLayout):
    def __init__(self, parent=None):  # 构造函数
        super().__init__(parent=parent)  # 传递父组件参数


class QSimHBoxLayout(QSimLayout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)