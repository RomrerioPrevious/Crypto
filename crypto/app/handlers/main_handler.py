import datetime
import pandas as pd
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
            testnet=True,  # TODO
            api_key=self.config["bybit"]["api"],
            api_secret=self.config["bybit"]["secret-key"]
        )

    def trade(self):
        symbols = self.config["bybit"]["symbols"].split()

        for symbol in symbols:
            result = self.parse(symbol)

            if not result:
                continue

            action = self.calculation_of_action(result)
            match action:
                case Action.Buy:
                    self.buy(symbol)
                case Action.Sell:
                    self.sell(symbol)

            self.log(
                result=result,
                action=action,
                symbol=symbol
            )

    def calculation_of_action(self, result) -> Action:
        actions = {
            Action.Buy: 0,
            Action.Sell: 0,
            Action.Nothing: 0
        }

        actions[result.ai] += 0.4
        actions[result.rsi] += 0.1
        actions[result.white_bar] += 0.1
        actions[result.moving_averages] += 0.1
        actions[result.margin_zones] += 0.1
        actions[result.resistance_waves] += 0.1
        actions[result.eliot_waves] += 0.1

        action = max(actions.items(), key=operator.itemgetter(1))[0]
        if action is None:
            action = Action.Nothing
        return action

    def parse(self, symbol: str) -> Result | None:
        bybit = self.bybit_handler.parse(symbol=symbol)
        ai = self.ai_handler.parse(symbol=symbol)
        try:
            result = bybit + ai
            return result
        except TypeError as er:
            Logger.write_error(er)
            return None

    def buy(self, symbol: str) -> None:
        self.client.place_order(
            category="linear",
            symbol=symbol,
            orderType="Market",
            side="Buy"
        )

    def sell(self, symbol: str) -> None:
        response = self.client.get_orderbook(
            category="linear",
            symbol=symbol,
            limit=50).get("result")

        if not response:  # TODO
            ...

        self.client.place_order(
            category="linear",
            symbol=symbol,
            orderType="Market",
            side="Sell",
            positionIdx=2
        )

    def log(self, result: Result, action: Action, symbol: str) -> None:
        if action == Action.Nothing:
            return

        data = {  # TODO
            "date": datetime.datetime,
            "operation": str(action),
            "currency": symbol,
            "cost": 0,
            "quantity": 0,
            "moving_averages": 0,
            "margin_zones": 0,
            "resistance_waves": 0,
            "eliot_waves": 0,
            "support_highs": 0,
            "support_lows": 0,
            "open": result.support[0],
            "close": result.support[1]
        }

        data = pd.DataFrame(data)

        with open(f"{Config.find_global_path()}resources\\trading_operations.csv", "a", encoding="UTF-8") as file:
            file.write(data.to_csv())

