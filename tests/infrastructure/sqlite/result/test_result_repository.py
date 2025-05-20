from datetime import date, datetime
from sqlite3 import connect
from pytest import fixture

from domain.model.result import FirstOrSecond, ResultChar
from domain.repository.result import FetchResultQuery, UpdateResultCommand
from domain.shared.unit import NonEmptyStr, PositiveInt
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import ResultTableConfig
from infrastructure.sqlite.result import (
    SQLiteResultCommandRepository, SQLiteResultQueryRepository
)
from infrastructure.sqlite.result import SearchConditionBuilder
from tests.helpers import make_result


def delete_all():
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        conn.execute(f"DELETE FROM {ResultTableConfig.TABLE_NAME}")
        conn.commit()


@fixture
def uow() -> SQLiteUnitOfWork:
    return SQLiteUnitOfWork()


@fixture
def command_repository(uow):
    return SQLiteResultCommandRepository(uow)


@fixture
def builder():
    return SearchConditionBuilder()


@fixture
def query_repository(builder):
    return SQLiteResultQueryRepository(builder)


def test_crud_flow(
    uow: SQLiteUnitOfWork,
    command_repository: SQLiteResultCommandRepository,
    query_repository: SQLiteResultQueryRepository
):
    # 空の query で全件取得し、件数が 0 であるか検証。
    delete_all()
    query: FetchResultQuery = {}
    count = len(query_repository.search(query))
    assert count == 0

    # テスト用の試合結果を作成して INSERT
    result = make_result(FirstOrSecond.FIRST, ResultChar.WIN)
    with uow:
        command_repository.register(result)

    # INSERT した試合結果を ID を指定して取得
    searched = query_repository.search_by_id(result.id_raw)
    assert searched is not None
    # Entity に定義した __eq__ (ID) による同一性検証
    assert searched == result
    # NoteRepository を介していないのでかならず None となる
    assert searched.note == None

    # 更新
    changed_side = FirstOrSecond.SECOND
    changed_result = ResultChar.LOSS
    changed_deck_name = "CHANGED"
    update_command = UpdateResultCommand(
        result.id_raw,
        changed_side,
        changed_result,
        changed_deck_name,
        changed_deck_name
    )
    with uow:
        command_repository.update(update_command)

    # 再度取得して同一性と更新を検証
    searched = query_repository.search_by_id(result.id_raw)
    assert searched is not None
    assert searched == result
    assert searched.first_or_second == changed_side
    assert searched.result == changed_result
    assert searched.my_deck_name == NonEmptyStr(changed_deck_name)
    assert searched.opponent_deck_name == NonEmptyStr(changed_deck_name)

    # 削除
    with uow:
        command_repository.delete_by_id(result.id_raw)

    # 再度取得して存在しないことを検証
    deleted = query_repository.search_by_id(result.id_raw)
    assert deleted is None


@fixture
def insert_test_data(
    uow: SQLiteUnitOfWork,
    command_repository: SQLiteResultCommandRepository,
    query_repository: SQLiteResultQueryRepository
):
    results = (
        make_result(
            FirstOrSecond.FIRST, ResultChar.WIN,
            NonEmptyStr("メタビート"), NonEmptyStr("ティアラメンツ"),
            datetime.fromisoformat("2023-01-01")
        ),
        make_result(
            FirstOrSecond.SECOND, ResultChar.LOSS,
            NonEmptyStr("ドラゴンリンク"), NonEmptyStr("ふわんだりぃず"),
            datetime.fromisoformat("2024-01-01")
        ),
        make_result(
            FirstOrSecond.FIRST, ResultChar.LOSS,
            NonEmptyStr("ドラゴンリンク"), NonEmptyStr("ティアラメンツ"),
            datetime.fromisoformat("2024-01-01")
        ),
        make_result(
            FirstOrSecond.SECOND, ResultChar.WIN,
            NonEmptyStr("メタビート"), NonEmptyStr("ふわんだりぃず"),
            datetime.fromisoformat("2024-01-01")
        ),
        make_result(
            FirstOrSecond.SECOND, ResultChar.DRAW,
            NonEmptyStr("ラビュリンス"), NonEmptyStr("クシャトリラ"),
            datetime.fromisoformat("2025-01-01")
        )
    )

    delete_all()

    with uow:
        for duel in results:
            command_repository.register(duel)

    # 空の query で全件取得し、件数を検証。
    query: FetchResultQuery = {}
    count = len(query_repository.search(query))
    assert count == 5


