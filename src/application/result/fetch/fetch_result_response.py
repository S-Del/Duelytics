from dataclasses import dataclass

from application.result.fetch.use_case import FetchResultData
from . import RecordData, EncounteredDeckData


@dataclass(frozen=True)
class FetchResultResponse:
    data_list: list[FetchResultData]
    record: RecordData
    distribution_for_pie: list[EncounteredDeckData]
    distribution_for_h_bar: list[EncounteredDeckData]
    win_rate_trend_data: list[float]
