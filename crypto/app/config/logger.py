import datetime
from icecream import ic


class Logger:
    @staticmethod
    def info() -> str:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{time} info | "

    @staticmethod
    def error() -> str:
        time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{time} error | "

    @staticmethod
    def custom(debug: str):
        time = datetime.datetime.now().strftime("%H:%M:%S")
        return f"{time} {debug} | "

    @staticmethod
    def write_error(error: str | BaseException):
        ic.prefix = Logger.error()
        ic(error)
        ic.prefix = Logger.info()

    @staticmethod
    def write_log(log: str):
        with open("logs.log", "a", encoding="UTF-8") as file:
            file.write(log + "\n")

    @staticmethod
    def clear():
        with open("logs.log", "w", encoding="UTF-8") as file:
            file.write("")