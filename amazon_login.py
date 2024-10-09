import pickle
import os

from socket import gethostname

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


from amazon_parser import scrape_order_deep

from classes import *
from constants import *
from crypto_functions import encrypt_data

import datetime


class AmazonCredentials:
    def __init__(self, username, password, cookie_pth, cookies=None) -> None:
        self.username = username
        self.password = password
        self.cookie_pth = cookie_pth
        self.cookies = cookies

        self.driver = webdriver.Chrome(options=self.set_chrome_options())
        self.wait = WebDriverWait(self.driver, short_wait)
        self.long_wait = WebDriverWait(self.driver, sel_timeout)
        self.end_year = self._set_current_year()

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
                    self.login_procedure(totp)
                except TimeoutException:
                    self.login_procedure_pw(totp)

        else:
            self.driver.get(page)
            self.login_procedure(totp)

        user_agent = self.driver.execute_script("return navigator.userAgent;")
        self.save_cookies()
        return self.driver, user_agent

    def create_driver(self, cookies=None, totp=None):
        """
        Create a webdriver for selenium and save the cookies.
        After the webdriver is closed again.
        """

        # Amazon-Website-URL
        page = (
            f"https://www.amazon.de/your-orders/orders?timeFilter=year-{self.end_year}"
        )

        if self.cookies:
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
                    self.login_procedure_pw()

        else:
            self.driver.get(page)
            self.login_procedure()

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

    def load_cookies(self, cookies):
        self.driver.execute_cdp_cmd("Network.enable", {})

        # Iterate through pickle dict and add all the cookies
        for cookie in cookies:
            # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
            if "expiry" in cookie:
                cookie["expires"] = cookie["expiry"]
                del cookie["expiry"]

            # Replace domain 'apple.com' with 'microsoft.com' cookies
            cookie["domain"] = cookie["domain"].replace("apple.com", "microsoft.com")

            # Set the actual cookie
            self.driver.execute_cdp_cmd("Network.setCookie", cookie)

        # Disable network tracking
        self.driver.execute_cdp_cmd("Network.disable", {})

    def login_procedure(self, totp=None):
        try:
            username_textbox = self.long_wait.until(
                EC.presence_of_element_located((By.ID, "ap_email"))
            )
            username_textbox.send_keys(self.username)
        except TimeoutException:
            pass

        try:
            password_textbox = self.long_wait.until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_textbox.send_keys(self.password)
        except TimeoutException:
            pass

        remember_checkbox = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="checkbox" and @name="rememberMe"]')
            )
        )
        remember_checkbox.click()

        SignIn_button = self.long_wait.until(
            EC.presence_of_element_located((By.ID, "signInSubmit"))
        )
        SignIn_button.click()

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

        if totp:
            try:
                totp_textbox = self.long_wait.until(
                    EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
                )
                totp_textbox.send_keys(totp)
            except TimeoutException:
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

        else:
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
                )
                raise MissingTotpError("Bitte geben sie den Zweiten Faktor an!")
            except TimeoutException:
                pass

    def login_procedure_pw(self, totp=None):
        """
        Login procedure where only a password is required for login.
        This happens if the tick was set for remember me.
        """
        try:
            password_textbox = self.long_wait.until(
                EC.presence_of_element_located((By.ID, "ap_password"))
            )
            password_textbox.send_keys(self.password)
        except TimeoutException:
            pass

        remember_checkbox = self.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="checkbox" and @name="rememberMe"]')
            )
        )
        remember_checkbox.click()

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

    def set_chrome_options(self) -> Options:
        """
        Sets chrome options for Selenium.
        Chrome options for headless browser is enabled.
        """
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        return chrome_options
