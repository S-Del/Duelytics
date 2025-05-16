from sqlite3 import  connect, IntegrityError, Row
from uuid import  uuid4
from pytest import fixture

from domain.model.note import Note
from domain.model.result import FirstOrSecond, ResultChar
from infrastructure.sqlite.config import DatabaseConfig
from infrastructure.sqlite.config.table import NoteTableConfig
from infrastructure.sqlite.result import SQLiteResultCommandRepository
from infrastructure.sqlite.note import (
    SQLiteNoteCommandRepository, SQLiteNoteQueryRepository
)
from infrastructure.sqlite.unit_of_work import SQLiteUnitOfWork
from tests.helpers import expect_uow_rollback_on_error, make_result


def delete_all():
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        conn.execute(f"DELETE FROM {NoteTableConfig.TABLE_NAME}")
        conn.commit()


@fixture
def uow():
    return SQLiteUnitOfWork()


@fixture
def note_command_repository(uow):
    return SQLiteNoteCommandRepository(uow)


@fixture
def note_query_repository():
    return SQLiteNoteQueryRepository()


@fixture
def result_command_repository(uow):
    return SQLiteResultCommandRepository(uow)


# QueryRepository には全件取得メソッドは無い為、ここで用意している。
def fetch_all():
    with connect(DatabaseConfig.DATABASE_NAME) as conn:
        conn.row_factory = Row
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {NoteTableConfig.TABLE_NAME}")
        datas = cursor.fetchall()

    notes: list[Note] = []
    if not datas:
        return notes
    for data in datas:
        notes.append(Note(
            data[NoteTableConfig.COLUMN_NAMES.ID],
            data[NoteTableConfig.COLUMN_NAMES.NOTE]
        ))
    return notes


def test_crud_flow(
    uow: SQLiteUnitOfWork,
    note_command_repository: SQLiteNoteCommandRepository,
    note_query_repository: SQLiteNoteQueryRepository,
    result_command_repository: SQLiteResultCommandRepository
):
    delete_all()
    notes = fetch_all()
    assert len(notes) == 0

    # Note は試合結果テーブルの ID と紐づくので、
    # 試合結果が存在しない場合は登録できてはならない。
    note = Note(uuid4(), "IntegrityErrorCase")
    with expect_uow_rollback_on_error(uow, IntegrityError):
        note_command_repository.register(note)
    with expect_uow_rollback_on_error(uow, IntegrityError):
        note_command_repository.upsert(note)
    notes = fetch_all()
    assert len(notes) == 0

    # 試合結果が存在すれば登録できるか検証
    result = make_result(FirstOrSecond.FIRST, ResultChar.WIN)
    with uow:
        result_command_repository.register(result)
    with uow:
        note = Note(result.id_raw, "ValidCase")
        note_command_repository.register(note)
    notes = fetch_all()
    assert len(notes) == 1
    assert notes[0].content == "ValidCase"

    # 取得し直して同一性をチェック
    registered_note = note_query_repository.search_by_id(note.id_raw)
    assert registered_note is not None
    assert note == registered_note # Note は Entity なので == で比較できる

    with uow:
        # 試合結果が存在すれば更新できるか検証
        new_note = Note(result.id_raw, "Updated")
        note_command_repository.upsert(new_note)
    updated_note = note_query_repository.search_by_id(new_note.id_raw)
    assert updated_note is not None
    assert updated_note == new_note
    assert updated_note.content == "Updated"

    # 試合結果は存在するが、まだメモは存在しない状態で登録できるか検証。
    new_result = make_result(FirstOrSecond.SECOND, ResultChar.LOSS)
    with uow:
        result_command_repository.register(new_result)
    note = note_query_repository.search_by_id(new_result.id_raw)
    assert note is None
    with uow:
        note_command_repository.upsert(Note(new_result.id_raw, "New Note"))
    note = note_query_repository.search_by_id(new_result.id_raw)
    assert note is not None
    assert note.content == "New Note"
