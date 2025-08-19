from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd

from .indicators import indicators


def trend_from_candles(df: pd.DataFrame) -> Dict[str, object]:
    ind = indicators(df)
    ema20_series = df.close.ewm(span=20, adjust=False).mean()
    y = ema20_series.tail(20).values
    x = np.arange(len(y))
    slope = np.polyfit(x, y, 1)[0]
    slope_norm = float(slope / (df.close.tail(20).std() + 1e-8))

    macd_hist_z = float(
        ind["macd_hist"] / (df.close.pct_change().rolling(50).std().iloc[-1] + 1e-6)
    )
    rsi_bias = (ind["rsi"] - 50.0) / 50.0
    adx_strength = min(ind["adx"], 50) / 50.0

    score = 0.35 * slope_norm + 0.30 * macd_hist_z + 0.20 * rsi_bias + 0.15 * adx_strength
    label = "Uptrend" if score > 0.4 else ("Downtrend" if score < -0.4 else "Ranging")
    conf = min(1.0, abs(score))
    reasons: list[str] = []
    if slope_norm > 0:
        reasons.append("EMA20 slope rising")
    else:
        reasons.append("EMA20 slope falling")
    if ind["macd_hist"] > 0:
        reasons.append("MACD histogram > 0")
    else:
        reasons.append("MACD histogram < 0")
    if ind["rsi"] > 55:
        reasons.append("RSI above 55")
    elif ind["rsi"] < 45:
        reasons.append("RSI below 45")
    if ind["adx"] > 20:
        reasons.append("Trend strength (ADX) > 20")
    return {
        "label": label,
        "score": float(score),
        "confidence": float(conf),
        "reasons": reasons,
    }
