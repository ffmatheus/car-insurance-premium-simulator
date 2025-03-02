from pydantic import BaseModel, Field

from src.application.dtos.car_dto import CarDTO


class PremiumResponseDTO(BaseModel):
    car: CarDTO
    applied_rate: float = Field(ge=0)
    policy_limit: float = Field(ge=0)
    calculated_premium: float = Field(ge=0)
    deductible_value: float = Field(ge=0)

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
                "applied_rate": 0.10,
                "policy_limit": 90000.0,
                "calculated_premium": 9050.0,
                "deductible_value": 10000.0,
            }
        }
