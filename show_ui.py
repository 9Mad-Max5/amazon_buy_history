from gui_ui import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PySide6.QtCore import QObject, QThread, Signal, Slot, QEvent

from validate_email_address import validate_email
from store_to_file import save_to_excel
from amazon_crawler import create_driver
from amazon_requester import request_amazon
from socket import gethostname
from datetime import datetime

from crypto_functions import decrypt_data 

from settings_handler import *
from version import version
from logger_config import setup_logging

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
        self.username = None
        self.start_year = None
        self.product_classes = []
        self.driver = None
        self.local = None
        self.user_agent = None
        self.base_domain = "https://www.amazon.de"
        self.cookies = None
        self.end_year = self.get_actual_year()
        self.cookie_filename = None
        self.path=load_settings()
        self.file = None
        self.logger = setup_logging()

        create_folders(self.path)
        # Create worker thread
        self.worker_thread = None
        self.worker = None

        # Initialisiere die Benutzeroberfläche aus der generierten Klasse
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.stackedWidget.setCurrentIndex(0)
        self.clear_all()

        # Dropdown-Menü erstellen
        self.ui.cb_local.addItems(["de", "en", "es", "fr"])
        self.ui.cb_local.currentIndexChanged.connect(self.on_language_change)
        self.local = self.ui.cb_local.currentText()
        self.ui.le_path.setText(self.path)
        self.ui.l_ver_n.setText(version)

        # Verbinde einen Button mit einer Funktion
        self.ui.b_login.clicked.connect(self.get_login_infos)
        self.ui.b_logout.clicked.connect(self.logout)
        self.ui.b_start.clicked.connect(self.start_crawling)
        self.ui.b_set_path.clicked.connect(self.set_path)

    # Button functions
    def get_login_infos(self):
        self.clear_error_label()

        if validate_email(self.ui.le_email.text()):
            self.credentials["mail"] = self.ui.le_email.text()
            self.username = self.credentials["mail"].split("@")[0]
            self.file = os.path.join(self.path, f"amazon_shopping_history_{self.username}.xlsx")
        else:
            self.ui.l_email_error.setText(
                "Ungültige eingabe! Keine valide Mailadresse!"
            )
            return
        
        self.set_cookie_filename()
        
        if len(self.ui.le_password.text()) > 0:
            self.credentials["pw"] = self.ui.le_password.text()

        self.load_cookies_to_var()

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
                    cookie_filename=self.cookie_filename,
                    cookies=self.cookies,
                    totp=self.credentials["totp"],
                )
                self.change_view(1)
                self.load_cookies_to_var()
                self.logger.debug(f"Erfolgreich angemeldet")

            except InvalidEmailError as e:
                self.ui.l_email_error.setText(str(e))
            except InvalidPasswordError as e:
                self.ui.l_pw_error.setText(str(e))
            except InvalidTotpError as e:
                self.ui.l_totp_error.setText(str(e))
            except MissingTotpError as e:
                self.ui.l_totp_error.setText(str(e))

    def logout(self):
        self.credentials = {}
        self.change_view(0)

    def set_path(self):
        path = QFileDialog.getExistingDirectory(self, "Ordner auswählen")
        if path:
            self.path = path
            self.ui.le_path.setText(self.path)
            update_settings(self.path)
            self.file = os.path.join(self.path, f"amazon_shopping_history_{self.username}.xlsx")

    def start_crawling(self):
        
        self.ui.b_start.setEnabled(False)
        start_date = self.ui.start_date.date()
        self.start_year = start_date.year()
        
        self.worker_thread = QThread()
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)
        self.worker = RequestWorker(start_year=self.start_year , end_year=self.end_year,
                                     base_domain=self.base_domain, user_agent=self.user_agent,
                                       cookies=self.cookies, path=self.path, file=self.file)
        self.worker.moveToThread(self.worker_thread)
        self.worker.finished.connect(self.worker_finished)
        self.worker.progress_updated.connect(self.update_progress)
        self.worker.info.connect(self.info)
        self.worker_thread.started.connect(self.worker.run)
        self.worker_thread.start()

    def load_cookies_to_var(self):
        if os.path.exists(self.cookie_filename):
            with open(self.cookie_filename, 'rb') as f:
                enc_cookies = pickle.load(f)

            self.cookies = decrypt_data(encrypted_data=enc_cookies,password=self.credentials["pw"])

    def set_cookie_filename(self):
        device_id = gethostname()
        self.cookie_filename = f"{device_id}_{self.credentials["mail"]}.pkl"

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

    def event(self, event):
        # if event.type() == QEvent.Close:
        #     if self.worker_thread.isRunning():
        #         self.worker_thread.quit()
        #         self.worker_thread.wait()
        return super().event(event)
    
    def clear_error_label(self):
        self.ui.l_totp_error.setText("")
        self.ui.l_email_error.setText("")

    def on_language_change(self):
        self.local = self.ui.cb_local.currentText()

    def update_progress(self, progress, item_name):
        # Hier aktualisieren Sie die Anzeige des Fortschritts und des aktuellen Elementnamens
        self.ui.b_start.setEnabled(False)
        self.ui.ba_progress.setValue(progress)
        self.ui.bro_text.append(f"Abgeschlossen mit dem laden von Jahr {item_name}")

    def info(self, item_name):
        self.ui.bro_text.append(item_name)

    def worker_finished(self):
        # Aktiviere den Start-Button, wenn der Worker-Prozess beendet ist
        self.ui.b_start.setEnabled(True)
        self.worker_thread.quit()

class RequestWorker(QObject):
    info = Signal(str)
    progress_updated = Signal(int, int)
    finished = Signal()

    def __init__(self, start_year, end_year, base_domain, user_agent, cookies, path, file):
        super().__init__()
        self.product_classes = []
        self.start_year = start_year
        self.end_year = end_year
        self.base_domain = base_domain
        self.user_agent = user_agent
        self.cookies = cookies
        self.file = file
        self.path = path
        self.logger = setup_logging()


    @Slot()
    def run(self):
        years_list = list(range(self.start_year, self.end_year + 1))
        total_items = len(years_list)

        for i, year in enumerate(years_list):
            msg = f"Starte mit laden von Jahr {year}"
            self.info.emit(msg)
            self.logger.info(msg)
            # Verarbeitung des Elements
            try:
                self.product_classes.extend(request_amazon(base_domain=self.base_domain, year=year, user_agent=self.user_agent, cookies=self.cookies, path=self.path))
            except ConnectionResetError:
                msg = f"Verbindung unterbrochen beim Start von Jahr {year}"
                self.info.emit(msg)
                self.logger.error(msg)
                continue

            except ConnectionError:
                msg = f"Verbindung unterbrochen beim Start von Jahr {year}"
                self.info.emit(msg)
                self.logger.error(msg)
                continue

            # Fortschritt aktualisieren und aktuellen Elementnamen übermitteln
            progress = int((i + 1) / total_items * 100)
            self.progress_updated.emit(progress, year)
            self.logger.info(f"Abgeschlossen mit dem laden von Jahr {year}")

        self.logger.info(f"Starte mit speischern in Excel")
        save_to_excel(product_list=self.product_classes, excel_file=self.file)
        self.finished.emit()


if __name__ == "__main__":
    import os
    import sys
    os.makedirs("img", exist_ok=True)
    logger = setup_logging()

    app = QApplication(sys.argv)
    main_window = MyMainWindow()
    logger.debug("Main window created")
    main_window.show()
    sys.exit(app.exec())
