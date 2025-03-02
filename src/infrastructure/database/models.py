from datetime import datetime
import uuid

from sqlalchemy import (
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Boolean,
    DateTime,
    JSON,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class PremiumCalculation(Base):
    __tablename__ = "premium_calculations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    car_make = Column(String, nullable=False)
    car_model = Column(String, nullable=False)
    car_year = Column(Integer, nullable=False)
    car_value = Column(Float, nullable=False)
    deductible_percentage = Column(Float, nullable=False)
    broker_fee = Column(Float, nullable=False)
    has_location = Column(Boolean, default=False)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postal_code = Column(String, nullable=True)
    applied_rate = Column(Float, nullable=False)
    base_premium = Column(Float, nullable=False)
    deductible_value = Column(Float, nullable=False)
    policy_limit = Column(Float, nullable=False)
    calculated_premium = Column(Float, nullable=False)
    request_data = Column(JSON, nullable=False)
    response_data = Column(JSON, nullable=False)

    def __repr__(self):
        return f"<PremiumCalculation(id={self.id}, car={self.car_make} {self.car_model}, premium={self.calculated_premium})>"
