import asyncio
from textual import on
from textual.app import App, ComposeResult
from textual.containers import *
from textual.widgets import Header, Footer, Input, Button
from .app.view import *
from icecream import ic
from crypto import MainHandler, Config


class CryptoApp(App):
    BINDINGS = [("ctrl+d", "toggle_dark", "Theme"),
                ("ctrl+s", "save", "Save")]
    CSS_PATH = "resources/index.tcss"
    task = None

    def compose(self) -> ComposeResult:
        yield Header(name="Crypto")
        with Center(id="config"):
            yield Settings(id="settings")
        with Horizontal(id="buttons"):
            yield Button(id="save",
                         label="save")
            yield Button(id="start",
                         label="start")
        yield Footer()

    @on(Button.Pressed, "#start")
    def action_start(self):
        handler = MainHandler()

        self.task = asyncio.create_task(handler.trade())

        buttons = self.query_one("#buttons", Horizontal)
        self.query_one("#start").remove()
        new_button = Button(
            id="stop",
            label="stop"
        )
        buttons.mount(new_button)

    @on(Button.Pressed, "#stop")
    async def action_stop(self):
        self.task.cancel()

        buttons = self.query_one("#buttons", Horizontal)
        await self.query_one("#stop").remove()
        new_button = Button(
            id="start",
            label="start"
        )
        await buttons.mount(new_button)

    @on(Button.Pressed, "#save")
    async def action_save(self):
        config = Config()
        await self.save_block(
            section="bybit",
            fields=["api", "secret-key", "symbols"]
        )
        await self.save_block(
            section="strategies",
            fields=["oversold_threshold", "overbought_threshold", "long_ma", "short_ma"]
        )
        await self.save_block(
            section="price",
            fields=["max_price", "buy_coefficient", "sell_coefficient"]
        )
        await self.save_block(
            section="coefficients",
            fields=["rsi", "white_bar", "moving_averages", "margin_zones", "resistance_waves", "eliot_waves"]
        )

        with open(Config.find_config_path(), "w", encoding="UTF-8") as file:
            config.write(file)

    async def save_block(self, fields: [str], section: str):
        config = Config()
        block = self.query_one(f"#{section}")
        for i in fields:
            value = block.query_one(f"#{i}", Input).value
            config[section][i] = value

    async def action_toggle_dark(self) -> None:
        self.dark = not self.dark
