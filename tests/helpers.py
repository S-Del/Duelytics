from contextlib import contextmanager
from datetime import datetime
from pytest import fail
from typing import Literal, Type
from uuid import UUID, uuid4

from application.services import UnitOfWork
from domain.shared.unit import NonEmptyStr
from domain.model.result import DuelResult, FirstOrSecond, ResultChar


def make_duel_result(
    id: UUID | None = None,
    registered_at: datetime | None = None,
    first_or_second_char: Literal['F', 'S'] = 'F',
    result_char: Literal['W', 'L', 'D'] = 'W',
    my_deck_name: str = "MY_DECK_NAME",
    opponent_deck_name: str = "OPPONENT_DECK_NAME",
    memo: str | None = None
) -> DuelResult:
    return DuelResult(
        id = id or uuid4(),
        registered_at=registered_at or datetime.now(),
        first_or_second=FirstOrSecond(first_or_second_char),
        result=ResultChar(result_char),
        my_deck_name=NonEmptyStr(my_deck_name),
        opponent_deck_name=NonEmptyStr(opponent_deck_name),
        memo=NonEmptyStr(memo) if memo else None
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
