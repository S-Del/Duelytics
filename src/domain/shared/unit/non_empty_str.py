from domain.shared import ValueObject


class NonEmptyStr(ValueObject[str]):
    def validate(self, value: str):
        if not value.strip():
            raise ValueError(f"渡された値が空")

    def __str__(self) -> str:
        return self.value
