from dataclasses import dataclass
from typing import ClassVar


TABLE_NAME = "results"


@dataclass(frozen=True)
class ColumnNames:
    ID: ClassVar[str] = "id"
    REGISTER_DATE: ClassVar[str] = "registered_at"
    FIRST_OR_SECOND: ClassVar[str] = "first_or_second"
    RESULT: ClassVar[str] = "result"
    MY_DECK_NAME: ClassVar[str] = "my_deck_name"
    OPPONENT_DECK_NAME: ClassVar[str] = "opponent_deck_name"


@dataclass(frozen=True)
class IndexNames:
    REGISTER_DATE: ClassVar[str] = "_".join([
        TABLE_NAME,
        ColumnNames.REGISTER_DATE,
        "idx"
    ])


@dataclass(frozen=True)
class ResultTableConfig:
    TABLE_NAME: ClassVar[str] = TABLE_NAME
    COLUMN_NAMES: ClassVar[ColumnNames] = ColumnNames()
    INDEX_NAMES: ClassVar[IndexNames] = IndexNames()
