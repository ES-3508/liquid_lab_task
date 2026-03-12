from fastapi import HTTPException
from clients.api import get
import httpx



async def stock_summary(symbol: str, year: int) -> dict:

    # Fetch data from API
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol={symbol}&apikey=demo"
    try:
        response = await get(url)
        response.raise_for_status()
        data = response.json()
        
        # Calculate summary for the year
        summary = calculate_yearly_summary(data, symbol, year)

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
        "symbol": symbol,
        "year": year,
        "high": None if high == float("-inf") else high,
        "low": None if low == float("inf") else low,
        "volume": volume
    }
