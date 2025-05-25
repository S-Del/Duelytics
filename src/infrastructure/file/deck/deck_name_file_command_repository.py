from injector import inject
from logging import getLogger
from os import SEEK_END

from domain.repository.deck import DeckNameCommandRepository
from domain.shared.unit import NonEmptyStr
from infrastructure.file.deck.exceptions import (
    DeckNameFileNotFoundError, DeckNameFileWriteError
)
from . import DeckNameFilePath


class DeckNameFileCommandRepository(DeckNameCommandRepository):
    @inject
    def __init__(self, path: DeckNameFilePath):
        self._path = path
        self._logger = getLogger(__name__)

    def add(self, name: NonEmptyStr):
        try:
            # 本来は mode='a' を使用したいが、
            # このモードではファイルが存在しなかった場合に
            # 空ファイル新規作成するというクソキモい仕様を持っている。
            # デッキ名ファイルの初期内容は空では無く、
            # 「ファイルの使用法」のコメント行も含まれていて欲しいため、
            # 空ファイル作成を避けるために仕方なく "r+" を指定している。
            with open(self._path, "r+", encoding="utf-8") as file:
                # ファイル末尾へのシークを行うのみで、内容の読み取りは行わない。
                file.seek(0, SEEK_END)
                file.write(f"{name.value}\n")
        except FileNotFoundError as fne:
            msg = f"デッキ名ファイルが見つからなかった: {fne}"
            self._logger.error(msg, exc_info=True)
            raise DeckNameFileNotFoundError(msg) from fne
        except OSError as ose:
            msg = f"デッキ名ファイルの書き込みに失敗: {ose}"
            self._logger.error(msg, exc_info=True)
            raise DeckNameFileWriteError(msg) from ose
