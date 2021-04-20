import requests
from bs4 import BeautifulSoup
import datetime

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
       

keyword = input("Enter search parameter:")
specify = input("Enter label criteria: ")
prodlist = []
for iterate in range(0,5):
    URL = 'https://www.canadacomputers.com/search/results_details.php?language=en&keywords='+keyword+"&page_num="+str(iterate)

    page = requests.get(URL)
   
    parser = BeautifulSoup(page.content, 'html.parser')

    results = parser.find(id="product-list")

    prod_cards = results.find_all('div', class_="col-12 py-1 px-1 bg-white mb-1 productTemplate gridViewToggle")
    for i in prod_cards:
        link = (i.find('span', class_='text-dark d-block productTemplate_title')).find('a', class_='text-dark text-truncate_3')['href']
        try:
            price = i.find('span', class_='d-block mb-0 pq-hdr-product_price line-height').text
        except:
            price = i.find('span', class_='text-danger d-block mb-0 pq-hdr-product_price line-height').text
        name = (i.find('span', class_='text-dark d-block productTemplate_title')).text
        if specify.lower() in name.lower():
            prodlist.append(Product(link, (price.strip('$')).replace(',', ''), name))
        else:
           continue

for o in prodlist:
    if o.check_stock():
        print("-------------------------")
        print("LABEL:", o.return_name())
        print("PRICE: $" + str(o.return_price()))
        print("LINK: ", o.return_link())
        print("--------------------------")
