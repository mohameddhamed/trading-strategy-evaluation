from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.engine.core import run_backtest, STRATEGY_REGISTRY

app = FastAPI(
    title="Trading Strategy Evaluation API",
    description="Backend engine for calculating quantitative strategy performance.",
)


class StrategyRequest(BaseModel):
    strategy: str
    asset: str
    parameters: dict


@app.get("/api/health")
def read_health_check():
    return {"status": "online", "message": "Trading Engine API is running."}


@app.get("/api/strategies")
def list_strategies():
    return {"strategies": list(STRATEGY_REGISTRY.keys())}


@app.post("/api/run")
def run_strategy(request: StrategyRequest):
    try:
        result = run_backtest(request.strategy, request.asset, request.parameters)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"No data file found for asset '{request.asset}'.")
