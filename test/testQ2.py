from scrap.qsimlogger import (QWidget, QLabel, QLineEdit, QVBoxLayout, QFont, QApplication, Qt)

class FontSelectorDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Font Selector Demo")
        self.setFixedSize(300, 150)

        # 创建主布局
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # 创建顶部标签
        label = QLabel("选择字体：")
        label_font = QFont()
        label_font.setPointSize(12)
        label.setFont(label_font)
        label.setAlignment(Qt.AlignCenter)  # 使用文档中存在的对齐属性

        # 创建字体选择框（模拟QFontComboBox）
        font_combo = QLineEdit()
        font_combo.setPlaceholderText("请选择字体...")

        # 创建示例文本标签
        example_label = QLabel("Hello Qt!")
        example_label.setAlignment(Qt.AlignCenter)

        # 添加组件到布局
        main_layout.addWidget(label)
        main_layout.addWidget(font_combo)
        main_layout.addWidget(example_label)

        # 设置布局边距和间距
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)


if __name__ == '__main__':
    app = QApplication([])
    Demo = FontSelectorDemo()
    app.exec()

    # 打印捕获的日志（实际评估时输出到文件）
    from scrap.qsimlogger import get_logs
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