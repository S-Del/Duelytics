from injector import inject
from logging import getLogger
from typing import ClassVar

from application.services.file import IDeckNameFileInitializer
from infrastructure.file.deck import DeckNameFilePath
from infrastructure.file.deck.exceptions import DeckNameFileCreationError


class DeckNameFileInitializer(IDeckNameFileInitializer):
    INITIAL_CONTENT: ClassVar[str] = '\n'.join([
        "# このファイルはデッキ名入力の際の「入力補完」に使われます。",
        "# 1 行に 1 つのデッキ名を記入できます。",
        "# 試合結果登録時に新しいデッキ名であれば自動で登録されますが、",
        "# このファイルに直接自由に追加、削除できます。",
        "# '#' から始まる行はコメント行として扱われ、"
        "デッキ名としては読み込まれません。",
        "# また、空行も無視されます。",
        '\n'
    ])

    @inject
    def __init__(self, path: DeckNameFilePath):
        self._path = path
        self._logger = getLogger(__name__)

    def execute(self):
        if self._path.exists():
            self._logger.info(
                "デッキ名ファイルが存在するため作成をスキップ"
            )
            return

        self._logger.info("デッキ名ファイルの作成開始")
        try:
            with open(self._path, 'w', encoding="utf-8") as file:
                file.write(DeckNameFileInitializer.INITIAL_CONTENT)
        except OSError as ose:
            self._logger.error(f"デッキ名ファイルの作成失敗: {ose}")
            raise DeckNameFileCreationError from ose

        self._logger.info(f"デッキ名ファイル作成完了")
