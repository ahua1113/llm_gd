from qsimlogger import (QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
                        QHBoxLayout, QFont, QApplication, Qt, QFontComboBox)


class FontSelectorDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建顶部标签
        label = QLabel("选择字体：")
        label.setFont(QFont('Arial', 12))
        label.setAlignment(Qt.AlignLeft)

        # 创建 QFontComboBox 控件
        font_combo = QFontComboBox()
        font_combo.currentFontChanged.connect(self.update_example_text)

        # 创建示例文本标签
        self.example_text = QLabel("Hello Qt!")

        # 创建垂直布局
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(font_combo)
        layout.addWidget(self.example_text)

        # 设置窗口布局
        self.setLayout(layout)

        # 固定窗口尺寸
        self.setFixedSize(300, 150)

    def update_example_text(self, font):
        # 更新示例文本的字体
        self.example_text.setFont(font)


if __name__ == '__main__':
    app = QApplication([])
    demo = FontSelectorDemo()
    demo.show()
    app.exec()

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