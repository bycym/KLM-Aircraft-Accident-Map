from collections.abc import Iterable

from safety_database.csv_importer import ParsedAccident
from safety_database.model import AccidentRecord


class AccidentRepository:
    def count(self) -> int:
        return AccidentRecord.count()

    def save(self, accident: ParsedAccident) -> None:
        AccidentRecord(**accident.__dict__).save()

    def list_years(self) -> list[int]:
        return sorted({int(record.year) for record in AccidentRecord.scan()})

    def by_year(self, year: int) -> Iterable[AccidentRecord]:
        #item = AccidentRecord.year_index.query(2019)
        return AccidentRecord.year_index.query(year)
