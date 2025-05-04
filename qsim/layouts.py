from qsim.enums import Qt


class QSimLayout:
    # 由于排序逻辑是根据 HBOX 和 VBOX 来判断的，因此为便于操作，在布局类中记录所有日志
    _logs = []
    _children = []

    def __init__(self, parent=None):
        self._parent = parent  # 保存父组件引用
        self._parent_layout = None  # 记录父布局
        self._layout_index = 0  # 在父布局中的索引
        self.log_event("LAYOUT_CREATED", self.__class__.__name__)  # 调用自身方法

    def log_event(self, event_type, *args):
        # 布局自己的日志记录方法
        formatted_args = [str(arg) for arg in args]

        path = self.get_layout_path()
        # print("路径:", path)

        # print("父子关系:")
        # for child in self._children:
        #    print("索引：",child._layout_index)
        #    print("父子：",child._parent_layout)

        entry = {
            'component': self,
            'event': f"[{event_type}] {', '.join(formatted_args)}",
            'path': path
        }

        QSimLayout._logs.append(entry)

    def get_layout_path(self):
        """基于_children中的父子关系信息生成布局路径"""
        path = []
        current = self._children
        # 通过组件的父布局关系向上追溯
        for child in current:
            # 获取当前组件在父布局中的索引（从1开始）
            index = child._layout_index
            # 确定父布局类型
            parent = child._parent_layout
            layout_type = 'HBox' if isinstance(parent, QSimHBoxLayout) else 'VBox'
            # 将布局段添加到路径头部（保证根在前）
            path.insert(0, (layout_type, index))

        return path

    def addWidget(self, widget, stretch=0, alignment=None):
        widget._parent_layout = self  # 设置子组件的父布局
        # 索引从 1 开始
        widget._layout_index = len(self._children) + 1
        self._children.append(widget)

        # 记录拉伸因子
        self.log_event("ADD_WIDGET", widget.__class__.__name__, f"stretch({stretch})")

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

        layout._layout_index = len(self._children) + 1
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

    def addWidget(self, widget, stretch=0, alignment=None):
        super().addWidget(widget, stretch, alignment)

        widget._layout_index = len(self._children) + 1
        self._children.append(widget)


class QSimHBoxLayout(QSimLayout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def addWidget(self, widget, stretch=0, alignment=None):
        super().addWidget(widget, stretch, alignment)

        widget._layout_index = len(self._children) + 1
        self._children.append(widget)


class QSimGridLayout(QSimLayout):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.log_event("GRID_LAYOUT_CREATED", self.__class__.__name__)

    def addWidget(self, widget, row=0, column=0, rowSpan=1, columnSpan=1, stretch=0, alignment=None):
        """向网格布局添加组件，兼容基类参数并支持网格特性"""
        widget._parent_layout = self
        widget._layout_index = len(self._children) + 1
        self._children.append(widget)

        # 记录基类的stretch和alignment
        super().addWidget(widget, stretch=stretch, alignment=alignment)

        # 记录网格布局参数
        self.log_event("GRID_ADD_WIDGET", widget.__class__.__name__,
                      f"row={row}", f"col={column}",
                      f"rowSpan={rowSpan}", f"colSpan={columnSpan}")

        # 处理对齐方式
        if alignment:
            align_str = self._convert_alignment(alignment)
            self.log_event("GRID_WIDGET_ALIGNMENT", widget.__class__.__name__, align_str)

    def addLayout(self, layout, row=0, column=0, rowSpan=1, columnSpan=1, alignment=None):
        """向网格布局添加子布局，保持参数兼容性"""
        layout._parent_layout = self
        layout._layout_index = len(self._children) + 1
        self._children.append(layout)

        # 调用基类方法（无额外参数）
        super().addLayout(layout)

        # 记录网格布局参数
        self.log_event("GRID_ADD_LAYOUT", layout.__class__.__name__,
                      f"row={row}", f"col={column}",
                      f"rowSpan={rowSpan}", f"colSpan={columnSpan}")

        # 处理对齐方式
        if alignment:
            align_str = self._convert_alignment(alignment)
            self.log_event("GRID_LAYOUT_ALIGNMENT", layout.__class__.__name__, align_str)

    def setRowStretch(self, row, factor):
        self.log_event("GRID_ROW_STRETCH", row, factor)

    def setColumnStretch(self, column, factor):
        self.log_event("GRID_COLUMN_STRETCH", column, factor)

    def _convert_alignment(self, alignment):
        """将Qt对齐枚举转换为可读字符串"""
        alignment_map = {
            Qt.AlignLeft: "Left",
            Qt.AlignRight: "Right",
            Qt.AlignCenter: "Center",
            Qt.AlignHCenter: "HCenter",
            Qt.AlignVCenter: "VCenter",
            Qt.AlignTop: "Top",
            Qt.AlignBottom: "Bottom"
        }
        return alignment_map.get(alignment, str(alignment))
