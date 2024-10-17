from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QApplication,
    QMessageBox,
    QDialog,
)
from PySide6.QtGui import QFont, QIntValidator
from PySide6.QtCore import Qt
import sys

# Dein TotpPopup-Dialog
class TotpPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.totp_value = None  # Initialisiere den TOTP-Wert
        self.initUI()

    def initUI(self):
        self.setWindowTitle("TOTP-Abfrage")
        self.setFixedSize(400, 200)

        # Label für die Beschreibung
        label = QLabel("Bitte 6-stelligen TOTP eingeben:", self)
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 12))

        # Erstellen von 6 Eingabefeldern für die TOTP-Ziffern
        self.digits = []
        digits_layout = QHBoxLayout()

        for i in range(6):
            digit_input = QLineEdit(self)
            if i == 0:
                digit_input.setMaxLength(6)
                digit_input.setValidator(QIntValidator(0, 999999, self))
            else:
                digit_input.setMaxLength(1)
                digit_input.setValidator(QIntValidator(0, 9, self))
            digit_input.setAlignment(Qt.AlignCenter)
            digits_layout.addWidget(digit_input)
            self.digits.append(digit_input)

        self.digits[0].textChanged.connect(self.handle_first_digit_input)

        # OK-Button
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.check_totp)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(digits_layout)
        layout.addWidget(ok_button)
        self.setLayout(layout)

    def handle_first_digit_input(self):
        first_digit_text = self.digits[0].text()
        if len(first_digit_text) == 6 and first_digit_text.isdigit():
            for i, digit in enumerate(first_digit_text):
                self.digits[i].setText(digit)

    def check_totp(self):
        totp_code = "".join([digit.text() for digit in self.digits])
        if len(totp_code) == 6 and totp_code.isdigit():
            self.totp_value = totp_code
            self.accept()  # Akzeptiert den Dialog (schließt das Fenster)
        else:
            QMessageBox.warning(self, "Fehler", "Bitte einen gültigen 6-stelligen Code eingeben!")

    def get_totp(self):
        return self.totp_value

# Klasse, die den TOTP-Dialog aufruft
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Hauptfenster")

        button = QPushButton("TOTP eingeben", self)
        button.clicked.connect(self.open_totp_popup)

        layout = QVBoxLayout()
        layout.addWidget(button)
        self.setLayout(layout)

    def open_totp_popup(self):
        totp_dialog = TotpPopup()  # Erstelle den Dialog

        # Warte auf die Benutzerinteraktion
        if totp_dialog.exec() == QDialog.Accepted:
            totp_code = totp_dialog.get_totp()
            if totp_code:
                print(f"Eingegebener TOTP-Code: {totp_code}")
                # Hier kannst du den TOTP-Code weiter verarbeiten
            else:
                print("Kein TOTP-Code eingegeben.")
        else:
            print("Dialog wurde abgebrochen.")

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
