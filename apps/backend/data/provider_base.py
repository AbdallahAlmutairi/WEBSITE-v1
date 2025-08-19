from __future__ import annotations

from typing import Protocol, AsyncIterator, List

from ..models.market import Quote, Candle


class DataProvider(Protocol):
    async def get_quote(self, symbol: str) -> Quote:
        ...

    async def get_history(self, symbol: str, interval: str, lookback: str) -> List[Candle]:
        ...

    async def stream_quotes(self, symbols: list[str]) -> AsyncIterator[Quote]:
        ...
