from datetime import date, datetime, time
from typing import Any, Literal, Sequence

from domain.repository.result import FetchResultQuery
from infrastructure.sqlite.config.table import ResultTableConfig


SearchType = Literal["exact", "partial", "prefix", "suffix"]


class SearchConditionBuilder:
    def __init__(self):
        self.conditions: list[str] = []
        self.params: list[Any] = []

    @staticmethod
    def escape_like_param(
        value: str,
        search_type: SearchType = "exact"
    ) -> str:
        escaped = (value.replace("\\", "\\\\")
                        .replace("%", "\\%")
                        .replace("_", "\\_"))
        if search_type == "exact":
            return escaped
        if search_type == "partial":
            return f"%{escaped}%"
        if search_type == "prefix":
            return f"{escaped}%"
        if search_type == "suffix":
            return f"%{escaped}"
        raise ValueError(f"検索条件の指定が不正: {search_type}")

    def add_in(self,
        column_name: str,
        values: Sequence[str]
    ) -> "SearchConditionBuilder":
        if not values:
            return self
        place_holders = ", ".join(['?'] * len(values))
        self.conditions.append(f"{column_name} IN ({place_holders})")
        self.params.extend(values)
        return self

    def add_like(self,
        column_name: str,
        value: str,
        search_type: SearchType = "exact"
    ) -> "SearchConditionBuilder":
        escaped = SearchConditionBuilder.escape_like_param(value, search_type)
        self.conditions.append(f"{column_name} LIKE ? ESCAPE '\\'")
        self.params.append(escaped)
        return self

    def add_since(self,
        column_name: str,
        since: date
    ) -> "SearchConditionBuilder":
        self.conditions.append(f"{column_name} >= ?")
        time_str = time.fromisoformat("00:00:00")
        date_time_str = (
            datetime.combine(since, time_str)
                    .isoformat(timespec="seconds")
        )
        self.params.append(date_time_str)
        return self

    def add_until(self,
        column_name: str,
        until: date
    ) -> "SearchConditionBuilder":
        self.conditions.append(f"{column_name} <= ?")
        time_str = time.fromisoformat("23:59:59")
        date_time_str = (
            datetime.combine(until, time_str)
                    .isoformat(timespec="seconds")
        )
        self.params.append(date_time_str)
        return self

    def build(self, query: FetchResultQuery) -> tuple[str, tuple[Any]]:
        first_or_second = query.get("first_or_second")
        if first_or_second:
            self.add_in(
                ResultTableConfig.COLUMN_NAMES.FIRST_OR_SECOND,
                [char.value for char in first_or_second]
            )

        result = query.get("result")
        if result:
            self.add_in(
                ResultTableConfig.COLUMN_NAMES.RESULT,
                [char.value for char in result]
            )

        my_deck_name = query.get("my_deck_name")
        if my_deck_name:
            self.add_like(
                ResultTableConfig.COLUMN_NAMES.MY_DECK_NAME,
                my_deck_name.value,
                query.get("my_deck_name_search_type") or "exact"
            )

        opponent_deck_name = query.get("opponent_deck_name")
        if opponent_deck_name:
            self.add_like(
                ResultTableConfig.COLUMN_NAMES.OPPONENT_DECK_NAME,
                opponent_deck_name.value,
                query.get("opponent_deck_name_search_type") or "exact"
            )

        since = query.get("since")
        if since:
            self.add_since(
                ResultTableConfig.COLUMN_NAMES.REGISTER_DATE,
                since
            )

        until = query.get("until")
        if until:
            self.add_until(
                ResultTableConfig.COLUMN_NAMES.REGISTER_DATE,
                until
            )

        if not self.conditions:
            return ("", tuple())

        where_clause = " WHERE " + " AND ".join(self.conditions)
        params = tuple(self.params)
        self.conditions.clear()
        self.params.clear()
        return where_clause, params
