from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.engine.core import run_backtest, STRATEGY_MAP
import sys, os
from typing import Optional

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

app = FastAPI(
    title="Trading Strategy Evaluation API",
    description="Backend engine for calculating quantitative strategy performance.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class StrategyRequest(BaseModel):
    strategy: str
    asset: str
    parameters: dict
    start_date: Optional[str] = "2018-01-01"
    end_date: Optional[str] = "2024-06-30"
    initial_capital: Optional[float] = 100_000.0


@app.get("/api/health")
def read_health_check():
    return {"status": "online", "message": "Trading Engine API is running."}


@app.get("/api/strategies")
def list_strategies():
    return {"strategies": list(STRATEGY_MAP.keys())}


@app.post("/api/run")
def run_strategy(request: StrategyRequest):
    try:
        result = run_backtest(request.strategy, request.asset, request.parameters)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No data file found for asset '{request.asset}'.")
