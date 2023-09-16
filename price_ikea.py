import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer
from sqlalchemy.ext.declarative import declarative_base

PRODUCT_URL = "https://www.ozon.ru/product/botinki-buteks-tropik-597198420/?asb=pwkjlB2MDZgIxGKxzKrkOlaGjHN7dPqPvh8dizaoCXM%253D&asb2=UqFpokFUGJoK542TLJpQoY3Da0HSp7lFzy4OebWsdY8yc3y8Y9UJvSPq1M-DFzM3&sh=OwCN6OGslw"

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}
page = requests.get(url=PRODUCT_URL, headers=headers)
# print(page.content)

soup = BeautifulSoup(page.content, "lxml")
title = soup.find("span", class_="pip-header-section__title--big notranslate").get_text()
print(title)

price = soup.find("span", class_="pip-price__integer").get_text()
price = int(price.replace(" ", ""))
print(price, type(price))

Base = declarative_base()

class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)

engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)
