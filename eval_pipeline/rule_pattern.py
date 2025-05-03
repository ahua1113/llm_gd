# 问题验证规则
from typing import List

Q1_PATTERN = [
    {"type": "WIDGET_CREATED", "class": "QSimWidget", "path": []},
    {"type": "SET_LAYOUT", "layout": "QSimVBoxLayout", "path": []},
    {
        "type": "WIDGET_CREATED",
        "class": "QSimPushButton",
        "path": [("VBox", 0)]
    },
    {
        "type": "LABEL_CREATED",
        "text": "Hello World",
        "path": [("VBox", 1)]
    }
]

# 通用规则结构定义
Rule = List[dict]
