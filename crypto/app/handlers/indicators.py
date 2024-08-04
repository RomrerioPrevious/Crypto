import numpy as np
import pandas as pd
from pandas import DataFrame
from ..models import Action
from ..config import Config


class Indecators:
    @staticmethod
    def moving_average(data: DataFrame, window=14):
        return data.rolling(window=window).mean()

    @staticmethod
    def calculate_rsi(data: DataFrame, period=14) -> DataFrame:
        delta = data.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    @staticmethod
    def volume_pct_change(data: DataFrame):
        return data.pct_change()

    @staticmethod
    def find_support_resistance_levels(data: DataFrame, window=14, tolerance=0.02) -> (pd.Series, pd.Series):
        high = data[2]
        pivot_highs = pd.Series(
            np.where(high
                     .rolling(window=window).
                     max().
                     shift(-window + 1) == high, high, np.nan),
            index=data.index)
        low = data[3]
        pivot_lows = pd.Series(
            np.where(low
                     .rolling(window=window)
                     .min()
                     .shift(-window + 1) == low, low, np.nan),
            index=data.index)

        pivot_highs = pivot_highs[pivot_highs.notnull()].copy()
        pivot_lows = pivot_lows[pivot_lows.notnull()].copy()

        for i, val in enumerate(pivot_highs):
            if i == 0:
                continue
            if val - pivot_highs[i - 1] <= pivot_highs[i - 1] * tolerance:
                pivot_highs.iloc[i] = np.nan

        for i, val in enumerate(pivot_lows):
            if i == 0:
                continue
            if pivot_lows[i - 1] - val <= val * tolerance:
                pivot_lows.iloc[i] = np.nan

        pivot_highs = pivot_highs[pivot_highs.notnull()]
        pivot_lows = pivot_lows[pivot_lows.notnull()]

        return pivot_highs, pivot_lows

    @staticmethod
    def find_support_resistance(data: DataFrame, window: int = 14) -> (float, float):
        highs = data[2].rolling(window=window).max()
        lows = data[3].rolling(window=window).min()
        return highs.iloc[-1], lows.iloc[-1]

    @staticmethod
    def is_white_bar(data: DataFrame) -> bool:
        close = data[4].iloc[-1]
        open = data[1].iloc[-1]
        return close > open

    @staticmethod
    def calculate_sma(data: DataFrame, period: str) -> DataFrame:
        close = data[4]
        sma = close.rolling(window=int(period)).mean()
        return sma


class Strategies:
    @staticmethod
    def margin_zones_strategy(data: DataFrame, highs: float, lows: float) -> Action | None:
        close = round(float(data[4].iloc[-1]), 2)
        if close < lows:
            return Action.Buy
        elif close > highs:
            return Action.Sell
        else:
            return Action.Nothing

    @staticmethod
    def resistance_waves_strategy(data: DataFrame, highs: float) -> Action | None:
        close = round(float(data[4].iloc[-1]), 2)
        if close > highs:
            return Action.Sell
        else:
            return Action.Nothing

    @staticmethod
    def eliot_waves_strategy(data: DataFrame, highs: float, lows: float, wave_length: int) -> Action | None:
        close = data[4]

        if len(data) < 5 * wave_length:
            return Action.Nothing

        wave_types = []
        for i in range(0, len(data), wave_length):
            if i + wave_length >= len(data):
                break
            if close.iloc[i + wave_length] > close.iloc[i]:
                wave_types.append(1)  # Up
            else:
                wave_types.append(-1)  # Down

        if len(wave_types) < 5:
            return Action.Nothing
        if wave_types[0] == wave_types[1] or wave_types[1] == wave_types[2] or \
                wave_types[2] == wave_types[3] or wave_types[3] == wave_types[4]:
            return Action.Nothing

        corrective_wave = Strategies._find_corrective_wave(data, wave_length, 5 * wave_length, len(data))
        if not corrective_wave:
            return Action.Nothing

        if close.iloc[-1] > highs:
            return Action.Sell
        elif close.iloc[-1] < lows:
            return Action.Buy
        return Action.Nothing

    @staticmethod
    def _find_corrective_wave(data: DataFrame, wave_length: int, start_index: int, end_index: int) -> list | None:
        if end_index - start_index < 3 * wave_length:
            return None

        close = data[4]
        wave_types = []
        for i in range(start_index, end_index, wave_length):
            if i + wave_length > end_index:
                break
            if close.iloc[i + wave_length] > close.iloc[i]:
                wave_types.append(1)  # Up
            else:
                wave_types.append(-1)  # Down

        if len(wave_types) < 3:
            return None
        if wave_types[0] == wave_types[1] or wave_types[1] == wave_types[2]:
            return None

        return wave_types

    @staticmethod
    def rsi_strategy(rsi: float) -> Action | None:
        oversold_threshold = float(Config()["strategies"]["oversold_threshold"])
        overbought_threshold = float(Config()["strategies"]["overbought_threshold"])
        if rsi < oversold_threshold:
            return Action.Buy
        elif rsi > overbought_threshold:
            return Action.Sell
        else:
            return Action.Nothing

    @staticmethod
    def white_bar_strategy(date: DataFrame) -> Action | None:
        close = date[4]
        open = date[1]
        if close.iloc[-2] < open.iloc[-2]:
            if close.iloc[-1] > open.iloc[-1]:
                return Action.Buy
        elif close.iloc[-2] > open.iloc[-2]:
            if close.iloc[-1] < open.iloc[-1]:
                return Action.Sell
        else:
            return Action.Nothing

    @staticmethod
    def moving_averages_strategy(short_ma, long_ma) -> Action | None:
        if short_ma.iloc[-1] > long_ma.iloc[-1] and short_ma.iloc[-2] < long_ma.iloc[-2]:
            return Action.Buy
        elif short_ma.iloc[-1] < long_ma.iloc[-1] and short_ma.iloc[-2] > long_ma.iloc[-2]:
            return Action.Sell
        else:
            return Action.Nothing
