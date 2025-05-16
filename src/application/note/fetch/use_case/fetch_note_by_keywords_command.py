from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class FetchNoteByKeywordsCommand:
    keywords: Sequence[str]
