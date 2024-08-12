import datetime
from time import sleep
from .indicators import Indecators
import pandas as pd
from icecream import ic
from .ai_handler import AiHandler
from .bybit_handler import BybitHandler
from ..config import Config, Logger
from ..models import Result, Action
from pybit.unified_trading import HTTP
import operator


class MainHandler:
    def __init__(self):
        self.config = Config()
        self.bybit_handler = BybitHandler()
        self.ai_handler = AiHandler()
        self.client = self.client = HTTP(
            testnet=False,
            api_key=str(self.config["bybit"]["api"]),
            api_secret=str(self.config["bybit"]["secret-key"])
        )

    async def trade(self):
        while True:
            symbols = self.config["bybit"]["symbols"].split()

            for symbol in symbols:
                try:
                    result = await self.parse(symbol)

                    if not result:
                        continue

                    try:
                        config = Config()["coefficients"]

                        actions = {
                            Action.Buy: 0,
                            Action.Sell: 0,
                            Action.Nothing: 0
                        }

                        actions[result.ai] += float(config["ai"])
                        actions[result.rsi] += float(config["rsi"])
                        actions[result.white_bar] += float(config["white_bar"])
                        actions[result.moving_averages] += float(config["moving_averages"])
                        actions[result.margin_zones] += float(config["margin_zones"])
                        actions[result.resistance_waves] += float(config["resistance_waves"])
                        actions[result.eliot_waves] += float(config["eliot_waves"])
                    except BaseException as err:
                        await Logger.write_error(err)
                        actions = {None: 1}

                    action = max(actions.items(), key=operator.itemgetter(1))[0]
                    if action is None:
                        action = Action.Nothing

                    match action:
                        case Action.Buy:
                            self.buy(symbol, result)
                        case Action.Sell:
                            self.sell(symbol, result)
                except BaseException as ex:
                    ...

            sleep(5)

    async def parse(self, symbol: str) -> Result | None:
        result = self.bybit_handler.parse(symbol=symbol)
        result.ai = self.ai_handler.parse(symbol=symbol)
        return result

    def buy(self, symbol: str, result: Result) -> float | None:
        response = self.client.get_orderbook(
            category="spot",
            symbol=symbol,
            limit=50).get("result")

        price = float(response["a"][0][0])
        coef = float(Config()["price"]["buy_coefficient"])
        if price >= float(self.config["price"]["max_price"]):
            return

        self.client.place_order(
            category="spot",
            symbol=symbol,
            orderType="Market",
            side="Buy",
            qty="1",
            price=price * coef,
        )
        self.log(
            result=result,
            action=Action.Buy,
            symbol=symbol,
            cost=price * coef
        )

    def sell(self, symbol: str, result: Result) -> None:
        response = self.client.get_orderbook(
            category="spot",
            symbol=symbol,
            limit=50).get("result")

        price = float(response["a"][0][0])
        coef = float(Config()["price"]["sell_coefficient"])

        self.client.place_order(
            category="spot",
            symbol=symbol,
            orderType="Market",
            side="Sell",
            qty="1",
            price=price * coef,
        )
        self.log(
            result=result,
            action=Action.Sell,
            symbol=symbol,
            cost=price * coef
        )

    def log(self, result: Result, action: Action, symbol: str, cost: float) -> None:
        if action == Action.Nothing:
            return

        data = [
            datetime.datetime.now().strftime("%y/%m/%d/%H:%M"),
            str(action),
            symbol,
            str(cost),
            str(result.rsi_value),
            str(result.short_sma),
            str(result.long_sma),
            str(result.support[0]),
            str(result.support[1]),
            str(result.support[2]),
            str(result.support[3])
        ]

        with open(f"{Config.find_global_path()}resources\\trading_operations.csv", "a", encoding="UTF-8") as file:
            data = ",".join(data)
            file.write(f"{data}\n")
