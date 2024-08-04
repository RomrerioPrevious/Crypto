from enum import Enum


class Action(Enum):
    Buy = 0
    Hold = 1
    Close_Long_Position = 2
    Scale_Up = 3
    Adjust_Stop_Loss = 4
    Adjust_Take_Profit = 5
    Open_Short_Position = 6
    Close_Short_Position = 7
    Sell = 8
    Nothing = 9
