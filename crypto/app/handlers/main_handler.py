from .ai_handler import AiHandler
from .bybit_handler import BybitHandler
from ..config import Config, Logger
from ..models import Result, Action


class MainHandler:
    def __init__(self):
        self.config = Config()
        self.bybit_handler = BybitHandler()
        self.ai_handler = AiHandler()

    def parse(self):
        symbols = self.config["bybit"]["symbols"].split(";")
        results = []

        for symbol in symbols:
            bybit = self.bybit_handler.parse(symbol=symbol)
            ai = self.ai_handler.parse(symbol=symbol)
            try:
                result = bybit + ai
                self.make_action(result)
            except TypeError as er:
                Logger.write_error(er)

    def make_action(self, result: Result) -> Action:
        ...

    def buy(self):
        ...

    def sell(self):
        ...