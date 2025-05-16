from collections import Counter
from dataclasses import dataclass

from application.result.fetch.use_case import FetchResultData
from . import RecordData


@dataclass(frozen=True)
class FetchResultResponse:
    data_list: list[FetchResultData]
    record: RecordData
    deck_distribution: Counter[str]
    win_rate_trend_data: list[float]
