from typing import Union

from pydantic import BaseModel


class PanamaBase(BaseModel):
    url: str
    year: int
    price: int
    mileage: int


class PanamaCreate(PanamaBase):
    datetime: str


class Panama(PanamaBase):
    id: int

    class Config:
        orm_mode = True