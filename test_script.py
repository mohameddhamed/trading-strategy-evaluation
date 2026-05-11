import pandas as pd, numpy as np
from unittest.mock import patch

np.random.seed(42)
days = 200
prices = 100 * np.cumprod(1 + np.random.normal(0.001, 0.02, days))
df = pd.DataFrame({
    "Open": prices * 0.99, "High": prices * 1.01,
    "Low": prices * 0.98, "Close": prices,
    "Volume": np.random.randint(100_000, 500_000, days),
}, index=pd.date_range("2023-01-01", periods=days))

from src.engine.core import run_backtest

with patch("src.engine.core._load_csv", return_value=df):
    result = run_backtest("SMACrossover", "SPY", {"short_window": 10, "long_window": 50})

import json

print(json.dumps(result, indent=2))