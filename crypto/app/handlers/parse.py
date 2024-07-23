import bybit
from crypto import Config


class Parser:
    def __init__(self):
        self.config = Config()
        self.client = bybit.bybit(
            test=False,
            api_key=self.config["bybit"]["api"],
            api_secret=self.config["bybit"]["secret-key"]
        )

    def parse(self):
        ...
