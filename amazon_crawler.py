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
# from credentials import password


def create_driver_running(username, password, totp=None):
    # Aktuelles Datum und Uhrzeit abrufen
    now = datetime.datetime.now()
    # Aktuelles Jahr extrahieren
    end = now.year

    # Amazon-Website-URL
    page = f"https://www.amazon.de/your-orders/orders?timeFilter=year-{end}"

    device_id = gethostname()  # Automatisch die Hostname als Device ID verwenden
    cookie_filename = f"{username}_{device_id}.pkl"

    driver = webdriver.Chrome(options=set_chrome_options())

    if os.path.exists(cookie_filename):
        load_cookies(driver, cookie_filename)
        driver.get(page)
        try:
            WebDriverWait(driver, short_wait).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "your-orders-content-container")
                )
            )

        except:
            try:
                WebDriverWait(driver, short_wait).until(
                    EC.presence_of_element_located((By.ID, "ap_email"))
                )
                login_procedure(driver, username, password, sel_timeout, totp)
            except TimeoutException:
                login_procedure_pw(driver, password, sel_timeout, totp)

    else:
        driver.get(page)
        login_procedure(driver, username, password, sel_timeout, totp)

    # # Abrufen der Netzwerkinformationen
    # network_entries = driver.execute_cdp_cmd(
    #     "Network.getResponseBodyForInterception", {"interceptionId": 1}
    # )

    # # Die Netzwerkeinträge enthalten die Headers
    # headers = network_entries["headers"]
    # print("Headers:", headers)
    user_agent = driver.execute_script("return navigator.userAgent;")

    save_cookies(driver, cookie_filename)

    return driver, user_agent


def create_driver(username, password, cookie_filename, cookies=None, totp=None):
    # Aktuelles Datum und Uhrzeit abrufen
    now = datetime.datetime.now()
    # Aktuelles Jahr extrahieren
    end = now.year

    # Amazon-Website-URL
    page = f"https://www.amazon.de/your-orders/orders?timeFilter=year-{end}"

    driver = webdriver.Chrome(options=set_chrome_options())

    if os.path.exists(cookie_filename):
        load_cookies(driver, cookies)
        driver.get(page)
        try:
            WebDriverWait(driver, short_wait).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "your-orders-content-container")
                )
            )

        except:
            try:
                WebDriverWait(driver, short_wait).until(
                    EC.presence_of_element_located((By.ID, "ap_email"))
                )
                login_procedure(driver, username, password, sel_timeout, totp)
            except TimeoutException:
                login_procedure_pw(driver, password, sel_timeout, totp)

    else:
        driver.get(page)
        login_procedure(driver, username, password, sel_timeout, totp)

    # # Abrufen der Netzwerkinformationen
    # network_entries = driver.execute_cdp_cmd(
    #     "Network.getResponseBodyForInterception", {"interceptionId": 1}
    # )

    # # Die Netzwerkeinträge enthalten die Headers
    # headers = network_entries["headers"]
    # print("Headers:", headers)
    user_agent = driver.execute_script("return navigator.userAgent;")

    save_cookies(driver, cookie_filename, password)
    driver.quit()

    return user_agent


def start_crawling(driver, start, outbox, lang="de"):
    c_products = []

    now = datetime.datetime.now()
    # Aktuelles Jahr extrahieren
    end = now.year

    jahresliste = [x for x in range(start, end + 1)]
    for jahr in jahresliste:
        # Amazon-Website-URL
        outbox.append(f"Starte mit laden von Jahr {jahr}")
        page = f"https://www.amazon.de/your-orders/orders?timeFilter=year-{jahr}"
        # Liste der Produkte

        driver.get(page)
        result = scrape_order_deep(driver=driver, lang=lang)
        if result is not None:
            c_products.extend(result)
        # c_products.extend(crawl_amazon(driver, lang))

    # Schließe den WebDriver am Ende
    driver.quit()

    return c_products


