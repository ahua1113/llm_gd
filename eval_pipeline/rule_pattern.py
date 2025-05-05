# 问题验证规则
import re
from typing import List


Q1_PATTERN = {
    "1": r"'event':\s*'\[LABEL_CREATED\] Login'.*",
    "2": r"'event':\s*'\[PLACEHOLDER_SET\] Enter username'.*",
    "3": r"'event':\s*'\[PLACEHOLDER_SET\] Enter password'.*",
    "4": r"'event':\s*'\[ECHO_MODE_SET\] password'.*",
    "5": r"'event':\s*'\[BUTTON_CREATED\] Cancel'.*",
    "6": r"'event':\s*'\[BUTTON_CREATED\] Submit'.*",
    "7": r"'event':\s*'\[LAYOUT_ALIGNMENT_SET\] AlignCenter'.*",
    "8": r"'event':\s*'\[SET_SIZE\] 300, 250'.*"

}

Q2_PATTERN = {
    "1": r"'event':\s*'\[LABEL_CREATED\] 选择字体：'.*",
    "2": r"'event':\s*'\[ALIGNMENT_SET\] Left'.*",
    "3": r"'event':\s*'\[FONT_SIZE_SET\] 12'.*",
    "4": r"'event':\s*'\[WIDGET_CREATED\] QSimFontComboBox'.*",
    "5": r"'event':\s*'\[SIGNAL_CONNECT\] Connected to updateFont'.*",
    "6": r"'event':\s*'\[LABEL_CREATED\] Hello Qt!'.*",
    "7": r"'event':\s*'\[SET_SIZE\] 300, 150'.*"
}

Q3_PATTERN = {
    "1": r"'event':\s*'\[WIDGET_CREATED\] QSimLabel'.*",
    "2": r"'event':\s*'\[STYLESHEET_SET\] background-color: gray;'.*",
    "3": r"'event':\s*'\[SET_SIZE\] 100, 100'.*",
    "4": r"'event':\s*'\[FONT_SIZE_SET\] 14'.*",
    "5": r"'event':\s*'\[ALIGNMENT_SET\] Center'.*",
    "6": r"'event':\s*'\[WIDGET_CREATED\] QSimFrame'.*",
    "7": r"'event':\s*'\[FRAME_SHAPE_SET\] HLine'.*",
    "8": r"'event':\s*'\[STYLESHEET_SET\] color: black;'.*",
    "9": r"'event':\s*'\[SET_SIZE\] 200, 220'.*"
}

Q4_PATTERN = {
    "1": r"'event':\s*'\[GROUPBOX_CREATED\] Preferences'.*",
    "2": r"'event':\s*'\[WIDGET_CREATED\] QSimCheckBox'.*",
    "3": r"'event':\s*'\[CHECKBOX_CREATED\] Dark Mode'.*",
    "4": r"'event':\s*'\[CHECKBOX_CREATED\] Auto Update'.*",
    "5": r"'event':\s*'\[WIDGET_CREATED\] QSimComboBox'.*",
    "6": r"'event':\s*'\[COMBOBOX_ITEM_ADDED\] English'.*",
    "7": r"'event':\s*'\[COMBOBOX_ITEM_ADDED\] 中文'.*",
    "8": r"'event':\s*'\[SET_FIXED_WIDTH\] 400'.*"
}

Q5_PATTERN = {
    "1": r"'event':\s*'\[LABEL_CREATED\] Placeholder Image'.*",
    "2": r"'event':\s*'\[FONT_ITALIC_SET\] True'.*",
    "3": r"'event':\s*'\[STYLESHEET_SET\] color: gray;'.*",
    "4": r"'event':\s*'\[WIDGET_CREATED\] QSimLabel'.*",
    "5": r"'event':\s*'\[STYLESHEET_SET\] background-color: gray;'.*",
    "6": r"'event':\s*'\[SET_SIZE\] 200, 200'.*",
    "7": r"'event':\s*'\[WIDGET_CREATED\] QSimStatusBar'.*",
    "8": r"'event':\s*'\[STATUS_SET\] Ready'.*",
    "9": r"'event':\s*'\[SET_SIZE\] 250, 300'.*"
}

