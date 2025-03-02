from src.config.settings import settings
from src.domain.entities.car import Car
from src.domain.value_objects.premium import Premium


class PremiumCalculator:
    def calculate_age_rate(self, car: Car) -> float:
        age = car.get_age()
        return age * settings.AGE_RATE_PER_YEAR

    def calculate_value_rate(self, car: Car) -> float:
        value_brackets = car.value / settings.VALUE_BRACKET
        return value_brackets * settings.VALUE_RATE_PER_10000

    def adjust_rate_by_location(self, base_rate: float, car: Car) -> float:
        if not settings.ENABLE_GIS_ADJUSTMENT or not car.registration_location:
            return base_rate

        if car.registration_location:
            postal_code = car.registration_location.postal_code
            last_digit = int(postal_code[-1])
            adjustment = (last_digit / 10) * (
                settings.MAX_GIS_ADJUSTMENT - settings.MIN_GIS_ADJUSTMENT
            ) + settings.MIN_GIS_ADJUSTMENT
            return base_rate + adjustment

        return base_rate

    def calculate_premium(
        self, car: Car, deductible_percentage: float, broker_fee: float
    ) -> Premium:
        if deductible_percentage < 0 or deductible_percentage > 1:
            raise ValueError("Deductible percentage must be between 0 and 1")
        if broker_fee < 0:
            raise ValueError("Broker fee cannot be negative")

        age_rate = self.calculate_age_rate(car)
        value_rate = self.calculate_value_rate(car)
        base_rate = age_rate + value_rate

        applied_rate = self.adjust_rate_by_location(base_rate, car)

        base_premium = car.value * applied_rate

        deductible_discount = base_premium * deductible_percentage

        calculated_premium = base_premium - deductible_discount + broker_fee

        base_policy_limit = car.value * settings.DEFAULT_COVERAGE_PERCENTAGE
        deductible_value = base_policy_limit * deductible_percentage
        policy_limit = base_policy_limit - deductible_value

        return Premium(
            applied_rate=applied_rate,
            base_premium=base_premium,
            deductible_value=deductible_value,
            policy_limit=policy_limit,
            calculated_premium=calculated_premium,
        )
