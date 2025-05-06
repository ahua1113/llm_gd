from qsim.widgets import (QSimLayout, QSimApplication, QSimListWidget, QSimSignal, QSimColor, QSimPixmap, QSimLabel,
                          QSimHBoxLayout, QSimVBoxLayout, QSimWidget, QSimFontComboBox, QSimRadioButton, QSimPushButton,
                          QSimTabWidget, QSimCheckBox, QSimGroupBox, QSimListWidgetItem, QSimComboBox, QSimTableWidget,
                          QSimTableWidgetItem, QSimSpinBox, QSimSlider, QSimFrame, QSimProgressBar, QSimStatusBar,
                          QSimHeaderView, QSimLineEdit, Qt, QSimFont, QSimGridLayout)


class LoginForm(QSimWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 250)

        main_layout = QSimVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        title_label = QSimLabel("Login")
        title_label.setAlignment(Qt.AlignCenter)

        username_input = QSimLineEdit()
        username_input.setPlaceholderText("Enter username")

        password_input = QSimLineEdit()
        password_input.setPlaceholderText("Enter password")

        button_layout = QSimHBoxLayout()
        cancel_button = QSimPushButton("Cancel")
        submit_button = QSimPushButton("Submit")
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(submit_button)

        main_layout.addWidget(title_label)
        main_layout.addWidget(username_input)
        main_layout.addWidget(password_input)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)


if __name__ == '__main__':
    app = QSimApplication([])
    window = LoginForm()
    window.show()
    app.exec_()