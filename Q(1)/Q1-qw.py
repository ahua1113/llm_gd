import os

from qsim.widgets import (QSimApplication, QSimVBoxLayout, QSimWidget, QSimLineEdit, QSimPushButton, Qt, QSimFont)
from write_new_log import writeLogNew


class LoginForm(QSimWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(300, 250)

        layout = QSimVBoxLayout()

        title = QSimLineEdit("Login")
        title.setReadOnly(True)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QSimFont("Arial", 18))
        layout.addWidget(title)

        username_input = QSimLineEdit()
        username_input.setPlaceholderText("Enter username")
        layout.addWidget(username_input)

        password_input = QSimLineEdit()
        password_input.setPlaceholderText("Enter password")
        password_input.setEchoMode(QSimLineEdit.Password)
        layout.addWidget(password_input)

        button_layout = QSimVBoxLayout()
        cancel_button = QSimPushButton("Cancel")
        submit_button = QSimPushButton("Submit")
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(submit_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QSimApplication([])
    window = LoginForm()
    window.show()
    app.exec_()

    current_file = os.path.basename(__file__)
    writeLogNew(current_file)
