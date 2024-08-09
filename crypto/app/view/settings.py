from textual.containers import VerticalScroll, Container, Horizontal
from textual.widgets import Label, Input
from ..config import Config


class Settings(VerticalScroll):
    def compose(self):
        config = Config()

        yield Label("bybit")
        with Container(id="bybit"):
            with Horizontal():
                yield Input(id="api",
                            placeholder="api",
                            value=config["bybit"]["api"])
                yield Input(id="secret-key",
                            placeholder="secret key",
                            value=config["bybit"]["secret-key"])
            with Horizontal():
                yield Input(id="symbols",
                            placeholder="symbols",
                            value=config["bybit"]["symbols"])
        yield Label("strategies")
        with Container(id="strategies"):
            with Horizontal():
                yield Input(id="oversold_threshold",
                            placeholder="oversold threshold",
                            value=config["strategies"]["oversold_threshold"])
                yield Input(id="overbought_threshold",
                            placeholder="overbought threshold",
                            value=config["strategies"]["overbought_threshold"])
            with Horizontal():
                yield Input(id="long_ma",
                            placeholder="long_ma",
                            value=config["strategies"]["long_ma"])
                yield Input(id="short_ma",
                            placeholder="short_ma",
                            value=config["strategies"]["short_ma"])
        yield Label("price")
        with Container(id="price"):
            with Horizontal():
                yield Input(id="buy_coefficient",
                            placeholder="buy coefficient",
                            value=config["price"]["buy_coefficient"])
                yield Input(id="sell_coefficient",
                            placeholder="sell coefficient",
                            value=config["price"]["sell_coefficient"])
            with Horizontal():
                yield Input(id="max_price",
                            placeholder="max price",
                            value=config["price"]["max_price"])
        yield Label("coefficients")
        with Container(id="coefficients"):
            with Horizontal():
                yield Input(id="rsi",
                            placeholder="rsi",
                            value=config["coefficients"]["rsi"])
                yield Input(id="white_bar",
                            placeholder="white bar",
                            value=config["coefficients"]["white_bar"])
            with Horizontal():
                yield Input(id="moving_averages",
                            placeholder="moving averages",
                            value=config["coefficients"]["moving_averages"])
                yield Input(id="margin_zones",
                            placeholder="margin zones",
                            value=config["coefficients"]["margin_zones"])
            with Horizontal():
                yield Input(id="resistance_waves",
                            placeholder="resistance waves",
                            value=config["coefficients"]["resistance_waves"])
                yield Input(id="eliot_waves",
                            placeholder="eliot waves",
                            value=config["coefficients"]["eliot_waves"])
            with Horizontal():
                yield Input(id="ai",
                            placeholder="ai",
                            value=config["coefficients"]["ai"])
