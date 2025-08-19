# AI-Driven Stock Analysis Web App

Monorepo containing a Next.js frontend and FastAPI backend for real-time stock analysis, trend detection and AI Q&A.

## Structure

```
apps/
  frontend/  # Next.js 14 app
  backend/   # FastAPI service
```

## Requirements

- Node.js 20+
- Python 3.11+
- Redis (optional)

## Setup

1. Copy `.env.example` to `.env` and fill in values.
2. Backend:
   ```bash
   cd apps/backend
   pip install -r requirements.txt  # optional, Docker installs automatically
   uvicorn main:app --reload
   ```
3. Frontend:
   ```bash
   cd apps/frontend
   npm install
   npm run dev
   ```
4. Visit `http://localhost:3000`.

## Docker

```
docker compose up --build
```

## Providers

The default provider uses Yahoo Finance HTTP polling. To add a new real-time provider, implement the `DataProvider` protocol in `apps/backend/data/provider_base.py` and update `core/config.py`.

## Notes

- Saudi tickers require the `.SR` suffix (e.g. `2222.SR`).
- The demo AI endpoint streams responses via SSE. Provide an `OPENAI_API_KEY` in the `.env` to enable real answers.
- Trend calculations use EMA slope, MACD histogram, RSI bias and ADX strength.

This project is a simplified foundation intended for extension and experimentation.
