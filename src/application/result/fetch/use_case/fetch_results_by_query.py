from datetime import date
from uuid import UUID
from injector import inject
from logging import getLogger
from sqlite3 import Error as SQLiteError

from application.exception import (
    ApplicationCriticalError, DomainObjectCreationError
)
from domain.model.deck import DeckDistribution
from domain.model.record import RecordFactory, Record
from domain.model.result import FirstOrSecond, ResultChar
from domain.model.trend import WinRateTrend
from domain.repository.result import SearchResultsQuery, ResultQueryRepository
from domain.repository.result.exception import RepositoryDataError
from domain.shared.unit import NonEmptyStr, PositiveInt
from . import (
    DistributionDataMapper,
    FetchResultsRequest,
    FetchResultsResponse,
    RecordData,
    ResultDataMapper
)


class FetchResultsByQuery:
    @inject
    def __init__(self, repository: ResultQueryRepository):
        self._repository = repository
        self._logger = getLogger(__name__)

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

    def _fetch_by_id(self, id: str | None) -> FetchResultsResponse | None:
        self._logger.info(f"ID での検索を開始: {id}")
        try:
            result = self._repository.search_by_id(UUID(id))
            if not result:
                return None
            record = RecordFactory([result]).create()
            self._logger.info(f"ID での検索完了")
            mapper = DistributionDataMapper(DeckDistribution([result]))
            trend = WinRateTrend([result]).aggregate()
            return FetchResultsResponse(
                ResultDataMapper().to_data_list([result]),
                self._convert_to_record_data(record),
                mapper.top_n_with_other(),
                mapper.top_n_with_other(),
                [percentage.value for percentage in trend]
            )
        except ValueError:
            self._logger.error(f"指定された ID の形式が不正: {id}")
            raise
        except (SQLiteError, RepositoryDataError) as e:
            self._logger.critical(f"試合結果の検索に失敗: {e}")
            raise ApplicationCriticalError from e

    def handle(self,
        request: FetchResultsRequest
    ) -> FetchResultsResponse | None:
        id = request.get("id")
        if id:
            # ID の指定がある場合は検索用クエリの作成はせず、
            # 即座に ID での検索結果を返す。
            return self._fetch_by_id(id)

        query: SearchResultsQuery = {}

        first_or_second = request.get("first_or_second")
        if first_or_second:
            try:
                query["first_or_second"] = [
                    FirstOrSecond(char) for char in first_or_second
                ]
            except ValueError as ve:
                self._logger.error(f"先攻/後攻の値が不正: {first_or_second}")
                raise DomainObjectCreationError from ve

        result = request.get("result")
        if result:
            try:
                query["result"] = [ResultChar(char) for char in result]
            except ValueError as ve:
                self._logger.error(f"試合結果の値が不正: {result}")
                raise DomainObjectCreationError from ve

        my_deck_name = request.get("my_deck_name")
        if my_deck_name:
            try:
                query["my_deck_name"] = NonEmptyStr(my_deck_name)
            except ValueError as ve:
                self._logger.error(f"自分デッキ名の指定が不正: {my_deck_name}")
                raise DomainObjectCreationError from ve
            search_type = request.get("my_deck_name_search_type")
            if not search_type:
                raise KeyError("自分のデッキ名の検索タイプの指定が無い")
            query["my_deck_name_search_type"] = search_type

        opponent_deck_name = request.get("opponent_deck_name")
        if opponent_deck_name:
            try:
                query["opponent_deck_name"] = NonEmptyStr(opponent_deck_name)
            except ValueError as ve:
                self._logger.error(
                    f"相手デッキ名の指定が不正: {opponent_deck_name}"
                )
                raise DomainObjectCreationError from ve
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

        limit = request.get("limit")
        if limit:
            try:
                query["limit"] = PositiveInt(limit)
            except ValueError as ve:
                self._logger.error(f"取得件数の指定が不正: {limit}")
                raise DomainObjectCreationError from ve

        self._logger.info("試合結果の検索開始")

        try:
            results = self._repository.search(query)
        except (SQLiteError, RepositoryDataError) as e:
            self._logger.critical(f"試合結果の検索に失敗: {e}")
            raise ApplicationCriticalError from e

        if not results:
            self._logger.info("検索結果無し")
            return None

        self._logger.info(f"試合結果の検索が完了 ({len(results)} 件)")

        mapper = DistributionDataMapper(DeckDistribution(results))
        if query["order"] == "DESC":
            trend = WinRateTrend(list(reversed(results))).aggregate()
        else:
            trend = WinRateTrend(results).aggregate()

        return FetchResultsResponse(
            ResultDataMapper().to_data_list(results),
            self._convert_to_record_data(RecordFactory(results).create()),
            mapper.top_n_with_other(),
            mapper.top_n_with_other(10),
            [percentage.value for percentage in trend]
        )
