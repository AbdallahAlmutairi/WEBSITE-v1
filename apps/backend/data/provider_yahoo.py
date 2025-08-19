from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from typing import AsyncIterator, List

import httpx

from ..models.market import Candle, Quote
from .provider_base import DataProvider


YAHOO_QUOTE_URL = "https://query1.finance.yahoo.com/v7/finance/quote"
YAHOO_CHART_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


class YahooProvider(DataProvider):
    async def get_quote(self, symbol: str) -> Quote:
        async with httpx.AsyncClient() as client:
            r = await client.get(YAHOO_QUOTE_URL, params={"symbols": symbol})
            r.raise_for_status()
            result = r.json()["quoteResponse"]["result"][0]
            price = float(result["regularMarketPrice"])
            prev = float(result.get("previousClose", price))
            change = price - prev
            change_percent = (change / prev * 100.0) if prev else 0.0
            return Quote(
                symbol=result["symbol"],
                price=price,
                open=float(result.get("regularMarketOpen", price)),
                high=float(result.get("regularMarketDayHigh", price)),
                low=float(result.get("regularMarketDayLow", price)),
                prev_close=prev,
                change=change,
                change_percent=change_percent,
                ts=datetime.fromtimestamp(result["regularMarketTime"], tz=timezone.utc),
            )

    async def get_history(self, symbol: str, interval: str, lookback: str) -> List[Candle]:
        async with httpx.AsyncClient() as client:
            r = await client.get(
                YAHOO_CHART_URL.format(symbol=symbol),
                params={"interval": interval, "range": lookback},
            )
            r.raise_for_status()
            data = r.json()["chart"]["result"][0]
            timestamps = data["timestamp"]
            quotes = data["indicators"]["quote"][0]
            candles: List[Candle] = []
            for i, ts in enumerate(timestamps):
                candles.append(
                    Candle(
                        ts=datetime.fromtimestamp(ts, tz=timezone.utc),
                        open=float(quotes["open"][i]),
                        high=float(quotes["high"][i]),
                        low=float(quotes["low"][i]),
                        close=float(quotes["close"][i]),
                        volume=float(quotes["volume"][i]),
                    )
                )
            return candles

    async def stream_quotes(self, symbols: list[str]) -> AsyncIterator[Quote]:
        while True:
            for s in symbols:
                yield await self.get_quote(s)
            await asyncio.sleep(1)
