from injector import Module, Binder, ThreadLocalScope, singleton
from pathlib import Path

from application.events import EventAggregator
from application.result.edit.edit_result_scenario import EditResultScenario
from application.result.register import RegisterResultScenario
from application.services import UnitOfWork
from application.services.file import IDeckNameFileInitializer
from application.services.startup import StartupMessageService
from domain.repository.result import (
    ResultCommandRepository, ResultQueryRepository
)
from domain.repository.deck import (
    DeckNameCommandRepository, DeckNameQueryRepository
)
from domain.repository.note import NoteCommandRepository, NoteQueryRepository
from infrastructure.file.deck import (
    DeckNameFilePath,
    DeckNameFileInitializer,
    DeckNameFileQueryRepository,
    DeckNameFileCommandRepository
)
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.result import (
    SQLiteResultCommandRepository, SQLiteResultQueryRepository
)
from infrastructure.sqlite.note import (
    SQLiteNoteCommandRepository, SQLiteNoteQueryRepository
)


class InjectorConfig(Module):
    def configure(self, binder: Binder):
        binder.bind(StartupMessageService, scope=singleton)
        binder.bind(EventAggregator, scope=singleton)

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

        binder.bind(DeckNameFilePath, to=Path("decks.dnl"), scope=singleton)
        binder.bind(
            IDeckNameFileInitializer,
            to=DeckNameFileInitializer,
            scope=singleton)
        binder.bind(
            DeckNameCommandRepository, to=DeckNameFileCommandRepository
        )
        binder.bind(DeckNameQueryRepository, to=DeckNameFileQueryRepository)

        # scenario, use_case
        binder.bind(RegisterResultScenario, scope=ThreadLocalScope)
        binder.bind(EditResultScenario, scope=ThreadLocalScope)
