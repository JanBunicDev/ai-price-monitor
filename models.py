from typing import Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field


class ProductData(BaseModel):
    name: str =  Field(description="The full title or name of the product")
    price: float = Field(
        description="The numerical price of the product without numerical simbols"
    )
    in_stock: bool = Field(
        "True if the product is in stock False otherwise"
    )
    rating: Optional[float] = Field(
        default=None, description = "Stars out of 5 if available"
    )
    summary: str = Field(
        description = "A brief one sentense overview of the product"
    )


class ProductDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: float
    in_stock: bool
    rating: Optional[float] = None
    summary: str

