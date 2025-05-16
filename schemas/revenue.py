from datetime import date
from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum
class AnalysisPeriod(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    annual = "annual"

class GetRevenueAnalysis(BaseModel):
    period: AnalysisPeriod = Field(...)
    start_date: Optional[date] = Field(
        None
    )
    end_date: Optional[date] = Field(
        None
    )
    compare_with_previous: bool = Field(
        False
    )



