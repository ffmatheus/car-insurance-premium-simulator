import datetime
from dataclasses import dataclass
from typing import Optional

from src.domain.value_objects.address import Address


@dataclass
class Car:
    make: str
    model: str
    year: int
    value: float
    registration_location: Optional[Address] = None

    def __post_init__(self):
        current_year = datetime.datetime.now().year

        if not self.make:
            raise ValueError("Make cannot be empty")
        if not self.model:
            raise ValueError("Model cannot be empty")
        if self.year < 1900 or self.year > current_year + 1:
            raise ValueError(f"Year must be between 1900 and {current_year + 1}")
        if self.value <= 0:
            raise ValueError("Value must be positive")

    def get_age(self) -> int:
        return datetime.datetime.now().year - self.year
