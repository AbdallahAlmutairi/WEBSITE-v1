from __future__ import annotations

import os
from functools import lru_cache
from pydantic import BaseModel


class Settings(BaseModel):
    provider: str = "YAHOO"
    openai_api_key: str | None = None
    redis_url: str | None = None


@lru_cache
def get_settings() -> Settings:
    return Settings(
        provider=os.getenv("PROVIDER", "YAHOO"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        redis_url=os.getenv("REDIS_URL"),
    )
