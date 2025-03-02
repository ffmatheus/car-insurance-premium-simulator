import datetime
import pytest

from src.domain.entities.car import Car
from src.domain.services.premium_calculator import PremiumCalculator
from src.domain.value_objects.address import Address


class TestPremiumCalculator:
    def setup_method(self):
        self.calculator = PremiumCalculator()

        self.current_year = datetime.datetime.now().year

        self.test_car = Car(
            make="Toyota",
            model="Corolla",
            year=self.current_year - 10,
            value=100000.0,
        )

        self.test_car_with_location = Car(
            make="Toyota",
            model="Corolla",
            year=self.current_year - 10,
            value=100000.0,
            registration_location=Address(
                city="São Paulo", state="SP", postal_code="01310-200"
            ),
        )

    def test_calculate_age_rate(self):
        expected_rate = 10 * 0.005
        actual_rate = self.calculator.calculate_age_rate(self.test_car)
        assert actual_rate == expected_rate

    def test_calculate_value_rate(self):
        expected_rate = (100000.0 / 10000.0) * 0.005
        actual_rate = self.calculator.calculate_value_rate(self.test_car)
        assert actual_rate == expected_rate

    def test_premium_calculation_without_location(self):
        premium = self.calculator.calculate_premium(
            car=self.test_car, deductible_percentage=0.1, broker_fee=50.0
        )

        # Expected calculations:
        # Age rate: 10 years * 0.005 = 0.05
        # Value rate: (100000 / 10000) * 0.005 = 0.05
        # Total rate: 0.05 + 0.05 = 0.10
        # Base premium: 100000 * 0.10 = 10000
        # Deductible discount: 10000 * 0.1 = 1000
        # Calculated premium: 10000 - 1000 + 50 = 9050
        # Policy limit: 100000 - (100000 * 0.1) = 90000

        assert premium.applied_rate == 0.10
        assert premium.base_premium == 10000.0
        assert premium.deductible_value == 10000.0
        assert premium.policy_limit == 90000.0
        assert premium.calculated_premium == 9050.0

    def test_invalid_deductible_percentage(self):
        with pytest.raises(ValueError):
            self.calculator.calculate_premium(
                car=self.test_car, deductible_percentage=-0.1, broker_fee=50.0
            )

        with pytest.raises(ValueError):
            self.calculator.calculate_premium(
                car=self.test_car, deductible_percentage=1.1, broker_fee=50.0
            )

    def test_invalid_broker_fee(self):
        with pytest.raises(ValueError):
            self.calculator.calculate_premium(
                car=self.test_car, deductible_percentage=0.1, broker_fee=-10.0
            )
