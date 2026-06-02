from typing import Any


def has_valid_coordinates(record: Any) -> bool:
    return record.latitude is not None and record.longitude is not None


class AccidentQueryService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def years(self) -> dict[str, list[int]]:
        return {"years": self.repository.list_years()}

    def accidents_by_year(self, year: int) -> dict[str, Any]:
        records = list(self.repository.by_year(year))
        points = [self._to_point(record) for record in records if has_valid_coordinates(record)]
        return {
            "year": year,
            "total_count": len(records),
            "unmapped_count": len(records) - len(points),
            "accidents": points,
        }

    @staticmethod
    def _to_point(record: Any) -> dict[str, Any]:
        return {
            "event_id": record.event_id,
            "latitude": float(record.latitude),
            "longitude": float(record.longitude),
            "event_date": record.event_date or "",
            "location": record.location or "",
            "country": record.country or "",
            "injury_severity": record.injury_severity or "",
            "aircraft_category": record.aircraft_category or "",
            "make": record.make or "",
            "model": record.model or "",
            "investigation_type": record.investigation_type or "",
            "accident_number": record.accident_number or "",
        }
