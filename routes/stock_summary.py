from fastapi import APIRouter, HTTPException
from clients.api import get
import httpx
from auxiliary.stock_summary import stock_summary

router = APIRouter()

@router.get("/symbols/{symbol}/annual/{year}")
async def get_stock_summary(symbol: str, year: int):
    """
    API endpoint to get the annual stock summary for a given symbol and year.

    Args:
        symbol: Stock symbol (e.g., AAPL)
        year: Year for the summary (e.g., 2023)
    Returns:
        A dictionary containing the stock summary for the specified symbol and year.    
    """
    try:
        summary = await stock_summary(symbol, year)
        return summary
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
   