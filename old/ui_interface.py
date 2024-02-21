from PySide6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class LoginForm(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Anmeldeformular")

        # Erstellen Sie Widgets
        self.label_email = QLabel("E-Mail:")
        self.entry_email = QLineEdit()

        self.label_password = QLabel("Passwort:")
        self.entry_password = QLineEdit()
        self.entry_password.setEchoMode(QLineEdit.Password)  # Passwort anzeigen

        self.label_totp = QLabel("TOTP:")
        self.entry_totp = QLineEdit()

        self.label_year = QLabel("Jahr:")
        self.entry_year = QLineEdit()

        self.btn_login = QPushButton("Anmelden")
        self.btn_login.clicked.connect(self.login)

        # Layout erstellen
        layout = QVBoxLayout()
        layout.addWidget(self.label_email)
        layout.addWidget(self.entry_email)
        layout.addWidget(self.label_password)
        layout.addWidget(self.entry_password)
        layout.addWidget(self.label_totp)
        layout.addWidget(self.entry_totp)
        layout.addWidget(self.label_year)
        layout.addWidget(self.entry_year)
        layout.addWidget(self.btn_login)

        self.setLayout(layout)

    def login(self):
        email = self.entry_email.text()
        password = self.entry_password.text()
        totp = self.entry_totp.text()
        year = self.entry_year.text()

        if not email or not password:
            QMessageBox.critical(self, "Fehler", "E-Mail und Passwort sind erforderlich!")
            return

        # Hier könnten Sie den Login-Prozess mit den eingegebenen Daten durchführen

        # Beispiel: Zeige die eingegebenen Daten in einer MessageBox an
        message = f"E-Mail: {email}\nPasswort: {password}\nTOTP: {totp}\nJahr: {year}"
        QMessageBox.information(self, "Login-Daten", message)

if __name__ == "__main__":
    app = QApplication([])

    login_form = LoginForm()
    login_form.show()

    app.exec()
