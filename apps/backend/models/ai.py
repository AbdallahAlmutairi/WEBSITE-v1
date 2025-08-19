from __future__ import annotations

from pydantic import BaseModel


class AskRequest(BaseModel):
    symbol: str
    timeframe: str
    question: str
