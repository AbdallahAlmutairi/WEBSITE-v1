from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fastapi.testclient import TestClient

from ..main import app
from ..api import routes_market, routes_ai
from ..models.market import Candle, Quote
from ..services.trend import trend_from_candles


def _generate_df(slope: float) -> pd.DataFrame:
    close = np.linspace(100, 100 + slope * 99, 100)
    df = pd.DataFrame(
        {
            "open": close,
            "high": close + 1,
            "low": close - 1,
            "close": close,
            "volume": np.ones_like(close),
        }
    )
    return df


def _candles_from_df(df: pd.DataFrame) -> list[Candle]:
    candles: list[Candle] = []
    for idx, row in df.iterrows():
        candles.append(
            Candle(
                ts=pd.Timestamp("2024-01-01") + pd.Timedelta(minutes=idx),
                open=row.open,
                high=row.high,
                low=row.low,
                close=row.close,
                volume=row.volume,
            )
        )
    return candles


class DummyProvider:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self.candles = _candles_from_df(df)

    async def get_quote(self, symbol: str) -> Quote:  # pragma: no cover - unused in tests
        return Quote(
            symbol=symbol,
            price=float(self.df.close.iloc[-1]),
            open=float(self.df.open.iloc[0]),
            high=float(self.df.high.max()),
            low=float(self.df.low.min()),
            prev_close=float(self.df.close.iloc[-2]),
            change=float(self.df.close.iloc[-1] - self.df.close.iloc[-2]),
            change_percent=0.0,
            ts=pd.Timestamp("2024-01-01"),
        )

    async def get_history(self, symbol: str, interval: str, lookback: str) -> list[Candle]:
        return self.candles

    async def stream_quotes(self, symbols: list[str]):  # pragma: no cover - unused
        yield await self.get_quote(symbols[0])


@pytest.fixture
def uptrend_provider(monkeypatch):
    df = _generate_df(1)
    prov = DummyProvider(df)
    routes_market.provider = prov
    routes_ai.provider = prov
    return prov


def test_trend_from_candles_uptrend():
    df = _generate_df(1)
    result = trend_from_candles(df)
    assert result["label"] == "Uptrend"
    assert result["score"] > 0


def test_trend_api(uptrend_provider):
    client = TestClient(app)
    resp = client.get("/api/trend", params={"symbol": "TEST"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["label"] == "Uptrend"
