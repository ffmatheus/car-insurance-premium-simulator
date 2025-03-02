from dataclasses import dataclass, field
import datetime
import uuid

from src.domain.entities.car import Car
from src.domain.value_objects.premium import Premium


@dataclass
class PremiumCalculatedEvent:
    car: Car
    premium: Premium
    deductible_percentage: float
    broker_fee: float
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
