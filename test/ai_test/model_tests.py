from unittest import TestCase
from crypto import AiHandler, Config


class ModelTests(TestCase):
    config = Config()
    handler = AiHandler()

    def test_parse(self):
        action = self.handler.parse("BTCUSDT")
        print(action)
