from dataclasses import dataclass

from application.result.fetch.use_case import ResultData
from . import RecordData, EncounteredDeckData


@dataclass(frozen=True)
class FetchResultsResponse:
    result_data_list: list[ResultData]
    record: RecordData
    distribution_for_pie: list[EncounteredDeckData]
    distribution_for_h_bar: list[EncounteredDeckData]
    win_rate_trend_data: list[float]
