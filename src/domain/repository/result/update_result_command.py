from dataclasses import dataclass
from uuid import UUID

from domain.model.result import FirstOrSecond, ResultChar

@dataclass(frozen=True)
class UpdateResultCommand:
    id: UUID
    first_or_second: FirstOrSecond
    result: ResultChar
    my_deck_name: str
    opponent_deck_name: str
