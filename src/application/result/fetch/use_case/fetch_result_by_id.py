from injector import inject
from logging import getLogger
from sqlite3 import Error as SQLiteError

from application.exception import ApplicationCriticalError
from application.result import IdForResult
from domain.repository.result import ResultQueryRepository
from . import FetchResultData


class FetchResultById:
    """ID で試合結果を取得するユースケースクラス

    このクラスは主に「編集」や「削除」前の存在確認等に使用される。

    「検索」にて使用される、 `fetch_result_with_record` でも
    ID を使った検索と取得は可能だが、
    これは検索条件を組み合わせた上で、戦績やデッキ分布を求める場合に使用される。
    """
    @inject
    def __init__(self, repository: ResultQueryRepository):
        self.repository = repository
        self._logger = getLogger()

    def handle(self, id_for_result: IdForResult) -> FetchResultData | None:
        self._logger.info(f"ID での試合結果の検索開始: {id_for_result.id}")
        try:
            result = self.repository.search_by_id(id_for_result.uuid)
        except SQLiteError as e:
            self._logger.warning(f"データベースエラー: {e}")
            raise ApplicationCriticalError from e

        if not result:
            self._logger.info(f"指定された ID の試合が存在しなかった")
            return

        self._logger.info("\n".join([
            "ID での試合結果の検索完了",
            str(result)
        ]))

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
