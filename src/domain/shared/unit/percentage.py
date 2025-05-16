from domain.shared import ValueObject


class Percentage(ValueObject[float]):
    @classmethod
    def from_ratio(cls, ratio: float) -> "Percentage":
        return Percentage(ratio * 100)

    def to_ratio(self) -> float:
        return float(self)

    def __float__(self) -> float:
        return self.value / 100

    def __str__(self) -> str:
        return format(self.to_ratio(), ".1%")

    def __format__(self, format_spec: str) -> str:
        return format(self.value, format_spec)
