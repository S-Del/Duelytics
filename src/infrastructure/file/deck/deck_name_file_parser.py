from domain.shared.unit import NonEmptyStr


class DeckNameFileParser:
    def parse_lines(self, lines: list[str]) -> set[NonEmptyStr]:
        names: set[NonEmptyStr] = set()
        for line in lines:
            if line.startswith('#'):
                continue
            try:
                name = NonEmptyStr(line.rstrip("\r\n"))
            except ValueError:
                continue
            names.add(name)
        return names
