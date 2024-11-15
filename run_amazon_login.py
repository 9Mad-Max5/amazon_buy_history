import os
import pickle


from amazon_login import AmazonLogin
from credentials import *
from crypto_functions import decrypt_data


def load_cookies_to_var(cookie_filename):
    if os.path.exists(cookie_filename):
        with open(cookie_filename, "rb") as f:
            enc_cookies = pickle.load(f)

        return decrypt_data(encrypted_data=enc_cookies, password=password)


cookie_filename = "Maximilian-RTX_maximilian.huebner95@gmx.de.pkl"
cookies = load_cookies_to_var(cookie_filename)
login = AmazonLogin(
    username=username,
    password=password,
    cookie_pth=cookie_filename,
    cookies=cookies,
    # main_window=self
)
login.create_driver()