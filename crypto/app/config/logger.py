import datetime
from icecream import ic


class Logger:
    @staticmethod
    async def info() -> str:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"info {time} | "

    @staticmethod
    async def error() -> str:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"error {time} | "

    @staticmethod
    async def custom(debug: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{debug} {time}| "

    @staticmethod
    async def write_error(error: str | BaseException):
        ic.prefix = Logger.error()
        ic(error)
        ic.prefix = Logger.info()

    @staticmethod
    async def write_log(log: str):
        with open("logs.log", "a", encoding="UTF-8") as file:
            file.write(log + "\n")

    @staticmethod
    async def clear():
        with open("logs.log", "w", encoding="UTF-8") as file:
            file.write("")