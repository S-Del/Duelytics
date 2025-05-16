from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class ColumnNames:
    NAME: ClassVar[str] = "name"


@dataclass(frozen=True)
class DeckTableConfig:
    TABLE_NAME: ClassVar[str] = "decks"
    COLUMN_NAMES: ClassVar[ColumnNames] = ColumnNames()
