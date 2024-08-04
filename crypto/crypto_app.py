from time import sleep

from textual.app import App, ComposeResult
from textual.containers import *
from textual.widgets import Header, Footer, Input, Button, Static, Label
from icecream import ic

from crypto import MainHandler, Config


class CryptoApp(App):
    BINDINGS = [("ctrl+d", "toggle_dark", "Theme"),
                ("ctrl+t", "train", "Train"),
                ("ctrl+s", "save", "Save"),
                ("ctrl+r", "start", "Start")]
    CSS_PATH = "resources/index.tcss"

    def compose(self) -> ComposeResult:
        config = Config()

        yield Header(name="Valuer")
        with Center(id="config"):
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
        with Horizontal(id="buttons"):
            yield Button(id="training",
                         label="training")
            yield Button(id="start",
                         label="start")
        yield Footer()

    def action_start(self):
        handler = MainHandler()
        while True:
            handler.trade()
            sleep(60)

    def action_save(self):
        config = Config()
        bybit_values = [
            "api",
            "secret-key",
            "symbols"
        ]
        strategies_values = [
            "oversold_threshold",
            "overbought_threshold",
            "long_ma",
            "short_ma"
        ]
        bybit = self.query_one(f"#bybit")
        for i in bybit_values:
            value = bybit.query_one(f"#{i}", Input).value
            config["bybit"][i] = value

        strategies = self.query_one(f"#strategies")
        for i in strategies_values:
            value = strategies.query_one(f"#{i}", Input).value
            config["strategies"][i] = value

        with open(Config.find_config_path(), "w", encoding="UTF-8") as file:
            config.write(file)

    def action_toggle_dark(self) -> None:
        self.dark = not self.dark
