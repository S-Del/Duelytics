from datetime import datetime
from uuid import uuid4
from injector import inject
from logging import getLogger
from sqlite3 import Error as SQLiteError

from application.deck.register.use_case import (
    RegisterDeckCommand, RegisterDeckIfNotExists
)
from application.exception import (
    ApplicationCriticalError, DomainObjectCreationError
)
from domain.model.note import Note
from domain.model.result import DuelResult, FirstOrSecond, ResultChar
from domain.repository import UnitOfWork
from domain.repository.deck import DeckCommandRepository, DeckQueryRepository
from domain.repository.note import NoteCommandRepository
from domain.repository.result import ResultCommandRepository
from domain.shared.unit import NonEmptyStr
from . import RegisterResultCommand

class RegisterResultScenario:
    @inject
    def __init__(self,
        uow: UnitOfWork,
        result_repository: ResultCommandRepository,
        note_repository: NoteCommandRepository,
        register_deck: RegisterDeckIfNotExists
    ):
        self.uow = uow
        self.result_repository = result_repository
        self.note_repository = note_repository
        self.register_deck = register_deck
        self._logger = getLogger()

    def execute(self, command: RegisterResultCommand):
        try:
            duel_result = DuelResult(
                uuid4(),
                datetime.now(),
                FirstOrSecond(command.first_or_second),
                ResultChar(command.result),
                NonEmptyStr(command.my_deck_name),
                NonEmptyStr(command.opponent_deck_name)
            )
        except (ValueError, TypeError) as e:
            # command 生成時にバリデーションされているので、
            # 発生しないと思われるが、念のため。
            message = f"試合結果オブジェクトの作成に失敗: {e}"
            self._logger.error(message, exc_info=True)
            raise DomainObjectCreationError(message) from e

        # 試合結果（とメモ）の記録
        self._logger.info("試合結果とメモ (あれば) の登録を開始")
        try:
            with self.uow:
                self.result_repository.register(duel_result)
                if command.note:
                    self._logger.info("メモの登録を開始")
                    note = Note(duel_result.id_raw, command.note)
                    self.note_repository.register(note)
        except SQLiteError as se:
            self._logger.critical(f"データベースエラー: {se}")
            raise ApplicationCriticalError from se
        self._logger.info("試合結果とメモ (あれば) の登録完了")
        self._logger.debug(str(duel_result))

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