def crawl_amazon(driver, lang):
    c_products = []
    loop = True

    while loop:
        c_products.extend(scrape_order_deep(driver=driver, lang=lang))
        try:
            # Versuche den "Weiter"-Button zu finden
            next_button = WebDriverWait(driver, short_wait).until(
                EC.presence_of_element_located((By.XPATH, '//li[@class="a-last"]'))
            )
            loop = True
        except:
            loop = False
            pass

        # Klicke auf den "Weiter"-Button, falls er gefunden wurde
        if loop:
            next_button.click()

    return c_products


def save_cookies(driver, filename, password):
    # Hole die Cookies vom WebDriver
    cookies = driver.get_cookies()

    enc_cookies = encrypt_data(cookies, password)
    # Speichere die Cookies in einer Datei
    with open(filename, "wb") as file:
        pickle.dump(enc_cookies, file)


def load_cookies(driver, cookies):
    driver.execute_cdp_cmd("Network.enable", {})

    # Iterate through pickle dict and add all the cookies
    for cookie in cookies:
        # Fix issue Chrome exports 'expiry' key but expects 'expire' on import
        if "expiry" in cookie:
            cookie["expires"] = cookie["expiry"]
            del cookie["expiry"]

        # Replace domain 'apple.com' with 'microsoft.com' cookies
        cookie["domain"] = cookie["domain"].replace("apple.com", "microsoft.com")

        # Set the actual cookie
        driver.execute_cdp_cmd("Network.setCookie", cookie)

    # Disable network tracking
    driver.execute_cdp_cmd("Network.disable", {})


def login_procedure(driver, username, password, sel_timeout, totp=None):
    try:
        username_textbox = WebDriverWait(driver, sel_timeout).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        username_textbox.send_keys(username)
    except TimeoutException:
        pass

    try:
        password_textbox = WebDriverWait(driver, sel_timeout).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_textbox.send_keys(password)
    except TimeoutException:
        pass

    remember_checkbox = WebDriverWait(driver, short_wait).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@type="checkbox" and @name="rememberMe"]')
        )
    )
    remember_checkbox.click()

    SignIn_button = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "signInSubmit"))
    )
    SignIn_button.click()

    try:
        WebDriverWait(driver, short_wait).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "a-list-item"),
                "Es konnte kein Konto mit dieser E-Mail-Adresse gefunden werden.",
            )
        )
        raise InvalidEmailError("Kein Konto mit dieser E-Mail-Adresse.")
    except TimeoutException:
        pass

    try:
        WebDriverWait(driver, short_wait).until(
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
            totp_textbox = WebDriverWait(driver, sel_timeout).until(
                EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
            )
            totp_textbox.send_keys(totp)
        except TimeoutException:
            pass

        # Warte darauf, dass das Element anklickbar ist
        totp_store_checkbox = WebDriverWait(driver, sel_timeout).until(
            EC.element_to_be_clickable((By.ID, "auth-mfa-remember-device"))
        )
        # Klicke auf das Element
        totp_store_checkbox.click()

        auth_button = WebDriverWait(driver, sel_timeout).until(
            EC.presence_of_element_located((By.ID, "auth-signin-button"))
        )
        auth_button.click()

        try:
            WebDriverWait(driver, short_wait).until(
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
            WebDriverWait(driver, short_wait).until(
                EC.presence_of_element_located((By.ID, "auth-mfa-otpcode"))
            )
            raise MissingTotpError("Bitte geben sie den Zweiten Faktor an!")
        except TimeoutException:
            pass


def login_procedure_pw(driver, password, sel_timeout, totp=None):
    try:
        password_textbox = WebDriverWait(driver, sel_timeout).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_textbox.send_keys(password)
    except TimeoutException:
        pass

    remember_checkbox = WebDriverWait(driver, short_wait).until(
        EC.presence_of_element_located(
            (By.XPATH, '//input[@type="checkbox" and @name="rememberMe"]')
        )
    )
    remember_checkbox.click()

    SignIn_button = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.ID, "signInSubmit"))
    )
    SignIn_button.click()

    try:
        WebDriverWait(driver, short_wait).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, "a-list-item"),
                "Falsches Passwort",
            )
        )
        raise InvalidPasswordError("Falsches Passwort!")
    except TimeoutException:
        pass


def set_chrome_options() -> Options:
    """Sets chrome options for Selenium.
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
