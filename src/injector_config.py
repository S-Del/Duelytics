from injector import Module, Binder, ThreadLocalScope, singleton

from application.result.edit.edit_result_scenario import EditResultScenario
from application.result.register import RegisterResultScenario
from domain.repository import UnitOfWork
from domain.repository.result import (
    ResultCommandRepository, ResultQueryRepository
)
from domain.repository.deck import DeckCommandRepository, DeckQueryRepository
from domain.repository.note import NoteCommandRepository, NoteQueryRepository
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.result import (
    SQLiteResultCommandRepository, SQLiteResultQueryRepository
)
from infrastructure.sqlite.deck import (
    SQLiteDeckCommandRepository, SQLiteDeckQueryRepository
)
from infrastructure.sqlite.note import (
    SQLiteNoteCommandRepository, SQLiteNoteQueryRepository
)


class InjectorConfig(Module):
    def configure(self, binder: Binder):
        # uow, repository
        binder.bind(UnitOfWork, to=SQLiteUnitOfWork, scope=ThreadLocalScope)
        binder.bind(
            ResultCommandRepository,
            to=SQLiteResultCommandRepository,
            scope=ThreadLocalScope
        )
        binder.bind(ResultQueryRepository, to=SQLiteResultQueryRepository)
        binder.bind(
            NoteCommandRepository,
            to=SQLiteNoteCommandRepository,
            scope=ThreadLocalScope
        )
        binder.bind(NoteQueryRepository, to=SQLiteNoteQueryRepository)
        binder.bind(
            DeckCommandRepository,
            to=SQLiteDeckCommandRepository,
            scope=ThreadLocalScope
        )
        binder.bind(DeckQueryRepository, to=SQLiteDeckQueryRepository)

        # scenario, use_case
        binder.bind(RegisterResultScenario, scope=ThreadLocalScope)
        binder.bind(EditResultScenario, scope=ThreadLocalScope)
