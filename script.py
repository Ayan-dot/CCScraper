import requests
from bs4 import BeautifulSoup
import datetime
from classes.Product import Product
import sqlite3
     

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

prod_db = sqlite3.connect('productdb.sqlite')
db_cursor = prod_db.cursor()

db_cursor.execute('CREATE TABLE IF NOT EXISTS Products (name TEXT, price FLOAT, link TEXT, in_stock BIT)')
for o in prodlist:
    db_cursor.execute('SELECT in_stock from Products WHERE name = ?', (o.name, ))
    entry = db_cursor.fetchone()
    if entry is None:
        db_cursor.execute('INSERT INTO Products (name, price, link, in_stock) VALUES (?,?,?,?)', (o.name, o.price, o.link, int(o.check_stock())))
        print("didit")
    else: 
        db_cursor.execute('UPDATE Products SET in_stock = ? WHERE name = ?', (int(o.check_stock()), o.name))
    prod_db.commit()
    # if o.check_stock():
    #     print("-------------------------")
    #     print("LABEL:", o.return_name())
    #     print("PRICE: $" + str(o.return_price()))
    #     print("LINK: ", o.return_link())
    #     print("--------------------------")

