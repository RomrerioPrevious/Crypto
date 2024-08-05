from unittest import TestCase
from crypto import Config, MainHandler, Result, Action


class MainHandlerTest(TestCase):
    handler = MainHandler()
    config = Config()

    def test_calculation_of_action(self):
        result = Result(
            ai=Action.Buy,
            rsi=Action.Nothing,
            white_bar=Action.Nothing,
            moving_averages=Action.Sell,
            margin_zones=Action.Nothing,
            resistance_waves=Action.Nothing,
            eliot_waves=Action.Nothing,
            support=(1.0, 1.0),
        )
        action = self.handler.calculation_of_action(result)
        assert action == Action.Nothing

    def test_buy(self):
        self.handler.buy("BTCUSDT")

    def test_sell(self):
        self.handler.sell(
            symbol="BTCUSDT"
        )