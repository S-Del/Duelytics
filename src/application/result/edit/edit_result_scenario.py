from injector import inject
from logging import getLogger
from sqlite3 import Error as SQLiteError
from uuid import UUID

from application.deck.register.use_case import (
    RegisterDeckCommand, RegisterDeckIfNotExists
)
from application.exception import (
    ApplicationCriticalError, DomainObjectCreationError
)
from application.services import UnitOfWork
from domain.model.result import FirstOrSecond, ResultChar
from domain.repository.result import (
    ResultCommandRepository, ResultQueryRepository
)
from domain.shared.unit import NonEmptyStr
from . import EditResultCommand


class EditResultScenario:
    @inject
    def __init__(self,
        uow: UnitOfWork,
        query_repository: ResultQueryRepository,
        command_repository: ResultCommandRepository,
        register_deck: RegisterDeckIfNotExists,
    ):
        self._uow = uow
        self._query_repository = query_repository
        self._command_repository = command_repository
        self._register_deck = register_deck
        self._logger = getLogger(__name__)

    def execute(self, command: EditResultCommand):
        try:
            duel_result = self._query_repository.search_by_id(UUID(command.id))
        except SQLiteError as se:
            self._logger.critical(f"データベースエラー: {se}")
            raise ApplicationCriticalError from se
        if not duel_result:
            message = f"存在するはずの試合結果が見つからなかった"
            self._logger.critical(message)
            raise ApplicationCriticalError(message)

        self._logger.info("試合結果の編集を開始")
        try:
            edited_result = duel_result.update(
                first_or_second=FirstOrSecond(command.first_or_second),
                result=ResultChar(command.result),
                my_deck_name=NonEmptyStr(command.my_deck_name),
                opponent_deck_name=NonEmptyStr(command.opponent_deck_name),
                memo=NonEmptyStr(command.memo) if command.memo else None
            )
        except (ValueError, TypeError) as e:
            message = f"更新用データベース命令オブジェクトの作成に失敗: {e}"
            raise DomainObjectCreationError(message) from e

        try:
            with self._uow:
                self._command_repository.update(edited_result)
        except SQLiteError as se:
            self._logger.critical(f"データベースエラー: {se}")
            raise ApplicationCriticalError from se

        # デッキ名の記録は、
        # 試合結果記録の原始性 (試合結果記録時の UoW の管理下) に
        # 「含むべきではない」。
        # 試合結果テーブルとデッキ名ファイルは関係無いため。
        unique_deck_names = set([
            command.my_deck_name, command.opponent_deck_name
        ])
        for name in unique_deck_names:
            self._register_deck.handle(RegisterDeckCommand(name))
