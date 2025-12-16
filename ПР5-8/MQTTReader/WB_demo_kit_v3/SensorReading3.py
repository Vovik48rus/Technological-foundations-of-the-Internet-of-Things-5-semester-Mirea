from datetime import datetime
from pydantic import BaseModel, field_validator

class SensorReading(BaseModel):
    illuminance: float
    voltage: float
    co2: float
    case: int
    time: datetime

    @field_validator("illuminance", "voltage", "case", "co2", mode="before")
    def parse_numbers(cls, v):
        try:
            if v in {"illuminance", "voltage", "co2"}:
                return float(v)
            elif v in {"case"}:
                return int(v)
        except ValueError:
            return v
        return v
