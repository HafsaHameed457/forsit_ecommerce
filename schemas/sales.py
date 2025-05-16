from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class SortField(str, Enum):
    date = "date"
    amount = "amount"
    quantity = "quantity"

class GetSalesRecords(BaseModel):
    start_date: Optional[date] =Field(None)
    end_date: Optional[date] =Field(None)
    product_id: Optional[str] =Field(None)
    category_id: Optional[str] =Field(None)
    sort: SortField = SortField.date
    limit: int = Field(100, ge=1, le=1000)
    page: int = Field(1, ge=1)