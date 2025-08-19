from __future__ import annotations

from fastapi import APIRouter, HTTPException
import pandas as pd

from apps.backend.core.cache import cache
from apps.backend.data.provider_yahoo import YahooProvider
from apps.backend.models.market import Candle, Quote, Technicals, TrendResult
from apps.backend.services.indicators import indicators
from apps.backend.services.trend import trend_from_candles

router = APIRouter(prefix="/api")
provider = YahooProvider()


@router.get("/quote", response_model=Quote)
async def get_quote(symbol: str) -> Quote:
    key = f"quote:{symbol}"
    data = await cache.get(key)
    if data:
        return Quote.parse_raw(data)
    q = await provider.get_quote(symbol)
    await cache.set(key, q.json(), ttl=10)
    return q


@router.get("/history", response_model=list[Candle])
async def get_history(symbol: str, interval: str = "1d", lookback: str = "1mo") -> list[Candle]:
    try:
        candles = await provider.get_history(symbol, interval, lookback)
    except Exception:
        raise HTTPException(status_code=404, detail="Data not available")
    return candles


@router.get("/technicals", response_model=Technicals)
async def get_technicals(symbol: str, interval: str = "1d", lookback: str = "1mo") -> Technicals:
    candles = await provider.get_history(symbol, interval, lookback)
    df = pd.DataFrame([c.dict() for c in candles])
    ind = indicators(df)
    return Technicals(**ind)


@router.get("/trend", response_model=TrendResult)
async def get_trend(symbol: str, interval: str = "1d", lookback: str = "1mo") -> TrendResult:
    candles = await provider.get_history(symbol, interval, lookback)
    if len(candles) < 50:
        raise HTTPException(status_code=400, detail="Not enough data")
    df = pd.DataFrame([c.dict() for c in candles])
    result = trend_from_candles(df)
    return TrendResult(**result)
