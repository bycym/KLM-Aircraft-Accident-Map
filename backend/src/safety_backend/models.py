from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    detail: str


class YearsResponse(BaseModel):
    years: list[int]


class AccidentPoint(BaseModel):
    event_id: str
    latitude: float
    longitude: float
    event_date: str
    location: str

    country: str
    injury_severity: str
    aircraft_category: str
    make: str

    model: str

    investigation_type: str
    accident_number: str


class AccidentYearResponse(BaseModel):
    year: int
    total_count: int
    unmapped_count: int
    accidents: list[AccidentPoint]
