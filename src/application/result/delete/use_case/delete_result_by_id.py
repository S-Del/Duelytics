from injector import inject
from logging import getLogger
from sqlite3 import Error as SQLiteError

from application.exception import ApplicationCriticalError
from application.result import IdForResult
from application.services import UnitOfWork
from domain.repository.result import ResultCommandRepository


class DeleteResultById:
    @inject
    def __init__(self, uow: UnitOfWork, repository: ResultCommandRepository):
        self._uow = uow
        self._repository = repository
        self._logger = getLogger(__name__)

    def handle(self, id_for_result: IdForResult):
        self._logger.info(f"ID による試合結果の削除を開始: {id_for_result.id}")

        try:
            with self._uow:
                self._repository.delete_by_id(id_for_result.uuid)
        except SQLiteError as se:
            self._logger.critical(f"データベースエラー: {se}")
            raise ApplicationCriticalError from se

        self._logger.info(f"試合結果の削除が完了")
