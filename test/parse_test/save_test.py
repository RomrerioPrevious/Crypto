from unittest import TestCase
from crypto import Save


class SaveTest(TestCase):
    save = Save()

    def test_write(self):
        self.save.add("N", 1.0, 1)
        self.save.save_info()

    def test_calc(self):
        x = self.save.calculate_quantity_to_sell("BTCUSDT", 1.0)
        print(x)
