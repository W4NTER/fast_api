from selenium import webdriver
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal

PRODUCT_URL = "https://www.citilink.ru/product/smartfon-vivo-y33s-128gb-4gb-chernyi-3g-4g-2sim-6-58-lcd-1080x2408-and-1680467/"
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get(PRODUCT_URL)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")
title = soup.find(class_="Heading Heading_level_1 ProductHeader__title").get_text()
price = soup.find("span", class_="ProductHeader__price-default_current-price js--ProductHeader__price-default_current-price").get_text()
price_int = Decimal(sub(r"[^\d\-.]", "", price))
title = str(title.replace(" ", ""))
driver.close()
driver.quit()

print(title, type(title))
print(price_int, type(price_int))