from abc import ABC
from typing import Optional
import gym
import numpy as np
import pandas as pd
from pandas import DataFrame
from ..models import Action
from crypto.app.handlers.indicators import Indecators


class TradingEnvironment(gym.Env, ABC):
    def __init__(self, data: DataFrame, window_size: int, initial_balance: int, leverage: int):
        super(TradingEnvironment, self).__init__()

        self.data = data
        self.window_size = window_size
        self.initial_balance = initial_balance
        self.leverage = leverage

        self.balance = self.initial_balance
        self.position = None
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.current_step = self.window_size
        self.balance_history = []
        self.reward = 0

        self.action_space = gym.spaces.Discrete(8)  # Increased from 6 to 8 actions
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(window_size, 10), dtype=np.float32)

        # Calculate indicators
        state = self.data.iloc[self.current_step - self.window_size: self.current_step].copy()
        state["moving_average"] = Indecators.moving_average(state["close"], window=14)
        state["rsi"] = Indecators.calculate_rsi(state["close"], period=14)
        state["volume_pct_change"] = Indecators.volume_pct_change(state["volume"])
        state["resistance"], state["support"] = self.find_support_resistance_levels(self.data)

        self.data["ma"] = Indecators.moving_average(self.data["close"])
        self.data["rsi"] = Indecators.calculate_rsi(self.data["close"])
        self.data["volume_pct_change"] = Indecators.volume_pct_change(self.data["volume"])
        self.data["resistance"], self.data["support"] = self.find_support_resistance_levels(self.data)

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        self.balance = self.initial_balance
        self.position = None
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.current_step = self.window_size
        self.balance_history = []

        state = self.data.iloc[self.current_step - self.window_size: self.current_step].copy()
        state["moving_average"] = Indecators.moving_average(state["close"], window=14)
        state["rsi"] = Indecators.calculate_rsi(state["close"], period=14)
        state["volume_pct_change"] = Indecators.volume_pct_change(state["volume"])
        state["resistance"], state["support"] = self.find_support_resistance_levels(self.data)

        return state.values

    def step(self, action: Action):
        self.current_step += 1
        self.reward = 0
        done = False
        current_price = self.data.iloc[self.current_step]["close"]

        self.make_action(action, current_price)

        if self.position is not None:
            if (self.position > 0 and (current_price <= self.stop_loss or current_price >= self.take_profit)) or \
                    (self.position < 0 and (current_price >= self.stop_loss or current_price <= self.take_profit)):
                if self.position > 0:
                    sell_price = current_price
                    self.reward = (sell_price - self.position) * self.leverage
                else:
                    buy_price = current_price
                    self.reward = (self.entry_price - buy_price) * self.leverage
                self.save_balance()

        if self.balance <= 0:
            self.reward = -1000  # You can adjust the penalty value based on your preferences
            done = True
        # Calculate the reward as the change in account balance
        if len(self.balance_history) > 0:
            self.reward = self.balance - self.balance_history[-1]
        else:
            self.reward = 0

        state = self.data.iloc[self.current_step - self.window_size: self.current_step].copy()
        state["moving_average"] = Indecators.moving_average(state["close"], window=14)
        state["rsi"] = Indecators.calculate_rsi(state["close"], period=14)
        state["volume_pct_change"] = Indecators.volume_pct_change(state["volume"])
        state["resistance"], state["support"] = Indecators.find_support_resistance_levels(self.data)

        return state.values, self.reward, done, dict()

    def make_action(self, action, current_price):
        match action:
            case Action.Buy:
                self.buy(current_price)
            case Action.Hold:
                self.hold()
            case Action.Close_Long_Position:
                self.close_long_position(current_price)
            case Action.Scale_Up:
                self.scale_up(current_price)
            case Action.Adjust_Stop_Loss:
                self.adjust_stop_loss(current_price)
            case Action.Adjust_Take_Profit:
                self.adjust_take_profit(current_price)
            case Action.Open_Short_Position:
                self.open_short_position(current_price)
            case Action.Close_Short_Position:
                self.close_short_position(current_price)

    def buy(self, current_price: float):
        if self.position is None:
            self.entry_price = current_price
            self.position = self.entry_price
            self.stop_loss = self.entry_price * (1 - (0.05 / self.leverage))
            self.take_profit = self.entry_price * 1.05
            self.reward += self.initial_balance / (self.balance + 1)

    def open_short_position(self, current_price: float):
        if self.position is None:
            self.entry_price = current_price
            self.position = -self.entry_price  # Short position represented by a negative value
            self.stop_loss = self.entry_price * (1 + (0.05 / self.leverage))
            self.take_profit = self.entry_price * 0.95
            self.reward += self.initial_balance / (self.balance + 1)

    def hold(self):
        if self.position is not None:
            self.reward = -2  # Small penalty for holding a position

    def adjust_take_profit(self, current_price: float):
        if self.position is not None:
            self.take_profit = current_price * 1.05

    def adjust_stop_loss(self, current_price: float):
        if self.position is not None:
            self.stop_loss = current_price * (1 - (0.05 / self.leverage))

    def scale_up(self, current_price: float):
        if self.position is not None:
            profit = current_price - self.entry_price
            if profit > 0:
                self.entry_price = current_price
                self.stop_loss = self.entry_price * (1 - (0.05 / self.leverage))

    def close_short_position(self, current_price: float):
        if self.position is not None and self.position < 0:  # Check if there"s a short position
            buy_price = current_price
            self.reward = (self.entry_price - buy_price) * self.leverage
            self.save_balance()

    def close_long_position(self, current_price: float):
        if self.position is not None and self.position > 0:  # Check if there"s a long position
            self.reward = (current_price - self.position) * self.leverage
            self.save_balance()

    def save_balance(self):
        self.balance += self.reward
        self.position = None
        self.entry_price = None
        self.stop_loss = None
        self.take_profit = None
        self.balance_history.append(self.balance)

    @staticmethod
    def find_support_resistance_levels(data: DataFrame, window=14, tolerance=0.02) -> (pd.Series, pd.Series):
        high = data["close"]
        pivot_highs = pd.Series(
            np.where(high
                     .rolling(window=window).
                     max().
                     shift(-window + 1) == high, high, np.nan),
            index=data.index)
        low = data["low"]
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
