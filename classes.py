class Product:
    def __init__(self, order_date, delivery_date, order_number, product_name, product_price, product_link, image_filename):
        self.order_date = order_date
        self.delivery_date = delivery_date
        self.order_number = order_number
        self.product_name = product_name
        self.product_price = product_price
        self.product_link = product_link
        self.image_filename = image_filename

    def __repr__(self):
        return (
            f"Bestelldatum: {self.order_date} "
            f"Lieferdatum: {self.delivery_date} "
            f"Bestellnummer: {self.order_number} "
            f"Produktname: {self.product_name} "
            f"Preis: {self.product_price} "
            f"Bild: {self.image_filename}"
        )

class InvalidEmailError(ValueError):
    pass

class InvalidPasswordError(ValueError):
    pass

class InvalidTotpError(ValueError):
    pass

class MissingTotpError(ValueError):
    pass