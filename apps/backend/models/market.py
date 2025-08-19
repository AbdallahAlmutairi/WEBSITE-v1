from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel
from typing import Literal


class Quote(BaseModel):
    symbol: str
    price: float
    open: float
    high: float
    low: float
    prev_close: float
    change: float
    change_percent: float
    ts: datetime


class Candle(BaseModel):
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class Technicals(BaseModel):
    rsi: float
    macd: float
    macd_signal: float
    macd_hist: float
    adx: float
    ema20: float
    ema50: float
    ema200: float


class TrendResult(BaseModel):
    label: Literal['Uptrend', 'Downtrend', 'Ranging']
    score: float
    confidence: float
    reasons: list[str]
