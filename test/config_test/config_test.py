from unittest import TestCase
from crypto import Config


class ConfigTest(TestCase):
    config = Config()

    def test_get(self):
        result = self.config["test"]["test"]
        assert result == "1.0"
