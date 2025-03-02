from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Address:
    city: str
    state: str
    postal_code: str
    street: Optional[str] = None

    def __post_init__(self):
        if not self.city:
            raise ValueError("City cannot be empty")
        if not self.state:
            raise ValueError("State cannot be empty")
        if not self.postal_code:
            raise ValueError("Postal code cannot be empty")
