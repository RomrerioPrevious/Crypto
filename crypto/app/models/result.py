from dataclasses import dataclass

from ..models import Action


@dataclass
class Result:
    ai: bool
    rsi: Action
    white_bar: Action
    moving_averages: Action
    margin_zones: Action
    resistance_waves: Action
    eliot_waves: Action
    support: (float, float)

    @staticmethod
    def create_empty():
        return Result(None, None, None, None, None, None, None, None)

    def __add__(self, other):  # TODO new add
        if isinstance(other, Result):
            result = Result.create_empty()
            result.ai = other.ai or self.ai
            result.rsi = other.rsi, self.rsi
            result.white_bar = other.white_bar or self.white_bar

            result.moving_averages = self.moving_averages
            if other.moving_averages:
                result.moving_averages = other.moving_averages

            result.eliot_waves = self.eliot_waves
            if other.eliot_waves:
                result.eliot_waves = other.eliot_waves

            result.margin_zones = self.margin_zones
            if other.margin_zones:
                result.margin_zones = other.margin_zones

            result.resistance_waves = self.resistance_waves
            if other.resistance_waves:
                result.resistance_waves = other.resistance_waves

            return result
        else:
            raise TypeError