def test_search_query(
    insert_test_data, # テスト用データのみが登録された状態になる
    query_repository: SQLiteResultQueryRepository
):
    results = query_repository.search({
        "first_or_second": [FirstOrSecond.FIRST]
    })
    assert len(results) == 2
    results = query_repository.search({
        "first_or_second": [FirstOrSecond.SECOND]
    })
    assert len(results) == 3

    results = query_repository.search({
        "result": [ResultChar.WIN]
    })
    assert len(results) == 2
    results = query_repository.search({
        "result": [ResultChar.LOSS]
    })
    assert len(results) == 2

    results_draw = query_repository.search({
        "result": [ResultChar.DRAW]
    })
    assert len(results_draw) == 1
    results_labrynth = query_repository.search({
        "my_deck_name": NonEmptyStr("ラビュリンス")
    })
    assert len(results_labrynth) == 1
    results_kashtira = query_repository.search({
        "opponent_deck_name": NonEmptyStr("クシャトリラ")
    })
    assert len(results_kashtira) == 1
    # テストデータではラビュとクシャの試合それぞれ 1 試合のみで、
    # つまり「ラビュ vs クシャ」しか登録されていない。
    # そして引分の試合もこの試合しか無い。
    # つまり 3 件の試合データは同じ試合データを取得しているということになので、
    # 全てを比較した結果は同一でなければならない。
    assert results_labrynth[0] == results_kashtira[0] == results_draw[0]

    # search_type を指定しない場合はデフォルトで exact の検索となる。
    # 先ほどのケースで検証済みのため、ここではテストはしない。
    results = query_repository.search({
        "my_deck_name": NonEmptyStr("メタビ"),
        "my_deck_name_search_type": "prefix"
    })
    assert len(results) == 2
    results = query_repository.search({
        "my_deck_name": NonEmptyStr("ート"),
        "my_deck_name_search_type": "suffix"
    })
    assert len(results) == 2
    results = query_repository.search({
        "my_deck_name": NonEmptyStr("タビー"),
        "my_deck_name_search_type": "partial"
    })
    assert len(results) == 2
    results = query_repository.search({
        "opponent_deck_name": NonEmptyStr("ティアラ"),
        "opponent_deck_name_search_type": "prefix"
    })
    assert len(results) == 2
    results = query_repository.search({
        "opponent_deck_name": NonEmptyStr("メンツ"),
        "opponent_deck_name_search_type": "suffix"
    })
    assert len(results) == 2
    results = query_repository.search({
        "opponent_deck_name": NonEmptyStr("アラメ"),
        "opponent_deck_name_search_type": "partial"
    })
    assert len(results) == 2

    results = query_repository.search({
        "since": date.fromisoformat("2025-01-01")
    })
    assert len(results) == 1
    results = query_repository.search({
        "until": date.fromisoformat("2023-01-01")
    })
    assert len(results) == 1
    equal_date = date.fromisoformat("2024-01-01")
    results = query_repository.search({
        "since": equal_date,
        "until": equal_date
    })
    # since と unitl に同じ日付が指定されても、
    # since の 00:00:00 から until の 23:59:59 までを取得できなければならない。
    # よって、テストデータ 3 件全てを取得できていなければならない。
    assert len(results) == 3

    # LIMIT 句
    results = query_repository.search({
        "limit": PositiveInt(1)
    })
    assert len(results) == 1

    # 全ての検索条件の組み合わせを網羅することは不可能なので、
    # 以下では、よく使われると思われる検索条件の組み合わせでテストを行う。

    # 「自分のデッキ名、相手のデッキ名」指定
    # 有利対面もしくは不利対面としての懸念がある場合に、
    # 実際の状況を把握する場合に使用されると思われる。
    results = query_repository.search({
        "my_deck_name": NonEmptyStr("メタビート"),
        "opponent_deck_name": NonEmptyStr("ふわんだりぃず")
    })
    assert len(results) == 1

    # 「自分のデッキ名、以降日付」指定
    # 新パックの販売やリミットレギュレーションの変更など、
    # 自分のデッキ内容に変更があった場合は、
    # 特定の日付 (デッキ変更) 以降の試合結果を検索したい場合がある。
    results = query_repository.search({
        "my_deck_name": NonEmptyStr("ラビュリンス"),
        "since": date.fromisoformat("2025-01-01")
    })
    assert len(results) == 1

    # 「先攻、敗北、自分のデッキ名」指定
    # 遊戯王は基本的に先攻が強いカードゲームなため、
    # 先攻での敗因や苦手とする相手を把握するために、
    # この検索はよく使われると思われる。
    results = query_repository.search({
        "first_or_second": [FirstOrSecond.FIRST],
        "result": [ResultChar.LOSS],
        "my_deck_name": NonEmptyStr("ドラゴンリンク")
    })
    assert len(results) == 1

    # 以下は異常系
    results = query_repository.search({
        "my_deck_name": NonEmptyStr("存在しないデッキ名")
    })
    assert len(results) == 0
    results = query_repository.search({
        "opponent_deck_name": NonEmptyStr("存在しないデッキ名")
    })
    assert len(results) == 0
    results = query_repository.search({
        "since": date.fromisoformat("2030-01-01")
    })
    assert len(results) == 0
    results = query_repository.search({
        "until": date.fromisoformat("2020-01-01")
    })
    assert len(results) == 0
