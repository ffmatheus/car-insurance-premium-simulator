from typing import Dict, List, Optional, Any

from sqlalchemy.orm import Session

from src.application.dtos.car_dto import PremiumRequestDTO
from src.application.dtos.premium_dto import PremiumResponseDTO
from src.infrastructure.database.models import PremiumCalculation


class PremiumRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save_calculation(
        self,
        request: PremiumRequestDTO,
        response: PremiumResponseDTO,
        base_premium: float,
    ) -> PremiumCalculation:
        calculation = PremiumCalculation(
            car_make=request.car.make,
            car_model=request.car.model,
            car_year=request.car.year,
            car_value=request.car.value,
            deductible_percentage=request.deductible_percentage,
            broker_fee=request.broker_fee,
            applied_rate=response.applied_rate,
            base_premium=base_premium,
            deductible_value=response.deductible_value,
            policy_limit=response.policy_limit,
            calculated_premium=response.calculated_premium,
            request_data=request.model_dump(),
            response_data=response.model_dump(),
        )

        if request.car.registration_location:
            calculation.has_location = True
            calculation.city = request.car.registration_location.city
            calculation.state = request.car.registration_location.state
            calculation.postal_code = request.car.registration_location.postal_code

        self.db_session.add(calculation)
        self.db_session.commit()
        self.db_session.refresh(calculation)

        return calculation

    def get_calculation_by_id(
        self, calculation_id: str
    ) -> Optional[PremiumCalculation]:
        return (
            self.db_session.query(PremiumCalculation)
            .filter(PremiumCalculation.id == calculation_id)
            .first()
        )

    def get_calculations(
        self, skip: int = 0, limit: int = 100, filters: Optional[Dict[str, Any]] = None
    ) -> List[PremiumCalculation]:
        query = self.db_session.query(PremiumCalculation)

        if filters:
            if "car_make" in filters:
                query = query.filter(PremiumCalculation.car_make == filters["car_make"])
            if "car_model" in filters:
                query = query.filter(
                    PremiumCalculation.car_model == filters["car_model"]
                )
            if "min_value" in filters:
                query = query.filter(
                    PremiumCalculation.car_value >= filters["min_value"]
                )
            if "max_value" in filters:
                query = query.filter(
                    PremiumCalculation.car_value <= filters["max_value"]
                )
            if "state" in filters:
                query = query.filter(PremiumCalculation.state == filters["state"])

        return (
            query.order_by(PremiumCalculation.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
