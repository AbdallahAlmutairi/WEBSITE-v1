from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.backend.api.routes_market import router as market_router
from apps.backend.api.routes_ai import router as ai_router

app = FastAPI(title="Stock Analysis API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(market_router)
app.include_router(ai_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "ok"}
