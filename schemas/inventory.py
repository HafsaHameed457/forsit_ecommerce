from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class SortField(str, Enum):
    date = "date"
    amount = "amount"
    quantity = "quantity"

class GetInventory(BaseModel):
    product_id: Optional[str] = Field(
        None
    )
    category: Optional[str] = Field(
        None
    )
    start_date: Optional[date] = Field(
        None
    )
    end_date: Optional[date] = Field(
        None
    )
    sort: SortField = Field(
        SortField.date
    )
    low_stock_only: bool = Field(
        False
    )

class InventoryUpdate(BaseModel):
    amount: int = Field(
        None
    )
    product_id: str = Field(
        None
    )

    reason: Optional[str] = Field(
        None
    )
    