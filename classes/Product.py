import requests
from bs4 import BeautifulSoup
class Product:
    link = ""
    price = 0
    name = ""

    def __init__(self, href, prc, nm):
        self.link = href
        self.name = nm
        self.price = float(prc)
    def return_price(self):
        return self.price
    def return_name(self):
        return self.name
    def return_link(self):
        return self.link
    def check_stock(self):
        temp_url = self.link
        temp_page = requests.get(temp_url)
        temp_parser = BeautifulSoup(temp_page.content, 'html.parser')
        stockbox = temp_parser.find('div', class_="pi-prod-availability")
        stocks_list = stockbox.find_all('span')
        for i in stocks_list:
            if 'not available online' in (i.text.strip(" ")).lower() or "out of stock" in (i.text.strip(" ")).lower():
                continue
            else:
                return True
        return False