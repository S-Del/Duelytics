from logging import getLogger
from injector import singleton
from typing import Any, Callable, Type, TypeVar

from . import ApplicationEvent


EventType = TypeVar("EventType", bound=ApplicationEvent)


@singleton
class EventAggregator:
    """イベントの発行者と、その購読者を仲介するクラス。

    キーがイベント、値がコールバックの辞書を持つ。
    イベントが発行された時は、紐づいている全てのコールバックを呼び出す。
    """
    def __init__(self):
        # イベント (の型) をキーにしたコールバックのリスト
        self._events_for_subscribers: dict[
            Type[ApplicationEvent], list[Callable[[Any], None]]
        ] = {}
        self._logger = getLogger(__name__)

    def subscribe(self,
        event_type: Type[EventType],
        cbk: Callable[[EventType], None]
    ):
        """購読者 (Observer) が登録するためのメソッド"""
        self._events_for_subscribers.setdefault(event_type, []).append(cbk)
        self._logger.debug(
            "イベントの購読者が登録された。\n"
            f"\t{event_type.__name__} -> {cbk.__name__}"
        )

    def unsubscribe(self,
        event_type: Type[EventType],
        cbk: Callable[[EventType], None]
    ):
        """購読者が購読を解除するためのメソッド"""
        if event_type not in self._events_for_subscribers:
            return
        try:
            self._events_for_subscribers[event_type].remove(cbk)
            self._logger.debug(
                "イベントの購読が解除された。\n"
                f"\t{event_type.__name__} x {cbk.__name__}"
            )

            if not self._events_for_subscribers[event_type]:
                del self._events_for_subscribers[event_type]
                self._logger.debug(
                    f"購読者が居ないためキーを削除: {event_type.__name__}"
                )
        except ValueError:
            self._logger.warning(
                "登録されていない購読者 (コールバック) の削除が試みられた。\n"
                f"{event_type.__name__} ? {cbk.__name__}"
            )
            return

    def publish(self, event: ApplicationEvent):
        """発行者 (Subject) がイベントを発行するためのメソッド"""
        event_type = type(event)
        if not self._events_for_subscribers.get(event_type):
            self._logger.debug(
                f"発行されたイベントの購読者がいない: {event_type.__name__}"
                # 誰も来てくれなかった誕生日会みたいで悲しいね
            )
            return

        for cbk in self._events_for_subscribers[event_type]:
            try:
                cbk(event)
            except Exception as e:
                self._logger.error(
                    f"{event_type.__name__} のコールバック内でエラー: {e}",
                    exc_info=True
                )
                continue
