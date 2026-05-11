import numpy as np
import pandas as pd
from typing import Any
from src.strategies.base import BaseStrategy


class SMACrossover(BaseStrategy):
    def __init__(self, name="SMA Crossover", short_window=10, long_window=50):
        super().__init__(name)
        self.short_window = short_window
        self.long_window = long_window

    @classmethod
    def get_parameters(cls) -> dict[str, dict[str, Any]]:
        return {
            "short_window": {"type": "int", "default": 10, "min": 1, "max": 100},
            "long_window": {"type": "int", "default": 50, "min": 1, "max": 500},
        }

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        short_ma = data["Close"].rolling(window=self.short_window).mean()
        long_ma = data["Close"].rolling(window=self.long_window).mean()

        # +1 if short trend is above long trend, else -1
        data["Signal"] = np.where(
            short_ma > long_ma, 1, np.where(short_ma < long_ma, -1, 0)
        )
        return data


class RSIReversion(BaseStrategy):
    def __init__(self, name="RSI Reversion", window=14, lower_bound=30, upper_bound=70):
        super().__init__(name)
        self.window = window
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    @classmethod
    def get_parameters(cls) -> dict[str, dict[str, Any]]:
        return {
            "window": {"type": "int", "default": 14, "min": 1, "max": 50},
            "lower_bound": {"type": "int", "default": 30, "min": 1, "max": 50},
            "upper_bound": {"type": "int", "default": 70, "min": 50, "max": 99},
        }

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        delta = data["Close"].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate Exponential Moving Average of gains and losses
        avg_gain = gain.ewm(alpha=1 / self.window, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1 / self.window, adjust=False).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        # +1 if oversold (price dropped too much), -1 if overbought (price surged too much)
        data["Signal"] = np.where(
            rsi < self.lower_bound, 1, np.where(rsi > self.upper_bound, -1, 0)
        )
        return data


class BollingerBands(BaseStrategy):
    def __init__(self, name="Bollinger Bands", window=20, num_std=2):
        super().__init__(name)
        self.window = window
        self.num_std = num_std

    @classmethod
    def get_parameters(cls) -> dict[str, dict[str, Any]]:
        return {
            "window": {"type": "int", "default": 20, "min": 1, "max": 100},
            "num_std": {"type": "float", "default": 2.0, "min": 0.5, "max": 5.0},
        }

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        sma = data["Close"].rolling(window=self.window).mean()
        std = data["Close"].rolling(window=self.window).std()

        upper_band = sma + (std * self.num_std)
        lower_band = sma - (std * self.num_std)

        # Buy (+1) if price breaks below lower band, Sell (-1) if it breaks above upper band
        data["Signal"] = np.where(
            data["Close"] < lower_band, 1, np.where(data["Close"] > upper_band, -1, 0)
        )
        return data


class MACDSignalCross(BaseStrategy):
    def __init__(self, name="MACD Signal Cross", fast=12, slow=26, signal=9):
        super().__init__(name)
        self.fast = fast
        self.slow = slow
        self.signal = signal

    @classmethod
    def get_parameters(cls) -> dict[str, dict[str, Any]]:
        return {
            "fast": {"type": "int", "default": 12, "min": 1, "max": 50},
            "slow": {"type": "int", "default": 26, "min": 1, "max": 100},
            "signal": {"type": "int", "default": 9, "min": 1, "max": 50},
        }

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()

        ema_fast = data["Close"].ewm(span=self.fast, adjust=False).mean()
        ema_slow = data["Close"].ewm(span=self.slow, adjust=False).mean()

        macd_line = ema_fast - ema_slow
        signal_line = macd_line.ewm(span=self.signal, adjust=False).mean()

        # +1 when MACD crosses above Signal Line, -1 when it crosses below
        data["Signal"] = np.where(
            macd_line > signal_line, 1, np.where(macd_line < signal_line, -1, 0)
        )
        return data


class VolumeBreakout(BaseStrategy):
    def __init__(self, name="Volume Breakout", volume_window=20, volume_multiplier=1.5):
        super().__init__(name)
        self.volume_window = volume_window
        self.volume_multiplier = volume_multiplier

    @classmethod
    def get_parameters(cls) -> dict[str, dict[str, Any]]:
        return {
            "volume_window": {"type": "int", "default": 20, "min": 1, "max": 100},
            "volume_multiplier": {"type": "float", "default": 1.5, "min": 0.5, "max": 5.0},
        }

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()

        avg_volume = data["Volume"].rolling(window=self.volume_window).mean()
        is_volume_spike = data["Volume"] > (avg_volume * self.volume_multiplier)
        is_price_up = data["Close"] > data["Close"].shift(1)
        is_price_down = data["Close"] < data["Close"].shift(1)

        # Buy if high volume AND price goes up. Short if high volume AND price goes down.
        data["Signal"] = np.where(
            is_volume_spike & is_price_up,
            1,
            np.where(is_volume_spike & is_price_down, -1, 0),
        )

        # Carry the previous signal forward if no new breakout occurs (trend riding)
        data["Signal"] = data["Signal"].replace(0, np.nan).ffill().fillna(0)
        return data


class BuyAndHold(BaseStrategy):
    def __init__(self, name="Buy and Hold"):
        super().__init__(name)

    @classmethod
    def get_parameters(cls) -> dict[str, dict[str, Any]]:
        return {}

    def generate_signals(self, df: pd.DataFrame) -> pd.DataFrame:
        data = df.copy()
        # Per checklist instructions: signal is 1 on day one and stays forever
        data["Signal"] = 1
        return data
