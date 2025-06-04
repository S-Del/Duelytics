from injector import Module, Binder, ThreadLocalScope, singleton
from pathlib import Path

from application.events import EventAggregator
from application.result.edit import EditResultScenario
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
from infrastructure.file.deck import (
    DeckNameFilePath,
    DeckNameFileInitializer,
    DeckNameFileQueryRepository,
    DeckNameFileCommandRepository
)
from infrastructure.sqlite import SQLiteUnitOfWork
from infrastructure.sqlite.config import DatabaseFilePath
from infrastructure.sqlite.result import (
    SQLiteResultCommandRepository, SQLiteResultQueryRepository
)


class InjectorConfig(Module):
    def configure(self, binder: Binder):
        binder.bind(StartupMessageService, scope=singleton)
        binder.bind(EventAggregator, scope=singleton)

        # uow, repository
        binder.bind(DatabaseFilePath, to=Path("duelstats.db"), scope=singleton)
        binder.bind(UnitOfWork, to=SQLiteUnitOfWork, scope=ThreadLocalScope)
        binder.bind(
            ResultCommandRepository,
            to=SQLiteResultCommandRepository,
            scope=ThreadLocalScope
        )
        binder.bind(ResultQueryRepository, to=SQLiteResultQueryRepository)

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
