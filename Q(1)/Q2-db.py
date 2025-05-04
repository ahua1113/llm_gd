import os

from qsim.widgets import (QSimApplication, QSimLabel,
                          QSimVBoxLayout, QSimWidget, QSimFontComboBox, Qt, QSimFont)
from write_new_log import writeLogNew


class FontSelectorDemo(QSimWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建顶部标签
        label = QSimLabel("选择字体：")
        label.setAlignment(Qt.AlignLeft)
        font = QSimFont()
        font.setPointSize(12)
        label.setFont(font)

        # 创建字体选择框
        fontComboBox = QSimFontComboBox()
        fontComboBox.currentFontChanged.connect(self.updateFont)

        # 创建示例文本标签
        self.sampleText = QSimLabel("Hello Qt!")

        # 创建垂直布局
        vbox = QSimVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(fontComboBox)
        vbox.addWidget(self.sampleText)

        # 设置布局
        self.setLayout(vbox)

        # 设置窗口固定尺寸
        self.setFixedSize(300, 150)

    def updateFont(self, font):
        self.sampleText.setFont(font)


if __name__ == '__main__':
    import sys

    app = QSimApplication(sys.argv)
    demo = FontSelectorDemo()
    demo.show()
    app.exec()

    current_file = os.path.basename(__file__)
    writeLogNew(current_file)