Q6_PATTERN = {
    "1": r"'event':\s*'\[WIDGET_CREATED\] QSimTableWidget'.*",
    "2": r"'event':\s*'\[TABLE_COLUMN_SET\] 3'.*",
    "3": r"'event':\s*'\[HEADER_CREATED\] Name'.*",
    "4": r"'event':\s*'\[HEADER_CREATED\] Age'.*",
    "5": r"'event':\s*'\[HEADER_CREATED\] Department'.*"
}

Q7_PATTERN = {
    "1": r"'event':\s*'\[LABEL_CREATED\] Processing...'.*",
    "2": r"'event':\s*'\[STYLESHEET_SET\] color: blue;'.*",
    "3": r"'event':\s*'\[WIDGET_CREATED\] QSimProgressBar'.*",
    "4": r"'event':\s*'\[PROGRESS_SET\] 50'.*",
    "5": r"'event':\s*'\[LABEL_CREATED\] Step 2/4'.*",
    "6": r"'event':\s*'\[LAYOUT_ALIGNMENT_SET\] AlignVCenter'.*",
    "7": r"'event':\s*'\[SET_FIXED_HEIGHT\] 150'.*"
}

Q8_PATTERN = {
    "1": r"'event':\s*'\[WIDGET_CREATED\] QSimTabWidget'.*",
    "2": r"'event':\s*'\[TAB_ADDED\] General'.*",
    "3": r"'event':\s*'\[TAB_ADDED\] Advanced'.*",
    "4": r"'event':\s*'\[GROUPBOX_CREATED\] Settings'.*",
    "5": r"'event':\s*'\[WIDGET_CREATED\] QSimLabel'.*",
    "6": r"'event':\s*'\[LABEL_CREATED\] \[!\]'.*",
    "7": r"'event':\s*'\[STYLESHEET_SET\] color: red;'.*",
    "8": r"'event':\s*'\[SET_SIZE\] 400, 300'.*"
}

Q9_PATTERN = {
    "1": r"'event':\s*'\[WIDGET_CREATED\] QSimPushButton'.*",
    "2": r"'event':\s*'\[BUTTON_CREATED\] \[Icon\]'.*",
    "3": r"'event':\s*'\[WIDGET_CREATED\] QSimFrame'.*",
    "4": r"'event':\s*'\[FRAME_SHAPE_SET\] HLine'.*",
    "5": r"'event':\s*'\[STYLESHEET_SET\] color: gray;'.*",
    "6": r"'event':\s*'\[SET_FIXED_WIDTH\] 600'.*",
    "7": r"'event':\s*'\[SET_FIXED_HEIGHT\] 80'.*"
}

Q10_PATTERN = {
    "1": r"'event':\s*'\[STYLESHEET_SET\] background-color: lightyellow; border-radius: \d+px;'.*",
    "2": r"'event':\s*'\[WIDGET_CREATED\] QSimLabel'.*",
    "3": r"'event':\s*'\[LABEL_CREATED\] \[!\]'.*",
    "4": r"'event':\s*'\[LABEL_CREATED\] System maintenance\nScheduled at 3:00 AM'.*",
    "5": r"'event':\s*'\[SET_SIZE\] 350, 100'.*"
}


# 通用规则结构定义
Rule = List[dict]


# 传入日志内容，返回匹配成功的比率
def validate_log(text: str):
    patterns = Q1_PATTERN

    results = {key: False for key in patterns}

    for line in text.split('\n'):
        for key, pattern in patterns.items():
            if re.search(pattern, line):
                results[key] = True

    # 计算results中为true的key个数
    count = sum(1 for value in results.values() if value)

    # 返回匹配成功的比率
    return count / len(results) if count > 0 else 0.0  # 防止除以0的情况，返回0.0表示没有匹配成功的key


# 使用示例
if __name__ == "__main__":
    file_path = '../日志结果-new/Q4-db.py.txt'
    with open(file_path, 'r', encoding='utf-8') as f:
        log_content = f.read()

    res = validate_log(log_content)
    print(res)
