from datetime import datetime

from pydantic import BaseModel


class Product(BaseModel):
    date: str
    product: str
    category: str
    price: float
