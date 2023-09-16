from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class Panama(Base):
    __tablename__ = "panamera"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    year = Column(Numeric)
    datetime = Column(DateTime)
    price = Column(Numeric)
    mileage = Column(Numeric)