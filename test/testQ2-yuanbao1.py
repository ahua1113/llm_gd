from qsimlogger import (QWidget, QLabel, QVBoxLayout, QFont,
                        QFontComboBox, QApplication, Qt)


class FontSelectorDemo(QWidget):
    """创建字体选择界面：
    1. 顶部标签"选择字体："（左对齐，12pt）
    2. 下方显示QFontComboBox控件
    3. 底部显示示例文本"Hello Qt!"（使用选中字体实时预览）
    4. 窗口固定尺寸300x150
    """

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowTitle("Font Selector Demo")

    def initUI(self):
        # 创建并配置顶部标签
        label = QLabel("选择字体：")
        label_font = QFont('Arial', 12)
        label.setFont(label_font)
        label.setAlignment(Qt.AlignLeft)

        # 初始化字体选择框
        self.font_combo = QFontComboBox()
        self.font_combo.currentFontChanged.connect(self.update_example_text)

        # 创建示例文本标签
        self.example_text = QLabel("Hello Qt!")
        self.example_text.setAlignment(Qt.AlignCenter)

        # 构建垂直布局
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.font_combo)
        layout.addWidget(self.example_text)

        # 设置窗口属性
        self.setLayout(layout)
        self.setFixedSize(300, 150)
        self.show()

    def update_example_text(self, font):
        """实时更新示例文本字体"""
        self.example_text.setFont(font)


if __name__ == '__main__':
    app = QApplication([])
    demo = FontSelectorDemo()
    app.exec_()

    # 打印捕获的日志（实际评估时输出到文件）
    from qsimlogger import get_logs
    import os

    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取根目录
    root_dir = os.path.dirname(current_dir)
    # 构建日志文本结果目录路径
    log_dir = os.path.join(root_dir, '日志文本结果')
    # 确保日志目录存在
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    current_file = os.path.basename(__file__)
    try:
        # 构建完整的文件路径
        file_path = os.path.join(log_dir, current_file + '.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            for log in get_logs():
                file.write(log + '\n')
        print(f"日志已成功写入 {file_path} 文件。")
    except Exception as e:
        print(f"写入日志到文件时出现错误: {e}")