from fastapi import HTTPException
from clients.api import get
import httpx
from database.db import Database
from settings import settings

from models.alpha_response import AlphavantageResponse


async def stock_summary(symbol: str, year: int) -> dict:
    db = Database()

    # Check if data is already in the database
    summary = db.get_annual_summary(symbol, year)
    if summary:
        return summary

    # Fetch data from API
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey={settings.alphavantage_api_key}"
    try:
        response = await get(url)
        response.raise_for_status()
        data = response.json()

        # Validate API response structure using pydantic
        try:
            AlphavantageResponse(**data)
        except Exception as e:
            # if the structure was unexpected, propagate as HTTPException
            raise HTTPException(status_code=400, detail=f"{response.json()}")

        # Calculate summary for the year
        summary = calculate_yearly_summary(data, symbol, year)
        if summary:
            # Store the summary in the database
            db.store_annual_record(
                {
                    "symbol": symbol,
                    "year": year,
                    "high": summary["high"],
                    "low": summary["low"],
                    "volume": summary["volume"]
                }
            )

        return summary
    
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
from fastapi import HTTPException

def calculate_yearly_summary(data: dict, symbol: str, year: int) -> dict:
    monthly_series = data.get("Monthly Time Series", {})

    year_str = str(year)

    high = float("-inf")
    low = float("inf")
    volume = 0
    found = False

    for date_str, values in monthly_series.items():
        if not date_str.startswith(year_str):
            continue

        found = True

        try:
            h = float(values.get("2. high", 0))
            l = float(values.get("3. low", 0))
            v = int(values.get("5. volume", 0))
        except (ValueError, TypeError):
            continue

        if h > high:
            high = h

        if l < low:
            low = l

        volume += v

    if not found:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for {symbol} in {year}"
        )

    return {
        "high": None if high == float("-inf") else high,
        "low": None if low == float("inf") else low,
        "volume": volume
    }
