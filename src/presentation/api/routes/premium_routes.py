from fastapi import APIRouter, Depends, HTTPException

from src.application.dtos.car_dto import PremiumRequestDTO
from src.application.dtos.premium_dto import PremiumResponseDTO
from src.application.services.premium_service import PremiumService
from src.domain.services.premium_calculator import PremiumCalculator


router = APIRouter(
    prefix="/insurance",
    tags=["INSURANCE CALCULATION"],
    responses={404: {"description": "Not found"}},
)


def get_premium_service() -> PremiumService:
    premium_calculator = PremiumCalculator()
    return PremiumService(premium_calculator=premium_calculator)


@router.post("/calculate", response_model=PremiumResponseDTO)
async def calculate_premium(
    request: PremiumRequestDTO,
    premium_service: PremiumService = Depends(get_premium_service),
) -> PremiumResponseDTO:
    try:
        return premium_service.calculate_premium(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
