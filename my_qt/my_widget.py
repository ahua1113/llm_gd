from PyQt5.QtWidgets import QPushButton
print("程序开始运行")


class CustomCircleWidget:
    def __init__(self):
        print("圆形区域已初始化，初始颜色为黑色")
        self.color = "black"

    def paintEvent(self):
        print(f"正在绘制圆形，当前颜色为 {self.color}")

    def set_blue(self):
        self.color = "蓝色"
        print("变色按钮被执行，圆形已变为蓝色")

    def restore_color(self):
        self.color = "黑色"
        print("复原按钮被执行，圆形已恢复为黑色")


class CustomPushButton:
    def __init__(self, text):
        print(f"{text} 按钮已创建")
        self.text = text

    def click(self):
        print(f"{self.text} 按钮被点击")


class CustomMainWindow:
    def __init__(self):
        print("主窗口已初始化")
        self.circle_widget = CustomCircleWidget()
        blue_button = CustomPushButton("变蓝")
        restore_button = CustomPushButton("复原")

        # 模拟按钮点击
        blue_button.click()
        self.circle_widget.set_blue()
        self.circle_widget.paintEvent()
        restore_button.click()
        self.circle_widget.restore_color()
        self.circle_widget.paintEvent()


window = CustomMainWindow()
print("程序运行结束")
