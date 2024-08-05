import numpy as np
from stable_baselines3.common.env_util import make_vec_env
from pybit.unified_trading import HTTP
from ..models import Action
from ..config import Config
from pandas import DataFrame
from stable_baselines3 import A2C


class AiHandler:
    def __init__(self):
        self.config = Config()
        self.model = A2C.load(f"{Config.find_global_path()}resources\\model.h5")
        self.env = make_vec_env("CartPole-v1", n_envs=1000)
        self.client = HTTP(
            testnet=False,
            api_key=self.config["bybit"]["api"],
            api_secret=self.config["bybit"]["secret-key"]
        )

    def parse(self, symbol: str, interval: str = "1") -> Action:
        response = self.client.get_kline(
            category="linear",
            symbol=symbol,
            interval=interval,
            limit=1000,
        )

        klines = response.get("result", {}).get("list", [])
        klines = sorted(klines, key=lambda x: int(x[0]))
        klines = DataFrame(klines)

        klines_last_5 = klines.tail(5)
        klines_data = klines_last_5[[1, 2, 3]].values.astype(np.float32)
        obs = klines_data.reshape((1, 5, 3))

        action, _states = self.model.predict(obs)

        if action[0] == 0:
            return Action.Buy
        if action[0] == 1:
            return Action.Sell
        return Action.Nothing
