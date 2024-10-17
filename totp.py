# 277744
import sys
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


class TotpPopup(QDialog):  # Verwende QDialog statt QWidget
    def __init__(self):
        super().__init__()
        self.totp_value = None  # Initialisiere den TOTP-Wert
        self.initUI()

    def initUI(self):
        # Fenster-Layout und Titel setzen
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
                digit_input.setMaxLength(1)  # Nur eine Ziffer pro Feld
                digit_input.setValidator(QIntValidator(0, 9, self))

            digit_input.setAlignment(Qt.AlignCenter)
            digits_layout.addWidget(digit_input)
            self.digits.append(digit_input)

        # Verbinde das erste Eingabefeld mit der Methode, die die restlichen Felder automatisch füllt
        self.digits[0].textChanged.connect(self.handle_first_digit_input)

        # OK-Button
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.check_totp)

        # Layout einrichten
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addLayout(digits_layout)
        layout.addWidget(ok_button)

        self.setLayout(layout)

    def handle_first_digit_input(self):
        """
        Überprüft, ob das erste Eingabefeld 6 Zeichen enthält, und teilt den TOTP-Code auf die restlichen Felder auf.
        """
        first_digit_text = self.digits[0].text()

        # Wenn im ersten Feld ein 6-stelliger Code eingegeben wird
        if len(first_digit_text) == 6 and first_digit_text.isdigit():
            # Teile den 6-stelligen Code auf die Felder auf
            for i, digit in enumerate(first_digit_text):
                self.digits[i].setText(digit)

    def check_totp(self):
        """
        Überprüft, ob alle Felder korrekt ausgefüllt sind und schließt den Dialog,
        wenn die Eingabe gültig ist.
        """
        totp_code = "".join([digit.text() for digit in self.digits])

        if len(totp_code) == 6 and totp_code.isdigit():
            self.totp_value = totp_code  # Setze den eingegebenen TOTP-Code
            self.accept()  # Schließt das Dialogfenster und akzeptiert die Eingabe
        else:
            QMessageBox.warning(
                self, "Fehler", "Bitte einen gültigen 6-stelligen Code eingeben!"
            )

    def get_totp(self):
        """
        Gibt den eingegebenen TOTP-Code zurück.
        """
        return self.totp_value

# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     # Hauptprogramm-Logik: Öffne das TOTP-Fenster und warte auf den Rückgabewert
#     window = TotpPopup()

#     if window.exec() == QDialog.Accepted:  # Warte, bis der Benutzer den Dialog schließt
#         totp_code = window.get_totp()  # Hol den eingegebenen TOTP-Code
#         if totp_code:
#             print(f"Eingegebener TOTP-Code: {totp_code}")

#     sys.exit(app.exec())


# class TotpPopup(QDialog):
#     def __init__(self):
#         super().__init__()
#         self.totp_value = None  # Initialisiere den TOTP-Wert
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("TOTP-Abfrage")
#         self.setFixedSize(400, 200)

#         # Label für die Beschreibung
#         label = QLabel("Bitte 6-stelligen TOTP eingeben:", self)
#         label.setAlignment(Qt.AlignCenter)
#         label.setFont(QFont("Arial", 12))

#         # Erstellen von 6 Eingabefeldern für die TOTP-Ziffern
#         self.digits = []
#         digits_layout = QHBoxLayout()

#         for i in range(6):
#             digit_input = QLineEdit(self)
#             if i == 0:
#                 digit_input.setMaxLength(6)
#                 digit_input.setValidator(QIntValidator(0, 999999, self))
#             else:
#                 digit_input.setMaxLength(1)
#                 digit_input.setValidator(QIntValidator(0, 9, self))
#             digit_input.setAlignment(Qt.AlignCenter)
#             digits_layout.addWidget(digit_input)
#             self.digits.append(digit_input)

#         self.digits[0].textChanged.connect(self.handle_first_digit_input)

#         # OK-Button
#         ok_button = QPushButton("OK", self)
#         ok_button.clicked.connect(self.check_totp)

#         layout = QVBoxLayout()
#         layout.addWidget(label)
#         layout.addLayout(digits_layout)
#         layout.addWidget(ok_button)
#         self.setLayout(layout)

#     def handle_first_digit_input(self):
#         first_digit_text = self.digits[0].text()
#         if len(first_digit_text) == 6 and first_digit_text.isdigit():
#             for i, digit in enumerate(first_digit_text):
#                 self.digits[i].setText(digit)

#     def check_totp(self):
#         totp_code = "".join([digit.text() for digit in self.digits])
#         if len(totp_code) == 6 and totp_code.isdigit():
#             self.totp_value = totp_code
#             self.accept()  # Akzeptiert den Dialog (schließt das Fenster)
#         else:
#             QMessageBox.warning(self, "Fehler", "Bitte einen gültigen 6-stelligen Code eingeben!")

#     def get_totp(self):
#         return self.totp_value