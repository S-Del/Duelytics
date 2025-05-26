from dataclasses import dataclass
from presentation.events import PresentationEvent


@dataclass(frozen=True)
class StatusBarMessageEvent(PresentationEvent):
    """ステータスバーへの通知が必要な際に発行されるイベント

    Attributes:
        msg (str): ステータスバーに表示したいメッセージ
        tooltip (str | None): tooltip として表示したいメッセージ
    """
    msg: str
    tooltip: str | None = None
