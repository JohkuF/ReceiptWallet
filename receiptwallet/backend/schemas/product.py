from datetime import datetime

from pydantic import BaseModel, field_validator


class Product(BaseModel):
    date: str = "today"
    product: str
    category: str
    price: float

    @field_validator("date")
    def check_date(date):
        if date == "today":
            return datetime.now().isoformat()
        return date
