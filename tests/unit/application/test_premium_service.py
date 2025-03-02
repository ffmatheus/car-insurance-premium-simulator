import pytest
from unittest.mock import MagicMock

from src.application.dtos.car_dto import CarDTO, AddressDTO, PremiumRequestDTO
from src.application.services.premium_service import PremiumService
from src.domain.entities.car import Car
from src.domain.services.premium_calculator import PremiumCalculator
from src.domain.value_objects.premium import Premium


class TestPremiumService:
    def setup_method(self):
        self.mock_calculator = MagicMock(spec=PremiumCalculator)

        self.premium_service = PremiumService(premium_calculator=self.mock_calculator)

        self.address_dto = AddressDTO(
            city="São Paulo", state="SP", postal_code="01310-200"
        )

        self.car_dto = CarDTO(
            make="Toyota",
            model="Corolla",
            year=2012,
            value=100000.0,
            registration_location=self.address_dto,
        )

        self.request_dto = PremiumRequestDTO(
            car=self.car_dto, deductible_percentage=0.1, broker_fee=50.0
        )

        self.mock_premium = Premium(
            applied_rate=0.10,
            base_premium=10000.0,
            deductible_value=10000.0,
            policy_limit=90000.0,
            calculated_premium=9050.0,
        )
        self.mock_calculator.calculate_premium.return_value = self.mock_premium

    def test_dto_to_car_conversion(self):
        car = self.premium_service._dto_to_car(self.car_dto)

        assert isinstance(car, Car)
        assert car.make == "Toyota"
        assert car.model == "Corolla"
        assert car.year == 2012
        assert car.value == 100000.0
        assert car.registration_location.city == "São Paulo"
        assert car.registration_location.state == "SP"
        assert car.registration_location.postal_code == "01310-200"

    def test_calculate_premium(self):
        response_dto = self.premium_service.calculate_premium(self.request_dto)

        self.mock_calculator.calculate_premium.assert_called_once()

        assert response_dto.car == self.car_dto
        assert response_dto.applied_rate == 0.10
        assert response_dto.policy_limit == 90000.0
        assert response_dto.calculated_premium == 9050.0
        assert response_dto.deductible_value == 10000.0
