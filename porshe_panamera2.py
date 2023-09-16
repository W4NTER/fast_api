from selenium import webdriver
from bs4 import BeautifulSoup
from re import sub
from decimal import Decimal

PRODUCT_URL = "https://ekaterinburg.drom.ru/porsche/panamera/46267626.html"
driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get(PRODUCT_URL)

html = driver.page_source
soup = BeautifulSoup(html, "lxml")
year2 = soup.find(class_="css-1kb7l9z e162wx9x0").get_text()
price2 = soup.find("div", class_="css-eazmxc e162wx9x0").get_text()
price_int2 = Decimal(sub(r"[^\d\-.]", "", price2))
mileage2 = soup.find_all("td", class_="css-lm1m3k ezjvm5n1", colspan = "1")[6].get_text()
mileage_int2 = Decimal(sub(r"[^\d\-.]", "", mileage2))
year_int2 = Decimal(sub(r"[^\d\-.]", "", year2))
driver.close()
driver.quit()
