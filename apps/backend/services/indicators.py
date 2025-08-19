from __future__ import annotations

from typing import Dict

import pandas as pd
import pandas_ta as ta


def indicators(df: pd.DataFrame) -> Dict[str, float]:
    out: Dict[str, float] = {}
    out["ema20"] = float(ta.ema(df.close, 20).iloc[-1])
    out["ema50"] = float(ta.ema(df.close, 50).iloc[-1])
    out["ema200"] = float(ta.ema(df.close, 200).iloc[-1])
    r = ta.rsi(df.close, 14)
    out["rsi"] = float(r.iloc[-1])
    m = ta.macd(df.close, 12, 26, 9)
    out["macd"] = float(m["MACD_12_26_9"].iloc[-1])
    out["macd_signal"] = float(m["MACDs_12_26_9"].iloc[-1])
    out["macd_hist"] = float(m["MACDh_12_26_9"].iloc[-1])
    a = ta.adx(high=df.high, low=df.low, close=df.close, length=14)
    out["adx"] = float(a["ADX_14"].iloc[-1])
    return out
