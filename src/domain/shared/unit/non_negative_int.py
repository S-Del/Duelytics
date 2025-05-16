from domain.shared import ValueObject


class NonNegativeInt(ValueObject[int]):
    def validate(self, value: int):
        if value < 0:
            raise ValueError(f"渡された値が負数: {value}")

    def __int__(self) -> int:
        return self.value
