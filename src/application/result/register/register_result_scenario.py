from datetime import datetime
from injector import inject
from logging import getLogger
from sqlite3 import Error as SQLiteError

from application.deck.register.use_case import (
    RegisterDeckCommand, RegisterDeckIfNotExists
)
from application.exception import (
    ApplicationCriticalError, DomainObjectCreationError
)
from application.services import UnitOfWork
from domain.model.result import DuelResult, FirstOrSecond, ResultChar
from domain.repository.result import ResultCommandRepository
from domain.shared.unit import NonEmptyStr
from . import RegisterResultCommand


class RegisterResultScenario:
    @inject
    def __init__(self,
        uow: UnitOfWork,
        result_repository: ResultCommandRepository,
        register_deck: RegisterDeckIfNotExists
    ):
        self._uow = uow
        self._result_repository = result_repository
        self._register_deck = register_deck
        self._logger = getLogger(__name__)

    def execute(self, command: RegisterResultCommand):
        try:
            memo = NonEmptyStr(command.note) if command.note else None
            duel_result = DuelResult(
                registered_at=datetime.now(),
                first_or_second=FirstOrSecond(command.first_or_second),
                result=ResultChar(command.result),
                my_deck_name=NonEmptyStr(command.my_deck_name),
                opponent_deck_name=NonEmptyStr(command.opponent_deck_name),
                memo=memo
            )
        except (ValueError, TypeError) as e:
            # command 生成時にバリデーションされているので、
            # 発生しないと思われるが、念のため。
            result_message_parts = f"試合結果オブジェクトの作成に失敗: {e}"
            self._logger.error(result_message_parts, exc_info=True)
            raise DomainObjectCreationError(result_message_parts) from e

        # 試合結果の記録
        self._logger.info("試合結果の登録を開始")
        result_message_parts = [
            f"\tID: {duel_result.id}",
            "\t登録日時: "
            f"{duel_result.registered_at.isoformat(timespec='seconds')}",
            f"\t先/後: {duel_result.first_or_second.value}",
            f"\t試合結果: {duel_result.result.value}",
            f"\t自分のデッキ名: {duel_result.my_deck_name.value}",
            f"\t相手のデッキ名: {duel_result.opponent_deck_name.value}"
        ]
        if duel_result.memo:
            result_message_parts.append(f"メモ: {duel_result.memo.value}")
        self._logger.debug("\n".join(result_message_parts))
        try:
            with self._uow:
                self._result_repository.register(duel_result)
        except SQLiteError as se:
            self._logger.critical(f"データベースエラー: {se}")
            raise ApplicationCriticalError from se
        self._logger.info("試合結果の登録完了")

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
