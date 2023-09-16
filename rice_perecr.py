import requests
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime


PRODUCT_URL = "https://www.perekrestok.ru/cat/464/p/ris-agro-alans-slim-fit-ekstra-buryj-800g-2167599"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
page = requests.get(url=PRODUCT_URL, headers=headers)

soup = BeautifulSoup(page.content, "lxml")
product_title = soup.find("h1", class_="sc-fubCfw cqjzZF product__title").get_text()

product_price = soup.find("div", class_="price-new").get_text()
product_price = product_price.replace(",", ".")
product_price_int = Decimal(sub(r"[^\d\-.]", "", product_price))
#print(product_title)
#print(product_price_int, type(product_price_int))

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

is_exist = session.query(Price).filter(Price.name==product_title).order_by(Price.datetime.desc()).first()
if not is_exist:
    session.add(
        Price(
            name=product_title,
            price=product_price,
            price_int=product_price_int,
            datetime=datetime.now()
        )
    )
    session.commit()
else:
    if is_exist.price_int != product_price_int:
        session.add(
            Price(
                name=product_title,
                price=product_price,
                price_int=product_price_int,
                datetime= datetime.now()
            )
        )
        session.commit()

items = session.query(Price).all()

for item in items:
    print(item)