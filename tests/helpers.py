from datetime import datetime
from contextlib import contextmanager
from typing import Type
from uuid import uuid4

from pytest import fail

from domain.shared.unit import NonEmptyStr
from domain.model.result import DuelResult, FirstOrSecond, ResultChar
from domain.repository import UnitOfWork


def make_result(
    first_or_second: FirstOrSecond,
    result: ResultChar,
    my_deck_name = NonEmptyStr("MY_DECK_NAME"),
    opponent_deck_name = NonEmptyStr("OPPONENT_DECK_NAME"),
    registered_at: datetime | None = None,
    note: str | None = None
) -> DuelResult:
    return DuelResult(
        uuid4(),
        registered_at or datetime.now(),
        first_or_second,
        result,
        my_deck_name,
        opponent_deck_name,
        note
    )

@contextmanager
def expect_uow_rollback_on_error(
    uow: UnitOfWork,
    expected_exception_type: Type[Exception]
):
    """指定された UoW の管理下で指定された例外が発生し、
    UoW に伝わることを検証する。
    結果としてロールバックすることを期待するが、
    ロールバックの内容自体はこの関数では検証しない。

    Args:
        uow (UnitOfWork): テスト対象の UoW インスタンス
        expected_exception_type: 発生を期待する例外の型

    Raises:
        pytest.fail: 期待する例外が発生しなかった場合は失敗

    Example:
        with expect_uow_roll_back_on_error(uow, IntegrityError):
            command_repository.register(data)

        result = query_repository.fetch_all()
        assert len(list(result)) == 0
    """
    try:
        with uow:
            yield # 期待する例外が発生し得る処理がここで行われる。
        fail(
            "発生を期待した例外、"
            f"{expected_exception_type.__name__} が発生しなかった。"
        )
    except expected_exception_type:
        pass # 期待する例外が発生した場合は正常
