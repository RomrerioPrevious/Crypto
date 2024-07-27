from pybit.unified_trading import HTTP
from crypto import Config, Result


class BybitHandler:
    def __init__(self):
        self.config = Config()
        self.session = HTTP(
            testnet=False,
            api_key=self.config["bybit"]["api"],
            api_secret=self.config["bybit"]["secret-key"]
        )

    def parse(self) -> Result:
        ...
