from typing import Sequence

from application.result import FirstOrSecondJP, ResultStringJP
from domain.model.result.duel_result import DuelResult
from . import ResultData


class ResultDataMapper:
    def to_data(self, result: DuelResult) -> ResultData:
        return ResultData(
            str(result.id),
            result.registered_at.strftime("%Y-%m-%d %H:%M:%S"),
            FirstOrSecondJP[result.first_or_second.value].value,
            result.first_or_second.value,
            ResultStringJP[result.result.value].value,
            result.result.value,
            result.my_deck_name.value,
            result.opponent_deck_name.value,
            result.memo.value if result.memo else ""
        )

    def to_data_list(self,
        results: Sequence[DuelResult]
    ) -> list[ResultData]:
        return [self.to_data(result) for result in results]
