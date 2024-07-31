from unittest import TestCase
from crypto import Config, BybitHandler
import pandas as pd


class BybitTest(TestCase):
    bybit = BybitHandler()
    config = Config()

    def test_parse(self):
        result = self.bybit.parse(
            symbol=self.config["bybit"]["symbols"],
        )
        print(result)
