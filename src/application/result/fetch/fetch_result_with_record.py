from datetime import date
from typing import Sequence
from uuid import UUID
from injector import inject
from logging import getLogger
from sqlite3 import Error as SQLiteError

from application.exception import ApplicationCriticalError
from application.result.fetch.use_case import FetchResultData
from domain.model.deck import DeckDistribution
from domain.model.record import RecordFactory, Record
from domain.model.result import FirstOrSecond, ResultChar
from domain.model.result.duel_result import DuelResult
from domain.model.trend.win_rate_trend import WinRateTrend
from domain.repository.result import FetchResultQuery, ResultQueryRepository
from domain.repository.result.exception import RepositoryDataError
from . import FetchResultRequest, FetchResultResponse, RecordData


class FetchResultWithRecord:
    @inject
    def __init__(self, repository: ResultQueryRepository):
        self.repository = repository
        self._logger = getLogger()

    def _convert_to_result_data(self, result: DuelResult) -> FetchResultData:
        return FetchResultData(
            result.id,
            result.registered_at,
            result.first_or_second.value,
            result.first_or_second_raw.value,
            result.result.value,
            result.result_raw.value,
            result.my_deck_name,
            result.opponent_deck_name,
            result.note
        )

    def _convert_to_record_data(self, record: Record) -> RecordData:
        return RecordData(
            f"{int(record.game_count)} 回",
            f"{int(record.win_count)} 回",
            f"{int(record.loss_count)} 回",
            f"{int(record.draw_count)} 回",
            f"{int(record.first_count)} 回",
            str(record.first_rate),
            f"{int(record.second_count)} 回",
            str(record.second_rate),
            str(record.win_rate),
            str(record.first_win_rate),
            str(record.second_win_rate)
        )

    def _convert_to_trend_data(self,
        results: Sequence[DuelResult]
    ) -> list[float]:
        percentages = WinRateTrend(list(reversed(results))).aggregate()
        return [percentage.value for percentage in percentages]

    def _fetch_by_id(self, id: str | None) -> FetchResultResponse | None:
        self._logger.info(f"ID での検索を開始: {id}")
        try:
            result = self.repository.search_by_id(UUID(id))
            if not result:
                return None
            record = RecordFactory([result]).create()
            self._logger.info(f"ID での検索完了")
            return FetchResultResponse(
                [self._convert_to_result_data(result)],
                self._convert_to_record_data(record),
                DeckDistribution([result]).aggregate(),
                self._convert_to_trend_data([result])
            )
        except ValueError:
            self._logger.error(f"指定された ID の形式が不正: {id}")
            raise
        except (SQLiteError, RepositoryDataError) as e:
            self._logger.critical(f"試合結果の検索に失敗: {e}")
            raise ApplicationCriticalError from e

    def handle(self,
        request: FetchResultRequest
    ) -> FetchResultResponse | None:
        id = request.get("id")
        if id:
            # ID の指定がある場合は検索用クエリの作成はせず、
            # 即座に ID での検索結果を返す。
            return self._fetch_by_id(id)

        query: FetchResultQuery = {}

        first_or_second = request.get("first_or_second")
        if first_or_second:
            try:
                query["first_or_second"] = [
                    FirstOrSecond(char) for char in first_or_second
                ]
            except ValueError:
                self._logger.error(f"先攻/後攻の値が不正: {first_or_second}")
                raise

        result = request.get("result")
        if result:
            try:
                query["result"] = [ResultChar(char) for char in result]
            except ValueError:
                self._logger.error(f"試合結果の値が不正: {result}")
                raise

        my_deck_name = request.get("my_deck_name")
        if my_deck_name:
            query["my_deck_name"] = my_deck_name
            search_type = request.get("my_deck_name_search_type")
            if not search_type:
                raise KeyError("自分のデッキ名の検索タイプの指定が無い")
            query["my_deck_name_search_type"] = search_type

        opponent_deck_name = request.get("opponent_deck_name")
        if opponent_deck_name:
            query["opponent_deck_name"] = opponent_deck_name
            search_type = request.get("opponent_deck_name_search_type")
            if not search_type:
                raise KeyError("相手デッキ名の検索タイプの指定が無い")
            query["opponent_deck_name_search_type"] = search_type

        since = request.get("since")
        if since:
            try:
                query["since"] = date.fromisoformat(since)
            except ValueError:
                self._logger.error(f"期間開始日の形式が不正: {since}")
                raise

        until = request.get("until")
        if until:
            try:
                query["until"] = date.fromisoformat(until)
            except ValueError:
                self._logger.error(f"期間終了日の形式が不正: {until}")
                raise

        query["order"] = request.get("order") or "DESC"

        self._logger.info("試合結果の検索開始")

        try:
            results = self.repository.search(query)
        except (SQLiteError, RepositoryDataError) as e:
            self._logger.critical(f"試合結果の検索に失敗: {e}")
            raise ApplicationCriticalError from e

        if not results:
            return None

        self._logger.info(f"試合結果の検索が完了 ({len(results)} 件)")

        return FetchResultResponse(
            [self._convert_to_result_data(result) for result in results],
            self._convert_to_record_data(RecordFactory(results).create()),
            DeckDistribution(results).aggregate(),
            self._convert_to_trend_data(results)
        )
