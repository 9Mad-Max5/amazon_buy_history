import pickle
import os
import sys
from pyppeteer import launch
from PySide6.QtWidgets import QApplication, QDialog
from socket import gethostname
from totp import TotpPopup
from amazon_parser import scrape_order_deep
from classes import *
from constants import *
from crypto_functions import encrypt_data
import datetime
import asyncio

class AmazonLogin:
    def __init__(self, username, password, cookie_pth, cookies=None, main_window=None) -> None:
        self.username = username
        self.password = password
        self.cookie_pth = cookie_pth
        self.cookies = cookies
        self.main_window = main_window

        self.browser = None
        self.page = None
        self.end_year = self._set_current_year()

    def _set_current_year(self):
        now = datetime.datetime.now()
        return now.year

    async def create_browser(self):
        """
        Launches the Puppeteer browser.
        """
        self.browser = await launch(headless=False, args=['--no-sandbox', '--disable-dev-shm-usage', '--window-size=1920,1080'])
        self.page = await self.browser.newPage()

    async def create_driver(self, totp=None):
        """
        Create a browser instance using Puppeteer and save cookies.
        """
        page_url = f"https://www.amazon.de/your-orders/orders?timeFilter=year-{self.end_year}"
        await self.page.goto(page_url)

        if self.cookies:
            await self.load_cookies(self.cookies)
            await self.page.reload()
            try:
                await self.page.waitForSelector('.your-orders-content-container', timeout=5000)
            except:
                await self.login_procedure(totp)
        else:
            await self.login_procedure(totp)

        user_agent = await self.page.evaluate('navigator.userAgent')
        await self.save_cookies()
        await self.browser.close()
        return user_agent

    async def save_cookies(self):
        """
        Saves cookies from the current browser session.
        """
        cookies = await self.page.cookies()
        enc_cookies = encrypt_data(cookies, self.password)
        with open(self.cookie_pth, "wb") as file:
            pickle.dump(enc_cookies, file)

    async def load_cookies(self, cookies):
        """
        Loads cookies into the current session.
        """
        await self.page.setCookie(*cookies)

    async def login_procedure(self, totp=None):
        """
        The login process using username, password and possibly 2FA.
        """
        await self.page.waitForSelector('#ap_email')
        await self.page.type('#ap_email', self.username)
        await self.page.click('#continue')

        await self.page.waitForSelector('#ap_password')
        await self.page.type('#ap_password', self.password)

        # Optional: handle "Remember Me" checkbox
        await self.page.click('input[name="rememberMe"]')

        await self.page.click('#signInSubmit')

        # Handle potential 2FA
        try:
            await self.page.waitForSelector('#auth-mfa-otpcode', timeout=5000)
            totp = self.get_totp_value()
            await self.page.type('#auth-mfa-otpcode', totp)
            await self.page.click('#auth-signin-button')
        except:
            pass

        # Check for login errors (invalid email/password)
        try:
            await self.page.waitForSelector('.a-list-item', timeout=5000)
            error_text = await self.page.evaluate('(element) => element.textContent', await self.page.querySelector('.a-list-item'))
            if "kein Konto" in error_text:
                raise InvalidEmailError("Kein Konto mit dieser E-Mail-Adresse.")
            if "Falsches Passwort" in error_text:
                raise InvalidPasswordError("Falsches Passwort!")
        except:
            pass

    def get_totp_value(self):
        """
        Opens the TOTP popup and returns the code.
        """
        return self.main_window.open_totp_popup()
