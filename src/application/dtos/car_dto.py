from typing import Optional

from pydantic import BaseModel, Field, field_validator
import datetime


class AddressDTO(BaseModel):
    city: str
    state: str
    postal_code: str
    street: Optional[str] = None

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "city": "São Paulo",
                "state": "SP",
                "postal_code": "01310-200",
                "street": "Avenida Paulista, 1000",
            }
        }


class CarDTO(BaseModel):
    make: str
    model: str
    year: int
    value: float
    registration_location: Optional[AddressDTO] = None

    @field_validator("year")
    def validate_year(cls, value):
        current_year = datetime.datetime.now().year
        if value < 1900 or value > current_year + 1:
            raise ValueError(f"Year must be between 1900 and {current_year + 1}")
        return value

    @field_validator("value")
    def validate_value(cls, value):
        if value <= 0:
            raise ValueError("Value must be positive")
        return value

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "make": "Toyota",
                "model": "Corolla",
                "year": 2012,
                "value": 100000.0,
                "registration_location": {
                    "city": "São Paulo",
                    "state": "SP",
                    "postal_code": "01310-200",
                    "street": "Avenida Paulista, 1000",
                },
            }
        }


class PremiumRequestDTO(BaseModel):
    car: CarDTO
    deductible_percentage: float = Field(gt=0, le=1)
    broker_fee: float = Field(ge=0)

    @field_validator("deductible_percentage")
    def validate_deductible_percentage(cls, value):
        if value < 0 or value > 1:
            raise ValueError("Deductible percentage must be between 0 and 1")
        return value

    @field_validator("broker_fee")
    def validate_broker_fee(cls, value):
        if value < 0:
            raise ValueError("Broker fee cannot be negative")
        return value

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "car": {
                    "make": "Toyota",
                    "model": "Corolla",
                    "year": 2012,
                    "value": 100000.0,
                    "registration_location": {
                        "city": "São Paulo",
                        "state": "SP",
                        "postal_code": "01310-200",
                    },
                },
                "deductible_percentage": 0.10,
                "broker_fee": 50.0,
            }
        }
