import csv
import re
from collections.abc import Iterable
from dataclasses import dataclass

from .logger import logger


@dataclass(frozen=True)
class ParsedAccident:
    event_id: str

    year: int
    location_key: str
    latitude: float | None
    longitude: float | None
    event_date: str

    location: str
    country: str
    injury_severity: str
    aircraft_category: str
    make: str
    model: str
    investigation_type: str
    accident_number: str


def normalize_location_key(location: str, country: str) -> str:
    raw = f"{country}:{location}".strip().lower()
    norm = re.sub(r"[^a-z0-9]+", "-", raw)
    
    #normalized = norm.strip("-").lower()

    normalized = norm.strip("-")
    # logger.info(f"{normalized}")

    return normalized or "unknown"


def parse_coordinate(value: str) -> float | None:
    stripped = value.strip()
    if not stripped:
        return None
    try:
        return float(stripped)
    except ValueError:
        return None


def parse_row(row: dict[str, str]) -> ParsedAccident | None:
    event_date = row["Event.Date"].strip()
    event_id = row["Event.Id"].strip()
    location = row.get("Location", "").strip()
    country = row.get("Country", "").strip()

    return ParsedAccident(
        event_id=event_id,
        year=int(event_date[:4]),
        location_key=normalize_location_key(location, country),
        
        latitude=parse_coordinate(row.get("Latitude", "")),
        longitude=parse_coordinate(
            row.get("Longitude", "")),
        event_date=event_date,

        location=location,
        country=country,
        injury_severity=row.get("Injury.Severity", "").strip(),
        #aircraft_category=row.get("Category", ""),

        aircraft_category=row.get("Aircraft.Category", "").strip(),
        make=row.get("Make", "").strip(),
        model=row.get("Model", "").strip(),
        investigation_type=row.get("Investigation.Type", "").strip(),
        accident_number=row.get("Accident.Number", "").strip(),
    )


def read_accidents(csv_path: str) -> Iterable[ParsedAccident]:
    with open(csv_path, encoding="latin-1", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            parsed = parse_row(row)
            
            #print(f"{parsed}")
            if parsed is not None:
                yield parsed


class AccidentSeeder:
    def __init__(self, repository) -> None:
        self.repository = repository

    def seed_if_empty(self, csv_path: str) -> int:
        if self.repository.count() > 0:
            return 0
        written = 0
        for accident in read_accidents(csv_path):
            self.repository.save(accident)
            written += 1
        return written
