from src.domain.value_objects.address import Address


class GISService:
    def calculate_risk_factor(self, address: Address) -> float:
        if not address:
            return 0.0

        try:
            last_digit = int(address.postal_code[-1])
            return (last_digit - 4.5) / 4.5
        except (ValueError, IndexError):
            return 0.0
