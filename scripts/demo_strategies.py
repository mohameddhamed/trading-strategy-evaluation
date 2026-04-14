import pandas as pd
import numpy as np
from src.strategies.classic import SMACrossover, RSIReversion


def generate_dummy_data(days=100):
    """Generates fake stock data for testing"""
    np.random.seed(42)
    price_changes = np.random.normal(loc=0.001, scale=0.02, size=days)
    prices = 100 * np.cumprod(1 + price_changes)
    volumes = np.random.randint(100000, 500000, size=days)
    dates = pd.date_range(start="2023-01-01", periods=days)
    return pd.DataFrame({"Close": prices, "Volume": volumes}, index=dates)


def main():
    print("--- GENERATING FAKE MARKET DATA ---")
    df = generate_dummy_data(100)

    print("\n--- TESTING SMA CROSSOVER ---")
    sma_strategy = SMACrossover(short_window=10, long_window=50)
    print(
        sma_strategy.execute(df)[
            ["Close", "Signal", "Market_Returns", "Strategy_Returns"]
        ].tail()
    )

    print("\n--- TESTING RSI REVERSION ---")
    rsi_strategy = RSIReversion(window=14)
    print(
        rsi_strategy.execute(df)[
            ["Close", "Signal", "Market_Returns", "Strategy_Returns"]
        ].tail()
    )


if __name__ == "__main__":
    main()
