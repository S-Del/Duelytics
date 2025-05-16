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
from domain.model.result import FirstOrSecond, ResultChar
from domain.model.note import Note
from domain.repository import UnitOfWork
from domain.repository.note import NoteCommandRepository, NoteQueryRepository
from domain.repository.result import (
    UpdateResultCommand, ResultCommandRepository
)
from . import EditResultCommand


class EditResultScenario:
    @inject
    def __init__(self,
        uow: UnitOfWork,
        result_repository: ResultCommandRepository,
        note_command_repository: NoteCommandRepository,
        note_query_repository: NoteQueryRepository,
        register_deck: RegisterDeckIfNotExists
    ):
        self.uow = uow
        self.result_repository = result_repository
        self.note_command_repository = note_command_repository
        self.note_query_repository = note_query_repository
        self.register_deck = register_deck
        self._logger = getLogger()

    def handle(self, command: EditResultCommand):
        self._logger.info("試合結果の編集を開始")
        try:
            update_command = UpdateResultCommand(
                UUID(command.id),
                FirstOrSecond(command.first_or_second),
                ResultChar(command.result),
                command.my_deck_name,
                command.opponent_deck_name
            )
        except (ValueError, TypeError) as e:
            message = f"更新用データベース命令オブジェクトの作成に失敗: {e}"
            raise DomainObjectCreationError(message) from e

        try:
            src_note = self.note_query_repository.search_by_id(
                update_command.id
            )

            with self.uow:
                self.result_repository.update(update_command)
                # メモの入力があったら upsert
                if command.note:
                    self.note_command_repository.upsert(
                        Note(update_command.id, command.note)
                    )
                # メモの入力が無いのに、元のノートが存在する場合は削除。
                if command.note is None and src_note is not None:
                    self.note_command_repository.delete_by_id(
                        update_command.id
                    )
        except SQLiteError as se:
            self._logger.critical(f"データベースエラー: {se}")
            raise ApplicationCriticalError from se

        # デッキ名の記録は、
        # 試合結果記録の原始性 (試合結果記録時の UoW の管理下) に
        # 「含むべきではない」。
        # 試合結果テーブルとデッキ名テーブルに依存性や結合は無い為。
        unique_deck_names = set([
            command.my_deck_name, command.opponent_deck_name
        ])
        try:
            self._logger.info("デッキ名の登録開始")
            for name in unique_deck_names:
                self.register_deck.handle(RegisterDeckCommand(name))
        except SQLiteError as se:
            # こちらでも DB のエラーは把捉して記録し「異常終了したい」のは同様
            self._logger.critical(f"データベースエラー: {se}")
            raise ApplicationCriticalError from se
        self._logger.info("デッキ名の登録完了")
