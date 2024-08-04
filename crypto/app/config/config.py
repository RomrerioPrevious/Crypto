from configparser import ConfigParser
import os


class Config:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            parser = ConfigParser()
            dir_path = Config.find_config_path()
            parser.read(dir_path, encoding="UTF-8")
            cls.instance = parser
        return cls.instance

    @staticmethod
    def find_config_path():
        return f"{Config.find_global_path()}resources\\\\config.ini"

    @staticmethod
    def find_global_path():
        dir_path = os.path.dirname(os.path.realpath(__file__))
        dir_path = dir_path.removesuffix("app\\\\config")
        dir_path = dir_path.removesuffix("app\\config")
        return dir_path