from __future__ import annotations
from typing import Dict
from pydantic import BaseModel, Field, RootModel


class MetaData(BaseModel):
    information: str = Field(..., alias="1. Information")
    symbol: str = Field(..., alias="2. Symbol")
    last_refreshed: str = Field(..., alias="3. Last Refreshed")
    time_zone: str = Field(..., alias="4. Time Zone")

    model_config = {
        "populate_by_name": True
    }


class TimeSeriesEntry(BaseModel):
    open: float = Field(..., alias="1. open")
    high: float = Field(..., alias="2. high")
    low: float = Field(..., alias="3. low")
    close: float = Field(..., alias="4. close")
    volume: int = Field(..., alias="5. volume")

    model_config = {
        "populate_by_name": True
    }


# Use RootModel for dict-like root structure
class MonthlyTimeSeries(RootModel[Dict[str, TimeSeriesEntry]]):
    model_config = {
        "populate_by_name": True
    }


class AlphavantageResponse(BaseModel):
    meta_data: MetaData = Field(..., alias="Meta Data")
    monthly_time_series: MonthlyTimeSeries = Field(..., alias="Monthly Time Series")

    model_config = {
        "populate_by_name": True
    }