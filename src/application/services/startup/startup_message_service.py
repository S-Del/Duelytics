class StartupMessageService:
    def __init__(self):
        self._warnings: list[tuple[str, str | None]] = []

    def add_warning(self, msg: str, details: str | None = None):
        self._warnings.append((msg, details))

    def get_pending_warnings(self) -> list[tuple[str, str | None]]:
        warnings = list(self._warnings)
        self._warnings.clear()
        return warnings

    def has_pending_messages(self) -> bool:
        return bool(self._warnings)
