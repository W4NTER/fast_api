from re import sub
from decimal import Decimal
import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://www.perekrestok.ru/cat/434/p/sok-biotta-bio-morkovnyj-pramogo-otzima-500ml-22410"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
}
page = requests.get(url=PRODUCT_URL, headers=headers)
#  print(page.content)

soup = BeautifulSoup(page.content, "lxml")
product_title = soup.find(
    "h1",
    class_="sc-fubCfw cqjzZF product__title"
).get_text()


product_price = soup.find("div", class_="price-new").get_text()
product_price = product_price.replace(",", ".")
product_price_int = Decimal(sub(r"[^\d\-.]", "", product_price))
#  print(price, type(price), price_int, type(price_int))


# --------------------------------------------
#             IKEA PRICE
#---------------------------------------------

PRODUCT_URL = "https://www.ikea.com/ru/ru/p/kaseberga-koseberga-plyazhnyy-stul-dlya-sada-akaciya-chernyy-belyy-60514407/"

headers = {
    "user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0"
}
page = requests.get(url=PRODUCT_URL, headers=headers)
#  print(page.content)

soup = BeautifulSoup(page.content, "lxml")
ikea_title = soup.find(
    "span",
    class_="pip-header-section__title--big notranslate"
).get_text()

ikea_price = soup.find("span", class_="pip-price__integer").get_text()
#  price = int(price.replace(" ", ""))
ikea_price_int = sub(r"[^\d\-.]", "", ikea_price)

# --------------------------------------------
#               DATABASE
# --------------------------------------------

from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    datetime = Column(DateTime)
    price = Column(String(64))
    price_int = Column(Numeric(10, 2))

    def __repr__(self):
        return f"{self.name} | {self.price}"

engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)

def add_price(title, price, price_int):
    is_exist = session.query(Price).filter(
        Price.name==title
    ).order_by(Price.datetime.desc()).first()

    if not is_exist:
        session.add(
            Price(
                name=title,
                datetime=datetime.now(),
                price=price,
                price_int=price_int
            )
        )
        session.commit()
    else:
        if is_exist.price_int != price_int:
            session.add(
                Price(
                    name=title,
                    datetime=datetime.now(),
                    price=price,
                    price_int=price_int
                )
            )
            session.commit()


add_price(product_title, product_price, product_price_int)
add_price(ikea_title, ikea_price, ikea_price_int)

items = session.query(Price).all()
for item in items:
    print(item)
