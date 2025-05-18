from domain.shared import ValueObject


class PositiveInt(ValueObject[int]):
    def validate(self, value: int):
        if value < 1:
            raise ValueError(f"渡された値が 1 未満")

    def __int__(self) -> int:
        return self.value
