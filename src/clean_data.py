import os
import pandas as pd

INPUT_FOLDER = "data/raw"
OUTPUT_FOLDER = "data/processed"

FILES = ["SPY.csv", "QQQ.csv", "GOLD.csv", "AAPL.csv", "TSLA.csv"]

REQUIRED_COLUMNS = ["Date", "Open", "High", "Low", "Close", "Volume"]


def load_data():
    dataframes = {}

    for file_name in FILES:
        file_path = os.path.join(INPUT_FOLDER, file_name)
        df = pd.read_csv(file_path)

        if not all(col in df.columns for col in REQUIRED_COLUMNS):
            raise ValueError(f"{file_name} is missing required columns")

        df = df[REQUIRED_COLUMNS].copy()
        df["Date"] = pd.to_datetime(df["Date"])
        df = df.sort_values("Date").drop_duplicates(subset="Date")
        dataframes[file_name] = df

    return dataframes


def find_common_date_range(dataframes):
    start_dates = [df["Date"].min() for df in dataframes.values()]
    end_dates = [df["Date"].max() for df in dataframes.values()]

    common_start = max(start_dates)
    common_end = min(end_dates)

    return common_start, common_end


def build_common_calendar(dataframes, common_start, common_end):
    all_dates = set()

    for df in dataframes.values():
        filtered = df[(df["Date"] >= common_start) & (df["Date"] <= common_end)]
        all_dates.update(filtered["Date"].tolist())

    common_calendar = sorted(all_dates)
    return pd.DatetimeIndex(common_calendar)


def clean_and_align_data(dataframes, common_start, common_end, common_calendar):
    cleaned_data = {}

    for file_name, df in dataframes.items():
        df = df[(df["Date"] >= common_start) & (df["Date"] <= common_end)].copy()
        df = df.set_index("Date")
        df = df.reindex(common_calendar)

        df["Open"] = df["Open"].ffill()
        df["High"] = df["High"].ffill()
        df["Low"] = df["Low"].ffill()
        df["Close"] = df["Close"].ffill()
        df["Volume"] = df["Volume"].fillna(0)

        df = df.reset_index().rename(columns={"index": "Date"})
        cleaned_data[file_name] = df

    return cleaned_data


def save_data(cleaned_data):
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for file_name, df in cleaned_data.items():
        output_path = os.path.join(OUTPUT_FOLDER, file_name)
        df.to_csv(output_path, index=False)
        print(f"Saved cleaned file: {output_path}")


def main():
    dataframes = load_data()

    common_start, common_end = find_common_date_range(dataframes)
    print(f"Common start date: {common_start.date()}")
    print(f"Common end date: {common_end.date()}")

    common_calendar = build_common_calendar(dataframes, common_start, common_end)
    cleaned_data = clean_and_align_data(dataframes, common_start, common_end, common_calendar)

    save_data(cleaned_data)


if __name__ == "__main__":
    main()