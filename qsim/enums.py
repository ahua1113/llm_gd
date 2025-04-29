class Qt:
    # 枚举类
    class AlignmentFlag:
        AlignLeft = "AlignLeft"
        AlignRight = "AlignRight"
        AlignHCenter = "AlignHCenter"
        AlignVCenter = "AlignVCenter"
        AlignCenter = "AlignCenter"
        AlignTop = "AlignTop"
        AlignBottom = "AlignBottom"

    # 保持向后兼容的别名
    AlignLeft = AlignmentFlag.AlignLeft
    AlignRight = AlignmentFlag.AlignRight
    AlignHCenter = AlignmentFlag.AlignHCenter
    AlignVCenter = AlignmentFlag.AlignVCenter
    AlignCenter = AlignmentFlag.AlignCenter
    AlignTop = AlignmentFlag.AlignTop
    AlignBottom = AlignmentFlag.AlignBottom
