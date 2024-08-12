import asyncio
from unittest import TestCase
from crypto import Config, MainHandler, Result, Action


class MainHandlerTest(TestCase):
    handler = MainHandler()
    config = Config()
    result = Result(
            ai=Action.Buy,
            rsi=Action.Nothing,
            white_bar=Action.Nothing,
            moving_averages=Action.Sell,
            margin_zones=Action.Nothing,
            resistance_waves=Action.Nothing,
            eliot_waves=Action.Nothing,
            support=(1.0, 1.0, 1.0, 1.0),
            rsi_value=0.55,
            short_sma=0.56,
            long_sma=0.83
        )

    def test_calculation_of_action(self):
        action = self.handler.calculation_of_action(self.result)
        assert action == Action.Nothing

    def test_buy(self):
        self.handler.buy("BTCUSDT", self.result)

    def test_sell(self):
        self.handler.sell(
            "BTCUSDT",
            self.result
        )

    def test_log(self):
        self.handler.log(
            result=self.result,
            symbol="BTCUSDT",
            action=Action.Buy,
            cost=100.1
        )

    def test_trade(self):
        asyncio.run(self.handler.trade())
