from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Price(BaseModel):
    name: str
    price: float

PRICES_DB = [
    Price(name="test1", price=1000),
    Price(name="test2", price=1212),
    Price(name="test3", price=13232),
    Price(name="test4", price=143400),
    Price(name="test5", price=200)
]


@app.get("/prices")
def read_prices():
    return PRICES_DB

@app.get("/price/{item_id}")
def read_price(item_id: int):
    return PRICES_DB[item_id]


@app.put("/price/{item_id}")
def update_price(item_id: int, item: Price):
    PRICES_DB[item_id] = item
    return {"status": "ok"}

@app.post("/price/create")
def create_price(item: Price):
    PRICES_DB.append(item)
    return {"status": "ok"}

@app.delete("/price/{item_id}")
def delete_price(item_id: int):
    del PRICES_DB[item_id]
    return {"status": "ok"}

