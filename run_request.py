from amazon_requester import request_amazon
from crypto_functions import decrypt_data
from credentials import *
import pickle

base_domain = "https://www.amazon.de"
year = 2024
product_classes = []
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'

with open("Maximilian-RTX_maximilian.huebner95@gmx.de.pkl", "rb") as f:
    enc_cookies = pickle.load(f)
cookies= decrypt_data(
                encrypted_data=enc_cookies, password=password
            )
path="C:/Users/maxim/Documents/amazon_buy_history"

# try:
product_classes.extend(
    request_amazon(
        base_domain=base_domain,
        year=year,
        user_agent=user_agent,
        cookies=cookies,
        path=path,
    )
)
# except ConnectionResetError:
#     msg = f"Verbindung unterbrochen beim Start von Jahr {year}"
#     print(msg)
#     continue

# except requests.exceptions.ConnectionError:
#     msg = f"Verbindung unterbrochen beim Start von Jahr {year}"
#     print(msg)
#     continue