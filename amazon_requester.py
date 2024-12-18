import requests
import os

from bs4 import BeautifulSoup
from classes import Product
from time import sleep

from logger_config import setup_logging
import random

import requests


def get_price(soup):
    price_path = [
        "div.a-row > span.a-size-small.a-color-price > nobr",
        "div.a-row > div.a-row.a-spacing-top-mini.gift-card-instance > div.a-column.a-span2",
    ]
    for p_p in price_path:
        product_price_res = soup.select_one(p_p)
        if product_price_res is not None:
            product_price = product_price_res.text.strip()
            return product_price


def get_shipment_stats(soup):
    # shipment information
    delivery_date = None
    shipment_soups = soup.find_all(
        "div", class_="a-row shipment-top-row js-shipment-info-container"
    )
    for shipment_soup in shipment_soups:
        try:
            delivery_date = shipment_soup.select_one(
                "div.a-row > span.a-size-medium.a-color-base.a-text-bold"
            ).text.strip()
        except AttributeError:
            try:
                delivery_date = shipment_soup.select_one(
                    "div.a-row > span.a-text-bold"
                ).text.strip()
            except AttributeError:
                delivery_date = None
                pass
    return delivery_date


def get_order_details(ses, uri, path):
    logger = setup_logging()
    logger.debug(f"Get order details: {uri}")
    order_date = None
    order_nr = None
    delivery_date = None
    c_products = []

    lang_dict = {"de": ["Bestellt am ", "Bestellnr."]}
    lang = "de"

    # sleep(random.randint(10, 30))
    res = ses.get(uri)
    logger.debug(f"Get order details: {res.status_code}")
    if res.ok:
        soup = BeautifulSoup(res.content, "html.parser")

        # Bestellnummer und Bestelldatum
        nr_date = soup.find_all("span", class_="order-date-invoice-item")
        for span_element in nr_date:
            span_info = span_element.get_text(strip=True)
            if lang_dict[lang][0] in span_info:
                order_date = span_info.replace(lang_dict[lang][0], "")

            if lang_dict[lang][1] in span_info:
                order_nr = span_info.replace(lang_dict[lang][1], "")

        delivery_date = get_shipment_stats(soup=soup)

        product_soups = soup.find_all("div", class_="a-fixed-left-grid")

        if product_soups:
            for p_soup in product_soups:
                # Extrahiere den Namen des Produkts
                product_name = p_soup.select_one(
                    "div.a-row > a.a-link-normal"
                ).text.strip()
                # Extrahiere den Preis des Produkts
                product_price = get_price(soup=p_soup)

                # Extrahiere den Link zum Produkt
                product_link = p_soup.select_one("div.a-row > a.a-link-normal")["href"]
                # Extrahiere das a-Element basierend auf der Klasse und dem href-Attribut
                a_elements = p_soup.find_all("a", class_="a-link-normal", href=True)
                logger.debug(f"Get order details: {product_link} loading picture")
                for a_element in a_elements:
                    # Extrahiere das img-Element innerhalb des a-Elements
                    img_element = a_element.find("img")
                    if img_element:
                        # Extrahiere Bild-URL
                        image_url = img_element["src"]
                        # Extrahiere Dateiname aus der Bild-URL
                        image_filename = image_url.split("/")[-1]
                        # Lade das Bild herunter
                        # sleep(random.randint(10, 30))
                        image_res = ses.get(image_url)
                        if image_res.ok:
                            # Speichere das Bild auf der Festplatte
                            img_path = os.path.join(path, "img", image_filename)
                            with open(img_path, "wb") as f:
                                f.write(image_res.content)

                        logger.debug(f"Get product and loading data is done")
                        c_products.append(
                            Product(
                                order_date=order_date,
                                delivery_date=delivery_date,
                                order_number=order_nr,
                                product_name=product_name,
                                product_price=product_price,
                                product_link=product_link,
                                image_filename=img_path,
                            )
                        )

        return c_products


def request_amazon(base_domain, year, user_agent, cookies, path="img"):
    # user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/120.0.6099.225 Safari/537.36'
    logger = setup_logging()

    ses = requests.Session()
    headers = {
        "User-Agent": user_agent,
    }
    logger.info(f"Request year: {year}")
    # Füge jedes Cookie aus der Liste zum Cookie-Jar hinzu
    cookie_jar = requests.cookies.RequestsCookieJar()
    for cookie in cookies:
        cookie_jar.set(cookie["name"], cookie["value"])

    ses.cookies = cookie_jar
    ses.headers.update(headers)

    c_products = []
    for start in range(0, 50, 10):
        logger.info(f"Request items beginning: {start}")
        url = f"{base_domain}/your-orders/orders?timeFilter=year-{year}&startIndex={start}"
        logger.debug(f"Request url: {url}")
        # url = "https://www.amazon.de/gp/your-account/order-details/ref=ppx_yo_dt_b_order_details_o00?ie=UTF8&orderID=305-1120833-4455507"
        # sleep(random.randint(10, 30))
        res = ses.get(url)
        logger.debug(f"Response status code: {res.status_code}")
        if res.ok:
            soup = BeautifulSoup(res.content, "html.parser")
            links = soup.find_all("a", class_="a-link-normal", href=True)
            if len(links) == 0:
                break

            else:
                for link in links:
                    uri = f"{base_domain}{link.attrs["href"]}"
                    if (
                        not "digital" in uri
                        and "order-details" in uri
                        and "orderID" in uri
                    ):
                        uri = uri.replace("/css/", "/your-account/")
                        c_products.extend(get_order_details(ses, uri, path=path))

    return c_products
