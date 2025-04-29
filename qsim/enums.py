class Qt:
    # 方向枚举
    Horizontal = 0
    Vertical = 1

    class AlignmentFlag:
        AlignLeft = "AlignLeft"
        AlignRight = "AlignRight"
        AlignHCenter = "AlignHCenter"
        AlignVCenter = "AlignVCenter"
        AlignCenter = "AlignCenter"
        AlignTop = "AlignTop"
        AlignBottom = "AlignBottom"

    class Alignment:
        AlignLeft = 0x0001
        AlignRight = 0x0002
        AlignCenter = 0x0004

    class ItemFlag:
        NoFlags = 0
        ItemIsEditable = 0x0001
        ItemIsSelectable = 0x0002

    class HeaderResize:
        Interactive = 0
        Fixed = 1
        Stretch = 2
        ResizeToContents = 3
        Custom = 4

    # 为测试代码提供直观的别名
    class QTableWidget:
        AdjustToContents = "AdjustToContents"  # 别名映射

    # 保持向后兼容的别名
    AlignLeft = AlignmentFlag.AlignLeft
    AlignRight = AlignmentFlag.AlignRight
    AlignHCenter = AlignmentFlag.AlignHCenter
    AlignVCenter = AlignmentFlag.AlignVCenter
    AlignCenter = AlignmentFlag.AlignCenter
    AlignTop = AlignmentFlag.AlignTop
    AlignBottom = AlignmentFlag.AlignBottom
