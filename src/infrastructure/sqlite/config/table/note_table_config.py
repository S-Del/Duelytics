from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class ColumnNames:
    ID: ClassVar[str] = "id"
    NOTE: ClassVar[str] = "note"


@dataclass(frozen=True)
class NoteTableConfig:
    TABLE_NAME: ClassVar[str] = "notes"
    COLUMN_NAMES: ClassVar[ColumnNames] = ColumnNames()
