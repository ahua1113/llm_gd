import os

from qsim.widgets import (QSimLayout, QSimApplication, QSimListWidget, QSimSignal, QSimColor, QSimPixmap, QSimLabel,
                          QSimHBoxLayout, QSimVBoxLayout, QSimWidget, QSimFontComboBox, QSimRadioButton, QSimPushButton,
                          QSimTabWidget, QSimCheckBox, QSimGroupBox, QSimListWidgetItem, QSimComboBox, QSimTableWidget,
                          QSimTableWidgetItem, QSimSpinBox, QSimSlider, QSimFrame, QSimProgressBar, QSimStatusBar,
                          QSimHeaderView, QSimLineEdit, Qt, QSimFont, QSimGridLayout)
from write_new_log import writeLogNew


class SettingsPanel(QSimWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Preferences 分组框
        preferences_group = QSimGroupBox("Preferences")
        dark_mode_checkbox = QSimCheckBox("Dark Mode")
        auto_update_checkbox = QSimCheckBox("Auto Update")

        vbox_preferences = QSimVBoxLayout()
        vbox_preferences.addWidget(dark_mode_checkbox)
        vbox_preferences.addWidget(auto_update_checkbox)
        preferences_group.setLayout(vbox_preferences)

        # Language 下拉框
        language_combo = QSimComboBox()
        language_combo.addItems(["English", "中文"])

        # 垂直布局
        vbox = QSimVBoxLayout()
        vbox.addWidget(preferences_group)
        vbox.addWidget(language_combo)

        self.setLayout(vbox)
        self.setFixedWidth(400)


if __name__ == '__main__':
    app = QSimApplication([])
    settings_panel = SettingsPanel()
    settings_panel.show()
    app.exec()

    current_file = os.path.basename(__file__)
    writeLogNew(current_file)