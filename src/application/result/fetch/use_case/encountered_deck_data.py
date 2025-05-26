from dataclasses import dataclass


@dataclass(frozen=True)
class EncounteredDeckData:
    name: str
    count: int
    encounter_rate: str
