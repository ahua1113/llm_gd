import contextlib
import io

from qsim.widgets import (QSimLayout, QSimApplication, QSimListWidget, QSimSignal, QSimColor, QSimPixmap, QSimLabel,
                          QSimHBoxLayout, QSimVBoxLayout, QSimWidget, QSimFontComboBox, QSimRadioButton, QSimPushButton,
                          QSimTabWidget, QSimCheckBox, QSimGroupBox, QSimListWidgetItem, QSimComboBox, QSimTableWidget,
                          QSimTableWidgetItem, QSimSpinBox, QSimSlider, QSimFrame, QSimProgressBar, QSimStatusBar,
                          QSimHeaderView, QSimLineEdit, Qt, QSimFont, QSimGridLayout)


class LogCaptureSystem:
    def __init__(self):
        self._logs = []
        self._original_imports = {}

    def _override_imports(self):
        """劫持组件类的日志记录方法"""

        # 备份原始日志列表
        self._original_logs = QSimLayout._logs

        # 劫持日志存储地址
        QSimLayout._logs = self._logs

    def _restore_imports(self):
        """恢复原始组件引用"""

        QSimLayout._logs = self._original_logs

    @contextlib.contextmanager
    def capture_logs(self, code: str):
        """执行代码并捕获日志的上下文管理器"""
        self._logs.clear()
        self._override_imports()

        try:
            # 创建临时命名空间
            namespace = {
                'QSimApplication': QSimApplication,
                'QSimWidget': QSimWidget,
                'QSimLabel': QSimLabel,
                'QSimPushButton': QSimPushButton,
                'QSimRadioButton': QSimRadioButton,
                'QSimTabWidget': QSimTabWidget,
                'QSimCheckBox': QSimCheckBox,
                'QSimGroupBox': QSimGroupBox,
                'QSimTableWidget': QSimTableWidget,
                'QSimHeaderView': QSimHeaderView,
                'QSimTableWidgetItem': QSimTableWidgetItem,
                'QSimHBoxLayout': QSimHBoxLayout,
                'QSimVBoxLayout': QSimVBoxLayout,
                'QSimFontComboBox': QSimFontComboBox,
                'QSimSignal': QSimSignal,
                'QSimProgressBar': QSimProgressBar,
                'QSimListWidget': QSimListWidget,
                'QSimPixmap': QSimPixmap,
                'QSimColor': QSimColor,
                'QSimListWidgetItem': QSimListWidgetItem,
                'QSimComboBox': QSimComboBox,
                'QSimSpinBox': QSimSpinBox,
                'QSimSlider': QSimSlider,
                'QSimFrame': QSimFrame,
                'QSimStatusBar': QSimStatusBar,
                'QSimLineEdit': QSimLineEdit,
                'QSimFont': QSimFont,
                'QSimGridLayout': QSimGridLayout,
                'Qt': Qt
                # 包含所有需要的组件类...
            }

            # 重定向标准输出
            with io.StringIO() as buf:
                with contextlib.redirect_stdout(buf):
                    exec(code, namespace)

                # 执行应用程序事件循环
                if 'app' in namespace:
                    namespace['app'].exec_()

            yield self._logs
        finally:
            self._restore_imports()
