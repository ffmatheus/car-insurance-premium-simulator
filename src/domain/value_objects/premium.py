from dataclasses import dataclass


@dataclass(frozen=True)
class Premium:
    applied_rate: float
    base_premium: float
    deductible_value: float
    policy_limit: float
    calculated_premium: float

    def __post_init__(self):
        if self.applied_rate < 0:
            raise ValueError("Applied rate cannot be negative")
        if self.base_premium < 0:
            raise ValueError("Base premium cannot be negative")
        if self.deductible_value < 0:
            raise ValueError("Deductible value cannot be negative")
        if self.policy_limit < 0:
            raise ValueError("Policy limit cannot be negative")
        if self.calculated_premium < 0:
            raise ValueError("Calculated premium cannot be negative")
