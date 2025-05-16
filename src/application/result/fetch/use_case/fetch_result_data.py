from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class FetchResultData:
    id: str
    registered_at: str
    first_or_second: Literal["先攻", "後攻"]
    first_or_second_raw: Literal['F', 'S']
    result: Literal["勝利", "敗北", "引分"]
    result_raw: Literal['W', 'L', 'D']
    my_deck_name: str
    opponent_deck_name: str
    note: str | None

    def __iter__(self):
        yield self.registered_at
        yield self.first_or_second
        yield self.result
        yield self.my_deck_name
        yield self.opponent_deck_name
        yield self.note
        yield self.id

    def __len__(self):
        return len(list(self.__iter__()))

    def __getitem__(self, key: int | slice):
        return list(self)[key]

    def __str__(self) -> str:
        return "\n".join([
            f"ID: {self.id}",
            f"登録日時: {self.registered_at}",
            f"先/後: {self.first_or_second}",
            f"試合結果: {self.result}",
            f"自分のデッキ: {self.my_deck_name}",
            f"相手のデッキ: {self.opponent_deck_name}",
            f"メモ: {self.note}"
        ])
