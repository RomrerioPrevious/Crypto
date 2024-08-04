from pybit.unified_trading import HTTP
from ..config import Config
from ..models import Result
from .indicators import *
import numpy as np
import pandas as pd


class BybitHandler:
    def __init__(self):
        self.config = Config()
        self.client = HTTP(
            testnet=False,
            api_key=self.config["bybit"]["api"],
            api_secret=self.config["bybit"]["secret-key"]
        )

    def parse(self, symbol: str, interval: str = "1") -> Result:
        response = self.client.get_kline(
            category="linear",
            symbol=symbol,
            interval=interval,
            limit=1000,
        )

        klines = response.get("result", {}).get("list", [])
        klines = sorted(klines, key=lambda x: int(x[0]))
        klines = DataFrame(klines)

        close_prices = []

        for candle in klines.values:
            close_price_for_list = float(candle[4])
            close_prices.append(close_price_for_list)

        close_prices = np.array(close_prices, dtype="float")
        close_prices = pd.DataFrame(close_prices)

        rsi = Strategies.rsi_strategy(rsi=round(float(Indecators.calculate_rsi(close_prices).values[-1]), 2))
        white_bar = Strategies.white_bar_strategy(date=klines)
        moving_averages = Strategies.moving_averages_strategy(
            short_ma=Indecators.calculate_sma(klines, Config()["strategies"]["short_ma"]),
            long_ma=Indecators.calculate_sma(klines, Config()["strategies"]["long_ma"]))
        highs, lows = Indecators.find_support_resistance(klines)
        margin_zones = Strategies.margin_zones_strategy(data=klines,
                                                        highs=highs,
                                                        lows=lows)
        resistance_waves = Strategies.resistance_waves_strategy(data=klines,
                                                                highs=highs)
        eliot_waves = Strategies.eliot_waves_strategy(data=klines,
                                                      highs=highs,
                                                      lows=lows,
                                                      wave_length=10)

        return Result(
            ai=None,
            rsi=rsi,
            white_bar=white_bar,
            moving_averages=moving_averages,
            margin_zones=margin_zones,
            resistance_waves=resistance_waves,
            eliot_waves=eliot_waves,
            support=(highs, lows)
        )
