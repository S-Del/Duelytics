from enum import Enum


class ResultChar(Enum):
    WIN = 'W'
    LOSS = 'L'
    DRAW = 'D'


class ResultStringJP(Enum):
    W = "勝利"
    L = "敗北"
    D = "引分"
