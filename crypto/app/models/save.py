from math import floor
from crypto.app import Config
import json


class Save:
    def __init__(self):
        self.config = Config()
        path = f"{Config.find_global_path()}resources\\save.json"
        with open(path, encoding="UTF-8") as file:
            self.save = dict(json.load(file))

    def add(self, symbol: str, price: float, quantity: int):
        if symbol not in self.save.keys():
            self.save[symbol] = []
        self.save[symbol].append({"price": price, "quantity": quantity})

    def calculate_quantity_to_buy(self, symbol: str, price: float) -> int:  # TODO
        max_price = float(self.config["bybit"]["max_price"]) / 2
        return floor(max_price / price)

    def calculate_quantity_to_sell(self, symbol: str, price: float) -> int:
        if symbol not in self.save.keys():
            return 1

        data = self.save[symbol]
        ids = []
        quantity = 0
        for n, i in enumerate(data):
            if i["price"] < price:
                continue
            quantity += i["quantity"]
            ids.append(n)

        for n, id in enumerate(ids):
            del self.save[symbol][id - n]

        self.save_info()

        return quantity

    def save_info(self):
        path = f"{Config.find_global_path()}resources\\save.json"
        with open(path, "w", encoding="UTF-8") as file:
            json.dump(self.save, file)
