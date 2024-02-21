from gui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow
from validate_email_address import validate_email
from store_to_file import save_to_excel
from amazon_crawler import create_driver
from amazon_requester import request_amazon
from socket import gethostname
from datetime import datetime

from classes import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidTotpError,
    MissingTotpError,
)
import pickle

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.credentials = {}
        self.start_year = None
        self.product_classes = []
        self.driver = None
        self.local = None
        self.user_agent = None
        self.base_domain = "https://www.amazon.de"
        self.cookies = None
        self.end_year = self.get_actual_year()


        # Initialisiere die Benutzeroberfläche aus der generierten Klasse
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.clear_all()

        # Dropdown-Menü erstellen
        self.ui.cb_local.addItems(["de", "en", "es", "fr"])
        self.ui.cb_local.currentIndexChanged.connect(self.on_language_change)
        self.local = self.ui.cb_local.currentText()

        # Verbinde einen Button mit einer Funktion
        self.ui.b_login.clicked.connect(self.get_login_infos)
        self.ui.b_logout.clicked.connect(self.logout)
        self.ui.b_start.clicked.connect(self.start_crawling)

    # Button functions
    def get_login_infos(self):
        self.clear_error_label()

        if validate_email(self.ui.le_email.text()):
            self.credentials["mail"] = self.ui.le_email.text()
        else:
            self.ui.l_email_error.setText(
                "Ungültige eingabe! Keine valide Mailadresse!"
            )
            return

        if len(self.ui.le_password.text()) > 0:
            self.credentials["pw"] = self.ui.le_password.text()

        if self.ui.le_totp.text():
            if self.is_valid_totp(self.ui.le_totp.text()):
                totp = self.ui.le_totp.text()
            else:
                self.ui.l_totp_error.setText("Kein gültiger wert für TOTP oder 2FA")
                totp = None
        else:
            totp = None

        self.credentials["totp"] = totp

        if "mail" in self.credentials and "pw" in self.credentials:
            try:
                self.user_agent = create_driver(
                    username=self.credentials["mail"],
                    password=self.credentials["pw"],
                    totp=self.credentials["totp"],
                )
                self.change_view(1)
                self.load_cookies_to_var()
            except InvalidEmailError as e:
                self.ui.l_email_error.setText(str(e))
            except InvalidPasswordError as e:
                self.ui.l_pw_error.setText(str(e))
            except InvalidTotpError as e:
                self.ui.l_totp_error.setText(str(e))
            except MissingTotpError as e:
                self.ui.l_totp_error.setText(str(e))

    def logout(self):
        self.change_view(0)

    def start_crawling(self):
        start_date = self.ui.start_date.date()
        self.start_year = start_date.year()
        # self.product_classes = start_crawling(driver=self.driver, start=self.start_year, outbox=self.ui.bro_text,lang=self.local)
        for year in range(self.start_year, self.end_year+1):
            self.ui.bro_text.append(f"Starte mit laden von Jahr {year}")
            self.product_classes.extend(request_amazon(base_domain=self.base_domain, year=year, user_agent=self.user_agent, cookies=self.cookies))
        save_to_excel(product_list=self.product_classes, excel_file="amazon_shopping_history.xlsx")

    def load_cookies_to_var(self):
        device_id = gethostname()  # Automatisch die Hostname als Device ID verwenden
        cookie_filename = f"{device_id}_{self.credentials["mail"]}_cookies.pkl"

        with open(cookie_filename, 'rb') as f:
            self.cookies = pickle.load(f)

    def get_actual_year(self):
        now = datetime.now()
        # Aktuelles Jahr extrahieren
        return now.year

    # GUI Managment
    def change_view(self, idx):
        self.clear_all()
        self.ui.stackedWidget.setCurrentIndex(idx)

    def is_valid_totp(self, value):
        # Überprüfe, ob der Wert eine Zeichenkette ist
        if not isinstance(value, str):
            return False

        # Überprüfe, ob die Zeichenkette nur aus Ziffern besteht
        if not value.isdigit():
            return False

        # Überprüfe, ob die Zeichenkette genau sechs Ziffern enthält
        if len(value) == 6:
            return True

        return False

    def clear_all(self):
        self.ui.le_email.clear()
        self.ui.le_password.clear()
        self.ui.le_totp.clear()
        self.ui.l_totp_error.setText("")
        self.ui.l_email_error.setText("")
        self.ui.bro_text.setText("")
        self.ui.ba_progress.setValue(0)
        # self.ui.le_ca_pass2.clear()
        # self.ui.le_ca_rsa1.clear()
        # self.ui.le_ca_rsa2.clear()
        # self.ui.file_tree.clear()
        # self.ui.tree_user.clear()
        # self.ui.l_login_info.clear()
        # self.ui.le_login.clear()
        # self.ui.le_password.clear()
        # self.ui.pte_info.clear()
        # self.ui.tree_info.clear()

    def clear_error_label(self):
        self.ui.l_totp_error.setText("")
        self.ui.l_email_error.setText("")

    def on_language_change(self):
        self.local = self.ui.cb_local.currentText()

if __name__ == "__main__":
    import os
    import sys
    os.makedirs("img", exist_ok=True)

    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    main_window.show()
    sys.exit(app.exec())
