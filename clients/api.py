from typing import Any, Dict, Optional

import httpx


async def get(
    url: str,
    params: Optional[Dict[str, Any]] = None,
) -> httpx.Response:
    """
    Make a GET request.

    Args:
        url: Endpoint URL
        params: Query parameters

    Returns:
        httpx.Response object
    """
    async with httpx.AsyncClient() as client:
        return await client.get(url, params=params)
