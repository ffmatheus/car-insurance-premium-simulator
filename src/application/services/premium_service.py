from src.application.dtos.car_dto import PremiumRequestDTO
from src.application.dtos.premium_dto import PremiumResponseDTO
from src.domain.entities.car import Car
from src.domain.events.premium_calculated import PremiumCalculatedEvent
from src.domain.services.premium_calculator import PremiumCalculator
from src.domain.value_objects.address import Address


class PremiumService:
    def __init__(self, premium_calculator: PremiumCalculator):
        self.premium_calculator = premium_calculator

    def _dto_to_car(self, car_dto) -> Car:
        registration_location = None
        if car_dto.registration_location:
            loc = car_dto.registration_location
            registration_location = Address(
                city=loc.city,
                state=loc.state,
                postal_code=loc.postal_code,
                street=loc.street,
            )

        return Car(
            make=car_dto.make,
            model=car_dto.model,
            year=car_dto.year,
            value=car_dto.value,
            registration_location=registration_location,
        )

    def calculate_premium(self, request: PremiumRequestDTO) -> PremiumResponseDTO:
        car = self._dto_to_car(request.car)

        premium = self.premium_calculator.calculate_premium(
            car=car,
            deductible_percentage=request.deductible_percentage,
            broker_fee=request.broker_fee,
        )

        event = PremiumCalculatedEvent(
            car=car,
            premium=premium,
            deductible_percentage=request.deductible_percentage,
            broker_fee=request.broker_fee,
        )

        return PremiumResponseDTO(
            car=request.car,
            applied_rate=premium.applied_rate,
            policy_limit=premium.policy_limit,
            calculated_premium=premium.calculated_premium,
            deductible_value=premium.deductible_value,
        )
