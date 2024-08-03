from unittest import TestCase
from crypto.app.ai import *


class ConfigTest(TestCase):
    def test_train(self):
        train_bot(symbol="BTCUSDT",
                  leverage=1,
                  timeframe_to_trade="",
                  csv_train="D:\\Save\\Crypto\\crypto\\resources\\dataset.csv",
                  window_size=5,
                  initial_balance=10000,
                  episodes=5
                  )
