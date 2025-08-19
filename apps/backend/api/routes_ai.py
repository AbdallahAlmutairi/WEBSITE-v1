from __future__ import annotations

import json
from typing import AsyncIterator

import httpx
from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..core.config import get_settings
from ..models.ai import AskRequest
from ..models.market import Candle, Technicals, TrendResult
from ..services.trend import trend_from_candles
from ..services.indicators import indicators
from ..data.provider_yahoo import YahooProvider
import pandas as pd

router = APIRouter(prefix="/api/ai")
settings = get_settings()
provider = YahooProvider()


async def _openai_stream(prompt: str) -> AsyncIterator[str]:
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.openai_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "stream": True,
        "messages": [
            {"role": "system", "content": "You are a professional market analyst."},
            {"role": "user", "content": prompt},
        ],
    }
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, headers=headers, json=payload) as resp:
            async for line in resp.aiter_lines():
                if line.startswith("data:"):
                    yield line[5:].strip()


@router.post("/ask")
async def ai_ask(req: AskRequest) -> StreamingResponse:
    if not settings.openai_api_key:
        async def fake() -> AsyncIterator[bytes]:
            yield b"data: OpenAI API key not configured\n\n"
            yield b"data: [DONE]\n\n"
        return StreamingResponse(fake(), media_type="text/event-stream")

    candles = await provider.get_history(req.symbol, req.timeframe, "30d")
    df = pd.DataFrame([c.dict() for c in candles])
    tech = indicators(df)
    trend = trend_from_candles(df)
    context = {"technicals": tech, "trend": trend}
    prompt = f"Context: {json.dumps(context)}\nQuestion: {req.question}"

    async def event_gen() -> AsyncIterator[bytes]:
        async for chunk in _openai_stream(prompt):
            yield f"data: {chunk}\n\n".encode()
        yield b"data: [DONE]\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")
