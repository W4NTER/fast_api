from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from datetime import datetime
from porshe_panamera import year_int, price_int, mileage_int, PRODUCT_URL1
from porshe_panamera2 import year_int2, price_int2, mileage_int2, PRODUCT_URL

Base = declarative_base()


class Price(Base):
    __tablename__ = "panamera"

    id = Column(Integer, primary_key=True)
    year = Column(Numeric)
    datetime = Column(DateTime)
    url = Column(String)
    price = Column(Numeric(10, 2))
    mileage = Column(Numeric)


engine = create_engine("sqlite:///data_base2.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)


def add_panama(year, price, mileage, url):
    is_exist = session.query(Price).filter(Price.mileage == mileage).order_by(Price.datetime.desc()).first()

    if not is_exist:
        session.add(
            Price(
                year=year,
                price=price,
                mileage=mileage,
                url=url,
                datetime=datetime.now()

            )
        )
        session.commit()
    else:
        if is_exist.price != price:
            session.add(
                Price(
                    year=year,
                    price=price,
                    mileage=mileage,
                    url=url,
                    datetime=datetime.now()
                )
            )
            session.commit()


add_panama(year_int, price_int, mileage_int, PRODUCT_URL1)
add_panama(year_int2, price_int2, mileage_int2, PRODUCT_URL)
