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
        self._uow = uow
        self._result_repository = result_repository
        self._note_repository = note_repository
        self._register_deck = register_deck
        self._logger = getLogger(__name__)

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
            with self._uow:
                self._result_repository.register(duel_result)
                if command.note:
                    self._logger.info("メモの登録を開始")
                    note = Note(duel_result.id_raw, command.note)
                    self._note_repository.register(note)
        except SQLiteError as se:
            self._logger.critical(f"データベースエラー: {se}")
            raise ApplicationCriticalError from se
        self._logger.info("試合結果とメモ (あれば) の登録完了")
        self._logger.debug(str(duel_result))

        # デッキ名の記録は、
        # 試合結果記録の原始性 (試合結果記録時の UoW の管理下) に
        # 「含むべきではない」。
        # 試合結果テーブルとデッキ名ファイルは関係無いため。
        unique_deck_names = set([
            command.my_deck_name, command.opponent_deck_name
        ])
        for name in unique_deck_names:
            # 以下の RegisterDeckIfNotExists.handle() が送出する、
            # ApplicationOperationWarning はここでの追加処理が無い為、
            # 把捉せずそのまま上位へ伝えている。
            # 把捉したプレゼン層がユーザー通知を行うことを期待している。
            self._register_deck.handle(RegisterDeckCommand(name))
