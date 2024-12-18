import pickle
import os
import sys
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
)
from socket import gethostname
from totp import TotpPopup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

# from show_ui import MyMainWindow

from amazon_parser import scrape_order_deep

from classes import *
from constants import *
from crypto_functions import encrypt_data, decrypt_data

import datetime


class AmazonLogin:
    def __init__(
        self, username, password, cookie_pth, cookies=None, main_window=None
    ) -> None:
        self.username = username
        self.password = password
        self.cookie_pth = cookie_pth
        self.cookies = cookies
        self.main_window = main_window

        self.driver = webdriver.Chrome(options=self.set_chrome_options())
        self.wait = WebDriverWait(self.driver, short_wait)
        self.long_wait = WebDriverWait(self.driver, sel_timeout)
        self.end_year = self._set_current_year()
        # self._load_cookies()

        # Cookie handling moved to the gui interface completely

    #     # Automatisch die Hostname als Device ID verwenden
    #     self.device_id = gethostname()
    #     self.cookie_file = f"{username}_{self.device_id}.pkl"

    # def _load_cookie_file(self):
    #     if os.path.exists(self.cookie_file):
    #         self.load_cookies(cookies)
    #         return True
    #     else:
    #         return False

    def _set_current_year(self):
        # Aktuelles Datum und Uhrzeit abrufen
        now = datetime.datetime.now()
        # Aktuelles Jahr extrahieren
        return now.year

    def _load_cookies_from_file(self):
        """
        Unused function in
        """
        if os.path.exists(self.cookie_pth):
            with open(self.cookie_pth, "rb") as f:
                enc_cookies = pickle.load(f)

            self.cookies = decrypt_data(
                encrypted_data=enc_cookies, password=self.password
            )
            self.load_cookies()

    def create_driver_running(self, totp=None):
        """
        Create a webdriver for selenium and keep it running.
        Technically deprecated as it was only used to scrape with active browser.
        Using a system of scraping all the contents with a get request.
        It returns a WebDriver object and the user agent
        """
        # Amazon-Website-URL
        page = (
            f"https://www.amazon.de/your-orders/orders?timeFilter=year-{self.end_year}"
        )

        if self.cookies:
            self.driver.get(page)
            try:
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "your-orders-content-container")
                    )
                )

            except:
                try:
                    self.wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
                    self.login_procedure()
                except TimeoutException:
                    print("Attempt with just a password")
                    try:
                        self.login_procedure_pw()
                    except TimeoutException:
                        raise PermissionError(
                            "Couldn't login either with password and mail nor else"
                        )

        else:
            self.driver.get(page)
            try:
                self.login_procedure()
            except TimeoutException:
                raise PermissionError("Couldn't login initially")

        user_agent = self.driver.execute_script("return navigator.userAgent;")
        self.save_cookies()
        return self.driver, user_agent

    def create_driver(self, totp=None):
        """
        Create a webdriver for selenium and save the cookies.
        After the webdriver is closed again.
        """

        # Amazon-Website-URL
        page = (
            f"https://www.amazon.de/your-orders/orders?timeFilter=year-{self.end_year}"
        )

        if self.cookies:
            self.load_cookies()
            self.driver.get(page)
            try:
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.CLASS_NAME, "your-orders-content-container")
                    )
                )

            except:
                try:
                    self.wait.until(EC.presence_of_element_located((By.ID, "ap_email")))
                    self.login_procedure(totp)
                except TimeoutException:
                    # Under the assumption that no email needs to be entered this method to just enter the password is valid
                    try:
                        self.login_procedure_pw()
                    except TimeoutException:
                        raise PermissionError(
                            "Couldn't login either with password and mail nor else"
                        )

        else:
            self.driver.get(page)
            try:
                self.login_procedure()
            except TimeoutException:
                raise PermissionError("Couldn't login initially")

        user_agent = self.driver.execute_script("return navigator.userAgent;")

        self.save_cookies()
        self.driver.quit()

        return user_agent

    def save_cookies(self):
        # Hole die Cookies vom WebDriver
        cookies = self.driver.get_cookies()

        enc_cookies = encrypt_data(cookies, self.password)
        # Speichere die Cookies in einer Datei
        with open(self.cookie_pth, "wb") as file:
            pickle.dump(enc_cookies, file)

    def load_cookies(self):
        self.driver.execute_cdp_cmd("Network.enable", {})

        # Iterate through pickle dict and add all the cookies
        for cookie in self.cookies:
            # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
            if "expiry" in cookie:
                cookie["expires"] = cookie["expiry"]
                del cookie["expiry"]

            # Replace domain 'apple.com' with 'microsoft.com' cookies
            # cookie["domain"] = cookie["domain"].replace("apple.com", "microsoft.com")

            # Set the actual cookie
            self.driver.execute_cdp_cmd("Network.setCookie", cookie)

        # Disable network tracking
        self.driver.execute_cdp_cmd("Network.disable", {})

    def login_procedure(self, totp=None):
        self._enter_username()
        self._enter_password()
        self._enter_totp()

    def login_procedure_pw(self, totp=None):
        """
        Login procedure where only a password is required for login.
        This happens if the tick was set for remember me.
        """
        self._enter_password()

    def _enter_username(self):
        """
        Function to obtain the username and enter the credentials accordingly.
        """
        username_textbox = self.long_wait.until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        username_textbox.send_keys(self.username)

        submit_mail = self.long_wait.until(
            EC.presence_of_element_located((By.ID, "continue"))
        )
        submit_mail.click()

        try:
            self.wait.until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, "a-list-item"),
                    "Es konnte kein Konto mit dieser E-Mail-Adresse gefunden werden.",
                )
            )
            raise InvalidEmailError("Kein Konto mit dieser E-Mail-Adresse.")
        except TimeoutException:
            pass

    def _enter_password(self):
        """
        Function to enter a password and enter the password accordingly.
        """
        password_textbox = self.long_wait.until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_textbox.send_keys(self.password)

        # Remember checkbox seems to be disappeared from the UI
        # remember_checkbox = self.wait.until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, '//input[@type="checkbox" and @name="rememberMe"]')
        #     )
        # )
        # remember_checkbox.click()

        SignIn_button = self.long_wait.until(
            EC.presence_of_element_located((By.ID, "signInSubmit"))
        )
        SignIn_button.click()

        try:
            self.wait.until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, "a-list-item"),
                    "Falsches Passwort",
                )
            )
            raise InvalidPasswordError("Falsches Passwort!")
        except TimeoutException:
            pass

    def _enter_totp(self):
        try:
            totp_textbox = self.long_wait.until(
                EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
            )
            totp = self.get_totp_value()
            totp_textbox.send_keys(totp)
        except TimeoutException:
            # Checking if there is a totp field
            # If there is no totp field we can proceed with storing the cookies
            pass

        # Warte darauf, dass das Element anklickbar ist
        totp_store_checkbox = self.long_wait.until(
            EC.element_to_be_clickable((By.ID, "auth-mfa-remember-device"))
        )
        # Klicke auf das Element
        totp_store_checkbox.click()

        auth_button = self.long_wait.until(
            EC.presence_of_element_located((By.ID, "auth-signin-button"))
        )
        auth_button.click()

        try:
            self.wait.until(
                EC.text_to_be_present_in_element(
                    (By.CLASS_NAME, "a-list-item"),
                    "Der eingegebene Code ist ungültig. Bitte erneut versuchen.",
                )
            )
            raise InvalidTotpError("Ungültiger ToTp oder 2FA Code")
        except TimeoutException:
            pass

        # else:
        #     try:
        #         self.wait.until(
        #             EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
        #         )
        #         raise MissingTotpError("Bitte geben sie den Zweiten Faktor an!")
        #     except TimeoutException:
        #         pass

    def get_totp_value(self):
        """
        Function to open a popup window in the main QT GUI for entering the TOTP code.
        """
        return self.main_window.open_totp_popup()

    def set_chrome_options(self) -> Options:
        """
        Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        """
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-popup-blocking")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-webauthn")
        chrome_options.add_argument("--disable-features=PasswordAutofillPublicAPI")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        # chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options
