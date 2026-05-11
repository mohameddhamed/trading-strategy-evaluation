import yfinance as yf
import pandas as pd
import os

TICKERS = {
    "SPY": "SPY",
    "QQQ": "QQQ",
    "GOLD": "GLD",
    "AAPL": "AAPL",
    "TSLA": "TSLA"
}

START_DATE = "2010-01-01"

OUTPUT_FOLDER = "data/raw"


def download_data():
    for name, ticker in TICKERS.items():
        print(f"Downloading {name}...")

        data = yf.download(ticker, start=START_DATE)

        data.reset_index(inplace=True)

        data = data[["Date", "Open", "High", "Low", "Close", "Volume"]]

        file_path = os.path.join(OUTPUT_FOLDER, f"{name}.csv")

        data.to_csv(file_path, index=False)

        print(f"Saved {name} to {file_path}")

def align_dates():
    dataframes = {}

    for name in TICKERS.keys():
        file_path = os.path.join(OUTPUT_FOLDER, f"{name}.csv")
        df = pd.read_csv(file_path, parse_dates=["Date"])
        dataframes[name] = df

    start_dates = [df["Date"].min() for df in dataframes.values()]
    end_dates = [df["Date"].max() for df in dataframes.values()]

    common_start = max(start_dates)
    common_end = min(end_dates)

    print(f"Common start date: {common_start}")
    print(f"Common end date: {common_end}")

    for name, df in dataframes.items():
        aligned = df[(df["Date"] >= common_start) & (df["Date"] <= common_end)]

        file_path = os.path.join(OUTPUT_FOLDER, f"{name}.csv")
        aligned.to_csv(file_path, index=False)

        print(f"Aligned {name}")

if __name__ == "__main__":
    download_data()
    align_dates()