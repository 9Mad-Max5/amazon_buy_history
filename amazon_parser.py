from bs4 import BeautifulSoup
import os
import requests
import sys

from socket import gethostname

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


from time import sleep

from classes import *
from constants import *
import locale
from datetime import datetime

def scrape_order(page_source):
    # Verwende BeautifulSoup, um die Daten zu scrapen
    soup = BeautifulSoup(page_source, "html.parser")
    # Finde alle Elemente mit der Klasse 'order-card js-order-card'
    order_elements = soup.find_all("div", class_="order-card")

    if len(order_elements) > 0:
        for order_element in order_elements:
            # # Extrahiere das Datum
            # order_date_element = order_element.find('span', class_='value')
            # order_date = order_date_element.text.strip() if order_date_element else 'N/A'

            # # Extrahiere die Bestellnummer
            # order_number_element = order_element.find('span', class_='value')
            # order_number = order_number_element.text.strip() if order_number_element else 'N/A'
            # Extrahiere Order Date
            order_date_element = order_element.find(
                "span", {"class": "a-color-secondary value"}
            )
            order_date = order_date_element.text.strip()

            # Extrahiere Order Number
            order_number_element = order_element.find(
                "span", {"class": "a-color-secondary value"}
            )
            order_number = order_number_element.text.strip()

            # Hier könntest du die Daten weiter verarbeiten oder ausgeben
            print(f"Order Date: {order_date}, Order Number: {order_number}")


def scrape_order_deep(driver, lang):
    locale.setlocale(locale.LC_TIME, lang)

    c_products = []

    # Scrolle nach unten, um alle Bestellungen zu laden
    body = WebDriverWait(driver, sel_timeout).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    body.send_keys(Keys.END)
    sleep(short_wait)

    details_buttons_xpath = (
        '//div[contains(@class, "a-fixed-right-grid-col") and contains(@class, "actions") and contains(@class, "a-col-right")]'
        '//a[contains(@class, "yohtmlc-order-details-link") and not(starts-with(@href, "/gp/digital/your-account/order-summary.html"))]'
    )
    
    try:
        details_buttons = WebDriverWait(driver, sel_timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, details_buttons_xpath))
        )
    except:
        return

    # for button in details_buttons:
    for idx in range(len(details_buttons)):
        _details_buttons = WebDriverWait(driver, sel_timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, details_buttons_xpath))
        )
        button = _details_buttons[idx]

        button.click()
        order_info = WebDriverWait(driver, sel_timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//div[@class="a-row a-spacing-base"]')
            )
        )

        # Verwende BeautifulSoup, um die HTML-Struktur zu analysieren
        soup = BeautifulSoup(order_info.get_attribute("outerHTML"), "html.parser")
        order_items = soup.find_all("span", {"class": "order-date-invoice-item"})

        # Initialisiere leere Variablen
        order_date = None
        order_number = None

        # Iteriere durch die gefundenen Elemente und extrahiere Daten
        for item in order_items:
            text = item.text.strip()
            if text.startswith(country_specific[lang][0]):
                order_date = text.replace(country_specific[lang][0], "")
                order_date = datetime.strptime(order_date, "%d. %B %Y").strftime("%d.%m.%Y")
            elif text.startswith(country_specific[lang][1]):
                order_number = item.find("bdi").text.strip()

        # Verwende BeautifulSoup, um die HTML-Struktur zu analysieren
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Extrahiere Informationen für jedes Produkt
        products = soup.find_all("div", {"class": "a-fixed-left-grid"})

        for product in products:
            # Bild herunterladen
            image_url = product.find("img")["src"]
            image_filename = f"img/{os.path.basename(image_url)}"
            try:
                response = requests.get(image_url)
                with open(image_filename, "wb") as f:
                    f.write(response.content)
            except:
                print("Kein Bild heruntergeladen.")
                pass

            # Name extrahieren
            product_name = None
            products_name = product.find_all("a", {"class": "a-link-normal"})
            for pro_n in products_name:
                product_name = pro_n.text.strip()
                if not product_name == "":
                    break

            # Preis extrahieren
            product_price = None
            try:
                product_price = product.find(
                    "span", {"class": "a-size-small", "class": "a-color-price"}
                ).text.strip()
                product_price = float(product_price[1:])
            except:
                pass

            delivery_date = None
            shimpent = False
            try:
                shipment_info = WebDriverWait(driver, short_wait).until(
                    EC.visibility_of_element_located(
                        (By.CLASS_NAME, "shipment-top-row")
                    )
                )
                shimpent = True
            except:
                shimpent = False

            if shimpent:
                # Verwende BeautifulSoup, um die HTML-Struktur zu analysieren
                soup = BeautifulSoup(
                    shipment_info.get_attribute("outerHTML"), "html.parser"
                )

                # Extrahiere das "Zugestellt am" Datum
                delivery_date_element = soup.find(
                    "span",
                    {
                        "class": "a-size-medium",
                        "class": "a-color-base",
                        "class": "a-text-bold",
                    },
                )
                delivery_date = delivery_date_element.text.strip().replace(
                    country_specific[lang][2], ""
                )

            if product_price:
                # print(f"Bestelldatum: {order_date} Lieferdatum: {delivery_date} Bestellnummer: {order_number} Produktname: {product_name} Preis: {product_price} Bild heruntergeladen: {image_filename}")
                c_products.append(
                    Product(
                        order_date=order_date,
                        delivery_date=delivery_date,
                        order_number=order_number,
                        product_name=product_name,
                        product_price=product_price,
                        image_filename=image_filename,
                    )
                )
        driver.back()

    return c_products
